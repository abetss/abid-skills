import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

const reviewerSkillNames = [
  'code-style-reviewer',
  'code-review-manager',
  'architecture-reviewer',
  'domain-expert-reviewer',
  'security-reviewer',
  'performance-reviewer',
];

const [
  workflowSource,
  reviewContract,
  codeStyleReference,
  codeStyleWithPlan,
  codeStyleWithoutPlan,
  codeStyleSkill,
  managerSkill,
  managerSpec,
  architectSolutionSkill,
  architectureSkill,
  architectureReference,
  ...reviewerMemories
] = await Promise.all([
  readFile(new URL('./review.js', import.meta.url), 'utf8'),
  readFile(new URL('./review-contract.md', import.meta.url), 'utf8'),
  readFile(new URL('../skills/code-style-reviewer/reference.md', import.meta.url), 'utf8'),
  readFile(new URL('../skills/code-style-reviewer/with-plan.md', import.meta.url), 'utf8'),
  readFile(new URL('../skills/code-style-reviewer/without-plan.md', import.meta.url), 'utf8'),
  readFile(new URL('../skills/code-style-reviewer/SKILL.md', import.meta.url), 'utf8'),
  readFile(new URL('../skills/code-review-manager/SKILL.md', import.meta.url), 'utf8'),
  readFile(new URL('../skills/code-review-manager/SPEC.md', import.meta.url), 'utf8'),
  readFile(new URL('../skills/architect-solution/SKILL.md', import.meta.url), 'utf8'),
  readFile(new URL('../skills/architecture-reviewer/SKILL.md', import.meta.url), 'utf8'),
  readFile(new URL('../skills/architecture-reviewer/reference.md', import.meta.url), 'utf8'),
  ...reviewerSkillNames.map((name) =>
    readFile(new URL(`../skills/${name}/memory.md`, import.meta.url), 'utf8')),
]);
const reviewerSkillTexts = await Promise.all(reviewerSkillNames.map((name) =>
  readFile(new URL(`../skills/${name}/SKILL.md`, import.meta.url), 'utf8')));
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;

function assignment(id, lens = 'code-style') {
  const isCodeStyle = lens === 'code-style';
  return {
    id,
    label: `${lens}: ${id}`,
    lens,
    role: isCodeStyle ? 'reviewer-junior' : 'reviewer-staff',
    ...(isCodeStyle ? {} : { model: 'staff-high' }),
    instructions: `Review ${id}.`,
  };
}

function finding(lens, overrides = {}) {
  return {
    lens,
    actionState: 'Block',
    bucket: lens === 'security' ? 'CWE-79' : 'Repository consistency',
    title: 'Concrete issue',
    file: 'src/example.ts',
    location: '1-2',
    currentCode: 'const unsafe = true;',
    reasoning: 'The current source contradicts the assigned contract.',
    suggestedChange: 'Replace the unsafe branch.',
    references: ['docs/contract.md'],
    ...overrides,
  };
}

function reviewResult(id, lens, findings = [], filesReviewed = ['src/example.ts']) {
  return {
    assignmentId: id,
    lens,
    summary: `Reviewed ${id}.`,
    findings,
    filesReviewed,
    notRelevant: [],
    plannedTests: [],
    gaps: [],
    teachingMoments: [],
    positiveFindings: [],
  };
}

async function runWorkflow({
  assignments,
  mode = 'single',
  mutateParallelResult,
  resultForAssignment,
  reviewedFiles: reviewedFilesOverride,
  codeStyleOwnership: codeStyleOwnershipOverride,
  calls = [],
} = {}) {
  const codeStyleAssignments = assignments.filter(({ lens }) => lens === 'code-style');
  const reviewedFiles = reviewedFilesOverride ??
    codeStyleAssignments.map((_, index) => `src/style-${index}.ts`);
  const codeStyleOwnership = codeStyleOwnershipOverride ??
    codeStyleAssignments.map((item, index) => ({
      file: reviewedFiles[index],
      assignmentId: item.id,
    }));
  const args = {
    reviewName: 'offline harness',
    assignments,
    ...(codeStyleAssignments.length ? { reviewedFiles, codeStyleOwnership } : {}),
    consolidation: {
      mode,
      mergerModel: 'model/merger:xhigh',
      ...(mode === 'council'
        ? { primaryModel: 'model/primary:high', secondaryModel: 'model/secondary:high' }
        : {}),
    },
  };

  const agent = async (agentPrompt, options = {}) => {
    calls.push({ agentPrompt, options });
    if (!options.outputSchema) {
      return `Merged by ${options.model}.`;
    }

    const id = /Assignment ID: ([^\n]+)/.exec(agentPrompt)?.[1];
    const lens = /Lens: ([^\n]+)/.exec(agentPrompt)?.[1];
    assert.ok(id, 'reviewer prompt includes assignment ID');
    assert.ok(lens, 'reviewer prompt includes lens');
    const ownedFiles = codeStyleOwnership
      .filter((item) => item.assignmentId === id)
      .map((item) => item.file);
    return resultForAssignment?.(id, lens, ownedFiles) ??
      reviewResult(id, lens, [], ownedFiles.length ? ownedFiles : ['src/example.ts']);
  };

  const parallel = async (operation, tasks) => {
    const entries = await Promise.all(
      Object.entries(tasks).map(async ([key, task]) => [key, await task()]),
    );
    const results = Object.create(null);
    for (const [key, value] of entries) {
      Object.defineProperty(results, key, {
        configurable: true,
        enumerable: true,
        value,
        writable: true,
      });
    }
    return mutateParallelResult?.(operation, results) ?? results;
  };

  const prompt = (template, values) => template.replace(
    /{([A-Za-z_$][\w$]*)}/g,
    (_match, key) => typeof values[key] === 'string'
      ? values[key]
      : JSON.stringify(values[key], null, 2),
  );

  const execute = new AsyncFunction('args', 'agent', 'parallel', 'prompt', 'phase', 'log', workflowSource);
  const output = await execute(args, agent, parallel, prompt, () => {}, () => {});
  return { calls, output };
}

test('runs ordinary dynamic assignments and one merger', async () => {
  const assignments = [
    assignment('style-client'),
    assignment('domain-state', 'domain'),
    assignment('performance-worker', 'performance'),
  ];
  const { calls, output } = await runWorkflow({ assignments });

  assert.deepEqual(Object.keys(output.reviews), assignments.map(({ id }) => id));
  assert.equal(output.consolidationMode, 'single');
  assert.equal(output.publicationState, 'owner-validation-required');
  assert.equal(calls.filter(({ options }) => options.outputSchema).length, 3);
  assert.equal(calls.filter(({ options }) => !options.outputSchema).length, 1);
});

test('requires exactly one code-style owner for every reviewed file', async () => {
  const assignments = [assignment('style-client')];

  await assert.rejects(
    runWorkflow({
      assignments,
      reviewedFiles: ['src/a.ts', 'src/b.ts'],
      codeStyleOwnership: [{ file: 'src/a.ts', assignmentId: 'style-client' }],
    }),
    /missing code-style owner for files: src\/b\.ts/,
  );

  await assert.rejects(
    runWorkflow({
      assignments,
      reviewedFiles: ['src/a.ts'],
      codeStyleOwnership: [
        { file: 'src/a.ts', assignmentId: 'style-client' },
        { file: 'src/a.ts', assignmentId: 'style-client' },
      ],
    }),
    /duplicate code-style owner for file: src\/a\.ts/,
  );
});

test('reconciles returned code-style file coverage before the merger', async () => {
  const assignments = [assignment('style-client')];
  const calls = [];

  await assert.rejects(
    runWorkflow({
      assignments,
      reviewedFiles: ['src/a.ts'],
      codeStyleOwnership: [{ file: 'src/a.ts', assignmentId: 'style-client' }],
      resultForAssignment: (id, lens) => reviewResult(id, lens, [], []),
      calls,
    }),
    /style-client did not account for code-style files: src\/a\.ts/,
  );
  assert.equal(calls.filter(({ options }) => !options.outputSchema).length, 0);

  await assert.rejects(
    runWorkflow({
      assignments: [assignment('style-a'), assignment('style-b')],
      reviewedFiles: ['src/a.ts', 'src/b.ts'],
      codeStyleOwnership: [
        { file: 'src/a.ts', assignmentId: 'style-a' },
        { file: 'src/b.ts', assignmentId: 'style-b' },
      ],
      resultForAssignment: (id, lens, ownedFiles) => reviewResult(
        id,
        lens,
        [],
        id === 'style-a' ? ['src/b.ts'] : ownedFiles,
      ),
    }),
    /style-a accounts for file owned elsewhere: src\/b\.ts/,
  );

  await assert.rejects(
    runWorkflow({
      assignments,
      reviewedFiles: ['src/a.ts'],
      codeStyleOwnership: [{ file: 'src/a.ts', assignmentId: 'style-client' }],
      resultForAssignment: (id, lens) => {
        const result = reviewResult(id, lens, [], ['src/a.ts']);
        result.notRelevant = [{ file: 'src/a.ts', reason: 'duplicate accounting' }];
        return result;
      },
    }),
    /style-client accounts for code-style file more than once: src\/a\.ts/,
  );
});

test('enforces the reviewer-junior role default for every code-style assignment', async () => {
  const wrongRole = assignment('style-wrong-role');
  wrongRole.role = 'reviewer-staff';
  await assert.rejects(
    runWorkflow({ assignments: [wrongRole] }),
    /code-style assignment style-wrong-role must use role reviewer-junior/,
  );

  const modelOverride = assignment('style-model-override');
  modelOverride.model = 'staff-high';
  await assert.rejects(
    runWorkflow({ assignments: [modelOverride] }),
    /code-style assignment style-model-override must inherit its model from role reviewer-junior/,
  );
});

test('passes approved ownership, evidence, and model choices into the merger', async () => {
  const calls = [];
  const style = assignment('style-client');
  style.instructions = 'Apply convention /rules/typescript.md because **/*.ts matched src/style-0.ts.';
  const architecture = assignment('architecture-api', 'architecture');
  architecture.instructions = 'Apply /Users/abtinghods/.agents/expertise/architecture/rest-api/expertise.md and its references/rest-api-guidance.md because the proposed solution changes an HTTP resource contract.';

  await runWorkflow({ assignments: [style, architecture], calls });
  const reviewerCall = calls.find(({ options }) => options.label === style.label);
  const mergerCall = calls.find(({ options }) => options.label === 'review merger');
  assert.equal(reviewerCall.options.role, 'reviewer-junior');
  assert.equal(reviewerCall.options.model, undefined);
  assert.match(mergerCall.agentPrompt, /Approved review plan:/);
  assert.match(mergerCall.agentPrompt, /codeStyleOwnership/);
  assert.match(mergerCall.agentPrompt, /src\/style-0\.ts/);
  assert.match(mergerCall.agentPrompt, /\/rules\/typescript\.md/);
  assert.match(mergerCall.agentPrompt, /architecture\/rest-api\/expertise\.md/);
  assert.match(mergerCall.agentPrompt, /references\/rest-api-guidance\.md/);
  assert.match(mergerCall.agentPrompt, /HTTP resource contract/);
  assert.equal(mergerCall.options.role, 'reviewer-thorough');
  assert.equal(mergerCall.options.model, 'model/merger:xhigh');
});

for (const id of ['__proto__', 'constructor', 'prototype']) {
  test(`rejects unsafe assignment ID ${id}`, async () => {
    await assert.rejects(
      runWorkflow({ assignments: [assignment(id)] }),
      new RegExp(`unsafe assignment id: ${id}`),
    );
  });
}

test('rejects a missing returned assignment before the merger', async () => {
  await assert.rejects(
    runWorkflow({
      assignments: [assignment('style-client'), assignment('domain-state', 'domain')],
      mutateParallelResult(operation, results) {
        if (operation === 'reviewers') delete results['domain-state'];
        return results;
      },
    }),
    /review assignment reconciliation failed: missing \[domain-state\]/,
  );
});

test('rejects an extra returned assignment before the merger', async () => {
  await assert.rejects(
    runWorkflow({
      assignments: [assignment('style-client')],
      mutateParallelResult(operation, results) {
        if (operation === 'reviewers') {
          results.unapproved = reviewResult('unapproved', 'code-style');
        }
        return results;
      },
    }),
    /review assignment reconciliation failed: extra \[unapproved\]/,
  );
});

test('rejects returned assignmentId and lens mismatches before the merger', async () => {
  await assert.rejects(
    runWorkflow({
      assignments: [assignment('security-auth', 'security')],
      resultForAssignment: () => reviewResult('other-id', 'performance'),
    }),
    /review identity mismatch for security-auth: expected assignmentId=security-auth lens=security; received assignmentId=other-id lens=performance/,
  );
});

test('accepts all domain action states without severity', async () => {
  for (const actionState of ['Block', 'Human Review', 'Suggestion']) {
    const id = `domain-${actionState}`;
    const { output } = await runWorkflow({
      assignments: [assignment(id, 'domain')],
      resultForAssignment: (assignmentId, lens) => reviewResult(
        assignmentId,
        lens,
        [finding(lens, {
          actionState,
          bucket: 'Business-rule correctness',
        })],
      ),
    });

    assert.equal(output.consolidationMode, 'single');
    assert.equal(
      Object.prototype.hasOwnProperty.call(output.reviews[id].findings[0], 'severity'),
      false,
    );
  }
});

for (const mode of ['single', 'council']) {
  test(`rejects domain severity before the ${mode} merger`, async () => {
    const calls = [];
    await assert.rejects(
      runWorkflow({
        assignments: [assignment(`domain-severity-${mode}`, 'domain')],
        mode,
        calls,
        resultForAssignment: (id, lens) => reviewResult(
          id,
          lens,
          [finding(lens, {
            bucket: 'Business-rule correctness',
            severity: 'Major',
          })],
        ),
      }),
      /domain finding 0 must not include severity/,
    );
    assert.equal(
      calls.filter(({ options }) => !options.outputSchema).length,
      0,
      'council or merger must not start for an invalid domain finding',
    );
  });
}

test('routes conventions through path-matched and content-matched branches', () => {
  assert.match(codeStyleReference, /15 path-matched documents under `path-matched\/`/);
  assert.match(codeStyleReference, /5 semantic documents under `content-matched\/`/);
  assert.match(codeStyleReference, /A keyword alone is insufficient\./);
});

test('requires exact convention reasons, code-style ownership, and manager composition', () => {
  const missingMessage = 'Convention files are needed under ~/.agents/conventions/ or {project}/.agents/conventions/.';

  assert.match(codeStyleReference, /table-of-content\.md/);
  assert.match(codeStyleReference, /exact `paths` metadata/);
  assert.match(codeStyleReference, /task, diff, imports, APIs, schemas, and changed behavior/);
  assert.match(codeStyleReference, /A keyword alone is insufficient\./);
  assert.match(codeStyleReference, /Every reviewed file has exactly one code-style owner\./);
  assert.match(codeStyleReference, /Use plan-named example files first\./);
  assert.match(codeStyleReference, /IMPLEMENTED/);
  assert.ok(codeStyleReference.includes(missingMessage));
  assert.ok(codeStyleWithPlan.includes(missingMessage));
  assert.match(codeStyleWithPlan, /every promised test\/verification scenario/i);
  assert.match(codeStyleWithoutPlan, /without inferring test completeness/i);
  assert.match(codeStyleSkill, /Stop at the assignment manifest/);
  for (const source of [codeStyleReference, codeStyleWithPlan, codeStyleWithoutPlan, codeStyleSkill]) {
    assert.match(source, /reviewer-junior/);
  }
  assert.match(codeStyleReference, /omit a model override/i);
  assert.match(managerSkill, /Build the code-style manifest/);
  assert.match(managerSkill, /reviewer-junior/);
  assert.match(managerSkill, /Display one combined proposal/);
  assert.match(managerSpec, /without recursively starting their standalone approvals or workflows/);
});

test('keeps memory local to every independently invokable reviewer skill', () => {
  assert.equal(reviewerMemories.length, reviewerSkillNames.length);
  for (const [index, memory] of reviewerMemories.entries()) {
    assert.match(memory, /^# .+ — Memory/m, `${reviewerSkillNames[index]} memory has a title`);
    assert.match(
      reviewerSkillTexts[index],
      /\(memory\.md\)/,
      `${reviewerSkillNames[index]} points to its local memory`,
    );
    assert.doesNotMatch(
      reviewerSkillTexts[index],
      /\.\.\/[^)]+\/memory\.md/,
      `${reviewerSkillNames[index]} does not borrow another skill's memory`,
    );
  }
  assert.match(codeStyleReference, /\[`memory\.md`\]\(memory\.md\)/);
  assert.match(managerSpec, /Every reviewer skill owns its own `memory\.md`/);
  assert.match(reviewContract, /Every independently invokable reviewer skill owns and reads its own `memory\.md`/);
});

test('preserves architect-solution ownership and local-first expertise fallback', () => {
  assert.match(architectSolutionSkill, /Inspect this skill's `experts\/` directory/);
  assert.match(architectSolutionSkill, /Treat an absent directory as empty/);
  assert.match(architectSolutionSkill, /For every material concern without an applicable local expert/);
  assert.match(architectSolutionSkill, /Consider every `ACTIVE` entry/);

  assert.match(architectureSkill, /\[Canonical architect solution\]\(\.\.\/architect-solution\/SKILL\.md\)/);
  assert.match(architectureSkill, /inspect its optional local `experts\/` first/);
  assert.match(architectureSkill, /use the global expertise index only for uncovered material concerns/);
  assert.match(architectureReference, /absent directory is equivalent to an empty directory/);
  assert.match(architectureReference, /Only for those concerns/);
  assert.match(managerSkill, /follow canonical `architect-solution`/);
  assert.match(managerSpec, /`architect-solution` is the canonical architecture owner/);

  for (const text of [architectureSkill, architectureReference, managerSkill, managerSpec]) {
    assert.doesNotMatch(text, /\.pi\/agent\/skills\/architect/);
  }
  assert.doesNotMatch(architectureSkill, /\.agents\/expertise\/architecture\/contention\/expertise\.md/);
});

test('accepts valid security action-state and severity combinations', async () => {
  for (const [actionState, severity] of [
    ['Block', 'Critical'],
    ['Block', 'Major'],
    ['Human Review', 'Major'],
    ['Human Review', 'Minor'],
    ['Suggestion', 'Minor'],
  ]) {
    const { output } = await runWorkflow({
      assignments: [assignment(`security-${actionState}-${severity}`, 'security')],
      resultForAssignment: (id, lens) => reviewResult(
        id,
        lens,
        [finding(lens, { actionState, severity })],
      ),
    });
    assert.equal(output.consolidationMode, 'single');
  }
});

test('rejects security findings without severity', async () => {
  await assert.rejects(
    runWorkflow({
      assignments: [assignment('security-missing-severity', 'security')],
      resultForAssignment: (id, lens) => reviewResult(id, lens, [finding(lens)]),
    }),
    /security finding 0 must include severity/,
  );
});

for (const [actionState, severity] of [
  ['Suggestion', 'Critical'],
  ['Suggestion', 'Major'],
  ['Human Review', 'Critical'],
  ['Block', 'Minor'],
]) {
  test(`rejects invalid security combination ${actionState} plus ${severity}`, async () => {
    await assert.rejects(
      runWorkflow({
        assignments: [assignment(`security-invalid-${actionState}-${severity}`, 'security')],
        resultForAssignment: (id, lens) => reviewResult(
          id,
          lens,
          [finding(lens, { actionState, severity })],
        ),
      }),
      new RegExp(`invalid security actionState/severity combination: ${actionState} \\+ ${severity}`),
    );
  });
}

test('accepts performance findings with explicit cost and impact evidence', async () => {
  const { output } = await runWorkflow({
    assignments: [assignment('performance-query', 'performance')],
    resultForAssignment: (id, lens) => reviewResult(
      id,
      lens,
      [finding(lens, {
        actionState: 'Block',
        bucket: 'N+1 queries',
        severity: 'Major',
        costEvidence: 'The changed request path executes one query per returned row.',
        changeImpact: 'The change makes the loop reachable from the list endpoint.',
        verificationMeasurement: 'Assert query count remains constant as row count increases.',
      })],
    ),
  });
  assert.equal(output.consolidationMode, 'single');
});

test('rejects performance findings that only state a pattern hypothesis', async () => {
  await assert.rejects(
    runWorkflow({
      assignments: [assignment('performance-hypothesis', 'performance')],
      resultForAssignment: (id, lens) => reviewResult(
        id,
        lens,
        [finding(lens, {
          actionState: 'Human Review',
          bucket: 'N+1 queries',
          severity: 'Major',
        })],
      ),
    }),
    /performance finding 0 must include costEvidence/,
  );
});

test('runs council analysis and then one final merger', async () => {
  const { calls, output } = await runWorkflow({
    assignments: [assignment('architecture-boundary', 'architecture')],
    mode: 'council',
    resultForAssignment: (id, lens) => reviewResult(
      id,
      lens,
      [finding(lens, {
        actionState: 'Block',
        bucket: 'Introduced',
        severity: 'Major',
      })],
    ),
  });

  assert.equal(output.consolidationMode, 'council');
  assert.equal(output.publicationState, 'owner-validation-required');
  assert.deepEqual(Object.keys(output.council), ['primary', 'secondary']);
  assert.equal(typeof output.report, 'string');
  assert.equal(calls.filter(({ options }) => !options.outputSchema).length, 3);
  assert.equal(calls.filter(({ options }) => options.label === 'review merger').length, 1);
});
