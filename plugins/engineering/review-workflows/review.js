const REVIEW_RESULT_SCHEMA = {
  type: 'object',
  required: [
    'assignmentId',
    'lens',
    'summary',
    'findings',
    'filesReviewed',
    'notRelevant',
    'plannedTests',
    'gaps',
    'teachingMoments',
    'positiveFindings',
  ],
  properties: {
    assignmentId: { type: 'string' },
    lens: { type: 'string' },
    summary: { type: 'string' },
    findings: {
      type: 'array',
      items: {
        type: 'object',
        required: [
          'lens',
          'actionState',
          'bucket',
          'title',
          'file',
          'location',
          'currentCode',
          'reasoning',
          'suggestedChange',
          'references',
        ],
        properties: {
          lens: { type: 'string' },
          actionState: { enum: ['Block', 'Human Review', 'Suggestion'] },
          bucket: { type: 'string' },
          severity: { enum: ['Critical', 'Major', 'Minor'] },
          title: { type: 'string' },
          file: { type: 'string' },
          location: { type: 'string' },
          currentCode: { type: 'string' },
          reasoning: { type: 'string' },
          suggestedChange: { type: 'string' },
          references: { type: 'array', items: { type: 'string' } },
          costEvidence: { type: 'string' },
          changeImpact: { type: 'string' },
          contractContradiction: { type: 'string' },
          verificationMeasurement: { type: 'string' },
        },
        additionalProperties: false,
      },
    },
    filesReviewed: { type: 'array', items: { type: 'string' } },
    notRelevant: {
      type: 'array',
      items: {
        type: 'object',
        required: ['file', 'reason'],
        properties: {
          file: { type: 'string' },
          reason: { type: 'string' },
        },
        additionalProperties: false,
      },
    },
    plannedTests: {
      type: 'array',
      items: {
        type: 'object',
        required: ['requirement', 'status', 'evidence'],
        properties: {
          requirement: { type: 'string' },
          status: { enum: ['IMPLEMENTED', 'PARTIAL', 'MISSING'] },
          evidence: { type: 'string' },
          missingBehavior: { type: 'string' },
        },
        additionalProperties: false,
      },
    },
    gaps: { type: 'array', items: { type: 'string' } },
    teachingMoments: { type: 'array', items: { type: 'string' } },
    positiveFindings: { type: 'array', items: { type: 'string' } },
  },
  additionalProperties: false,
};

const REVIEWER_ROLES = new Set([
  'reviewer-junior',
  'reviewer-shallow',
  'reviewer-staff',
  'reviewer-thorough',
]);

const REVIEW_LENSES = new Set([
  'architecture',
  'code-style',
  'domain',
  'security',
  'performance',
]);

const UNSAFE_ASSIGNMENT_IDS = new Set([
  '__proto__',
  'constructor',
  'prototype',
]);

const ACTION_STATES = new Set(['Block', 'Human Review', 'Suggestion']);
const SEVERITIES = new Set(['Critical', 'Major', 'Minor']);
const SEVERITY_LENSES = new Set(['architecture', 'security', 'performance']);
const ARCHITECTURE_BUCKETS = new Set(['Introduced', 'Exposed', 'Observed']);
const SECURITY_ACTION_SEVERITIES = {
  Block: new Set(['Critical', 'Major']),
  'Human Review': new Set(['Major', 'Minor']),
  Suggestion: new Set(['Minor']),
};

function requireText(value, name) {
  if (typeof value !== 'string' || !value.trim()) {
    throw new Error(`${name} must be a non-empty string`);
  }
  return value;
}

function validateCodeStyleOwnership(input) {
  const codeStyleAssignments = new Set(
    input.assignments
      .filter((assignment) => assignment.lens === 'code-style')
      .map((assignment) => assignment.id),
  );
  if (codeStyleAssignments.size === 0) return;

  const reviewedFiles = requireArray(input.reviewedFiles, 'reviewedFiles');
  const ownership = requireArray(input.codeStyleOwnership, 'codeStyleOwnership');
  if (reviewedFiles.length === 0) {
    throw new Error('reviewedFiles must not be empty when code-style review is selected');
  }

  const expected = new Set();
  for (const [index, file] of reviewedFiles.entries()) {
    requireText(file, `reviewedFiles[${index}]`);
    if (expected.has(file)) throw new Error(`duplicate reviewed file: ${file}`);
    expected.add(file);
  }

  const owned = new Set();
  for (const [index, item] of ownership.entries()) {
    if (!item || typeof item !== 'object' || Array.isArray(item)) {
      throw new Error(`codeStyleOwnership[${index}] must be an object`);
    }
    const file = requireText(item.file, `codeStyleOwnership[${index}].file`);
    const assignmentId = requireText(
      item.assignmentId,
      `codeStyleOwnership[${index}].assignmentId`,
    );
    if (!expected.has(file)) throw new Error(`code-style owner has unreviewed file: ${file}`);
    if (owned.has(file)) throw new Error(`duplicate code-style owner for file: ${file}`);
    if (!codeStyleAssignments.has(assignmentId)) {
      throw new Error(`invalid code-style owner assignment for ${file}: ${assignmentId}`);
    }
    owned.add(file);
  }

  const missing = [...expected].filter((file) => !owned.has(file));
  if (missing.length) {
    throw new Error(`missing code-style owner for files: ${missing.join(', ')}`);
  }
}

function validateInputs(input) {
  if (!input || typeof input !== 'object' || Array.isArray(input)) {
    throw new Error('args must be an object');
  }
  requireText(input.reviewName, 'reviewName');
  if (!Array.isArray(input.assignments) || input.assignments.length === 0) {
    throw new Error('assignments must be a non-empty array');
  }

  const seen = new Set();
  for (const assignment of input.assignments) {
    if (!assignment || typeof assignment !== 'object' || Array.isArray(assignment)) {
      throw new Error('each assignment must be an object');
    }
    const assignmentId = requireText(assignment.id, 'assignment.id');
    requireText(assignment.label, 'assignment.label');
    requireText(assignment.lens, 'assignment.lens');
    requireText(assignment.role, 'assignment.role');
    requireText(assignment.instructions, 'assignment.instructions');
    if (assignment.model !== undefined) {
      requireText(assignment.model, 'assignment.model');
    }
    if (assignmentId !== assignmentId.trim()) {
      throw new Error('assignment.id must not have leading or trailing whitespace');
    }
    if (UNSAFE_ASSIGNMENT_IDS.has(assignmentId)) {
      throw new Error(`unsafe assignment id: ${assignmentId}`);
    }
    if (!REVIEW_LENSES.has(assignment.lens)) {
      throw new Error(
        `assignment.lens must be one of: ${[...REVIEW_LENSES].join(', ')}`,
      );
    }
    if (!REVIEWER_ROLES.has(assignment.role)) {
      throw new Error(
        `assignment.role must be one of: ${[...REVIEWER_ROLES].join(', ')}`,
      );
    }
    if (assignment.lens === 'code-style') {
      if (assignment.role !== 'reviewer-junior') {
        throw new Error(
          `code-style assignment ${assignmentId} must use role reviewer-junior`,
        );
      }
      if (assignment.model !== undefined) {
        throw new Error(
          `code-style assignment ${assignmentId} must inherit its model from role reviewer-junior`,
        );
      }
    }
    if (seen.has(assignment.id)) {
      throw new Error(`duplicate assignment id: ${assignment.id}`);
    }
    seen.add(assignment.id);
  }

  validateCodeStyleOwnership(input);

  const consolidation = input.consolidation;
  if (!consolidation || typeof consolidation !== 'object' || Array.isArray(consolidation)) {
    throw new Error('consolidation must be an object');
  }
  if (!['single', 'council'].includes(consolidation.mode)) {
    throw new Error('consolidation.mode must be single or council');
  }
  requireText(consolidation.mergerModel, 'consolidation.mergerModel');
  if (consolidation.mode === 'council') {
    requireText(consolidation.primaryModel, 'consolidation.primaryModel');
    requireText(consolidation.secondaryModel, 'consolidation.secondaryModel');
    if (consolidation.primaryModel === consolidation.secondaryModel) {
      throw new Error('council consolidation requires two distinct models');
    }
  }
}

function requireArray(value, name) {
  if (!Array.isArray(value)) {
    throw new Error(`${name} must be an array`);
  }
  return value;
}

function validateTextArray(value, name) {
  for (const [index, item] of requireArray(value, name).entries()) {
    requireText(item, `${name}[${index}]`);
  }
}

function validateArchitectureFinding(finding, index) {
  if (!ARCHITECTURE_BUCKETS.has(finding.bucket)) {
    throw new Error(`architecture finding ${index} has invalid bucket: ${finding.bucket}`);
  }

  const validAction =
    (finding.bucket === 'Introduced' && finding.actionState === 'Block' &&
      ['Critical', 'Major'].includes(finding.severity)) ||
    (finding.bucket === 'Introduced' && finding.actionState === 'Human Review' &&
      finding.severity === 'Minor') ||
    (finding.bucket === 'Exposed' && finding.actionState === 'Human Review') ||
    (finding.bucket === 'Observed' && finding.actionState === 'Suggestion');
  if (!validAction) {
    throw new Error(
      `invalid architecture bucket/actionState/severity combination: ${finding.bucket} + ${finding.actionState} + ${finding.severity}`,
    );
  }
}

function validateFinding(finding, lens, index) {
  if (!finding || typeof finding !== 'object' || Array.isArray(finding)) {
    throw new Error(`${lens} finding ${index} must be an object`);
  }

  for (const field of [
    'lens',
    'actionState',
    'bucket',
    'title',
    'file',
    'location',
    'currentCode',
    'reasoning',
    'suggestedChange',
  ]) {
    requireText(finding[field], `${lens} finding ${index}.${field}`);
  }
  validateTextArray(finding.references, `${lens} finding ${index}.references`);

  if (finding.lens !== lens) {
    throw new Error(
      `${lens} finding ${index} has mismatched lens: ${finding.lens}`,
    );
  }
  if (!ACTION_STATES.has(finding.actionState)) {
    throw new Error(
      `${lens} finding ${index} has invalid actionState: ${finding.actionState}`,
    );
  }
  const hasSeverity = Object.prototype.hasOwnProperty.call(finding, 'severity');
  if (lens === 'domain' && hasSeverity) {
    throw new Error(`domain finding ${index} must not include severity`);
  }
  if (hasSeverity && !SEVERITIES.has(finding.severity)) {
    throw new Error(
      `${lens} finding ${index} has invalid severity: ${finding.severity}`,
    );
  }
  if (SEVERITY_LENSES.has(lens) && !hasSeverity) {
    throw new Error(`${lens} finding ${index} must include severity`);
  }

  if (lens === 'architecture') {
    validateArchitectureFinding(finding, index);
  }
  if (lens === 'security' &&
      !SECURITY_ACTION_SEVERITIES[finding.actionState].has(finding.severity)) {
    throw new Error(
      `invalid security actionState/severity combination: ${finding.actionState} + ${finding.severity}`,
    );
  }
  if (lens === 'performance') {
    if (typeof finding.costEvidence !== 'string' || !finding.costEvidence.trim()) {
      throw new Error(`performance finding ${index} must include costEvidence`);
    }
    const hasChangeImpact = typeof finding.changeImpact === 'string' &&
      finding.changeImpact.trim();
    const hasContractContradiction = typeof finding.contractContradiction === 'string' &&
      finding.contractContradiction.trim();
    if (!hasChangeImpact && !hasContractContradiction) {
      throw new Error(
        `performance finding ${index} must include changeImpact or contractContradiction`,
      );
    }
    if (typeof finding.verificationMeasurement !== 'string' ||
        !finding.verificationMeasurement.trim()) {
      throw new Error(
        `performance finding ${index} must include verificationMeasurement`,
      );
    }
  }
}

function validateReviewResult(result, assignment, codeStyleOwnership) {
  if (!result || typeof result !== 'object' || Array.isArray(result)) {
    throw new Error(`review result for ${assignment.id} must be an object`);
  }

  if (result.assignmentId !== assignment.id || result.lens !== assignment.lens) {
    throw new Error(
      `review identity mismatch for ${assignment.id}: expected assignmentId=${assignment.id} lens=${assignment.lens}; received assignmentId=${String(result.assignmentId)} lens=${String(result.lens)}`,
    );
  }
  requireText(result.summary, `${assignment.id}.summary`);

  for (const [index, finding] of requireArray(
    result.findings,
    `${assignment.id}.findings`,
  ).entries()) {
    validateFinding(finding, assignment.lens, index);
  }
  validateTextArray(result.filesReviewed, `${assignment.id}.filesReviewed`);

  for (const [index, item] of requireArray(
    result.notRelevant,
    `${assignment.id}.notRelevant`,
  ).entries()) {
    if (!item || typeof item !== 'object' || Array.isArray(item)) {
      throw new Error(`${assignment.id}.notRelevant[${index}] must be an object`);
    }
    requireText(item.file, `${assignment.id}.notRelevant[${index}].file`);
    requireText(item.reason, `${assignment.id}.notRelevant[${index}].reason`);
  }

  for (const [index, item] of requireArray(
    result.plannedTests,
    `${assignment.id}.plannedTests`,
  ).entries()) {
    if (!item || typeof item !== 'object' || Array.isArray(item)) {
      throw new Error(`${assignment.id}.plannedTests[${index}] must be an object`);
    }
    requireText(item.requirement, `${assignment.id}.plannedTests[${index}].requirement`);
    requireText(item.evidence, `${assignment.id}.plannedTests[${index}].evidence`);
    if (!['IMPLEMENTED', 'PARTIAL', 'MISSING'].includes(item.status)) {
      throw new Error(
        `${assignment.id}.plannedTests[${index}] has invalid status: ${String(item.status)}`,
      );
    }
  }

  validateTextArray(result.gaps, `${assignment.id}.gaps`);
  validateTextArray(result.teachingMoments, `${assignment.id}.teachingMoments`);
  validateTextArray(result.positiveFindings, `${assignment.id}.positiveFindings`);

  if (assignment.lens === 'code-style') {
    const expected = codeStyleOwnership
      .filter((item) => item.assignmentId === assignment.id)
      .map((item) => item.file);
    const accounted = [
      ...result.filesReviewed,
      ...result.notRelevant.map((item) => item.file),
    ];
    const seen = new Set();
    for (const file of accounted) {
      if (seen.has(file)) {
        throw new Error(`${assignment.id} accounts for code-style file more than once: ${file}`);
      }
      if (!expected.includes(file)) {
        throw new Error(`${assignment.id} accounts for file owned elsewhere: ${file}`);
      }
      seen.add(file);
    }
    const missing = expected.filter((file) => !seen.has(file));
    if (missing.length) {
      throw new Error(`${assignment.id} did not account for code-style files: ${missing.join(', ')}`);
    }
  }
}

function validateReviewPacket(reviews, assignments, codeStyleOwnership = []) {
  if (!reviews || typeof reviews !== 'object' || Array.isArray(reviews)) {
    throw new Error('reviewer results must be a keyed object');
  }

  const approved = new Map(assignments.map((assignment) => [assignment.id, assignment]));
  const returnedIds = Object.keys(reviews);
  const missing = assignments
    .map((assignment) => assignment.id)
    .filter((id) => !Object.prototype.hasOwnProperty.call(reviews, id));
  const extra = returnedIds.filter((id) => !approved.has(id));
  if (missing.length || extra.length) {
    const details = [
      ...(missing.length ? [`missing [${missing.join(', ')}]`] : []),
      ...(extra.length ? [`extra [${extra.join(', ')}]`] : []),
    ];
    throw new Error(`review assignment reconciliation failed: ${details.join('; ')}`);
  }

  for (const assignment of assignments) {
    validateReviewResult(reviews[assignment.id], assignment, codeStyleOwnership);
  }
}

validateInputs(args);
phase('parallel review');
log(`Launching ${args.assignments.length} approved reviewer assignment(s).`);

const reviewerTasks = Object.create(null);
for (const assignment of args.assignments) {
  reviewerTasks[assignment.id] = () => agent(
    prompt(
      `This workflow agent has no access to the owner's conversation. The complete approved assignment follows.\n\n` +
      `Assignment ID: {assignmentId}\nLens: {lens}\n\n{instructions}\n\n` +
      `Return assignmentId and lens exactly as shown. Account for every assigned file and every supplied evidence source. ` +
      `Preserve the lens's action states, buckets, and severity rules. Submit the schema object with workflow_result exactly once.`,
      {
        assignmentId: assignment.id,
        lens: assignment.lens,
        instructions: assignment.instructions,
      },
    ),
    {
      label: assignment.label,
      role: assignment.role,
      ...(assignment.model ? { model: assignment.model } : {}),
      outputSchema: REVIEW_RESULT_SCHEMA,
    },
  );
}

// Pi's installed preflight requires an object-expression task record. The
// object-spread form preserves dynamic assignment count and stable task keys.
const reviews = await parallel('reviewers', { ...reviewerTasks });
validateReviewPacket(reviews, args.assignments, args.codeStyleOwnership);
phase('merger preparation');

const approvedReviewPlan = {
  reviewedFiles: args.reviewedFiles ?? [],
  codeStyleOwnership: args.codeStyleOwnership ?? [],
  assignments: args.assignments.map(({ id, label, lens, role, model, instructions }) => ({
    id,
    label,
    lens,
    role,
    model: model ?? 'role default',
    instructions,
  })),
};

const councilPrompt = (variant) => prompt(
  `Analyze the immutable reviewer packet independently. You have no access to the owner's conversation.\n\n` +
  `Review: {reviewName}\nCouncil variant: {variant}\n\nApproved review plan:\n{approvedReviewPlan}\n\nReviewer packet:\n{reviews}\n\n` +
  `Identify supported findings, exact same-lens duplicates, contradictions, evidence gaps, and disagreements requiring adjudication. ` +
  `Preserve lens attribution and source evidence. This is analysis for the final merger, not the review artifact. ` +
  `Submit the analysis with workflow_result exactly once.`,
  {
    reviewName: args.reviewName,
    variant,
    approvedReviewPlan,
    reviews,
  },
);

let council = null;
if (args.consolidation.mode === 'council') {
  log('Launching two independent council analyses.');
  council = await parallel('council', {
    primary: () => agent(councilPrompt('independent primary analysis'), {
      label: 'primary council reviewer',
      role: 'reviewer-thorough',
      model: args.consolidation.primaryModel,
    }),
    secondary: () => agent(councilPrompt('independent secondary analysis'), {
      label: 'secondary council reviewer',
      role: 'reviewer-thorough',
      model: args.consolidation.secondaryModel,
    }),
  });
}

phase('merger');
const mergerPrompt = prompt(
  `Merge the complete immutable review evidence into one cohesive Markdown review artifact. You have no access to the owner's conversation.\n\n` +
  `Review: {reviewName}\nMode: {mode}\n\nApproved review plan:\n{approvedReviewPlan}\n\nReviewer packet:\n{reviews}\n\nCouncil analyses, when enabled:\n{council}\n\n` +
  `Treat reviewer packets as primary evidence and council analyses as advisory adjudication. ` +
  `Preserve every supported finding's lens attribution, actionState, bucket, severity when present, source location, current code, reasoning, suggested change, references, and performance evidence fields when present. ` +
  `Merge only exact duplicate claims within the same lens; keep cross-lens findings separate and explicitly resolve council disagreements from source evidence. ` +
  `Account for every reviewed and not-relevant file, planned-test status, gap, teaching moment, and positive finding. ` +
  `Structure Markdown with Summary, Scope and execution plan, Findings by lens, Files marked not relevant, Planned tests when present, Gaps, Teaching moments, and Positive findings. ` +
  `Do not invent or weaken findings, edit source files, or describe partial evidence as complete. ` +
  `Submit the one cohesive review artifact with workflow_result exactly once.`,
  {
    reviewName: args.reviewName,
    mode: args.consolidation.mode,
    approvedReviewPlan,
    reviews,
    council: council ?? 'Not enabled',
  },
);

const report = await agent(mergerPrompt, {
  label: 'review merger',
  role: 'reviewer-thorough',
  model: args.consolidation.mergerModel,
});

return {
  reviewName: args.reviewName,
  consolidationMode: args.consolidation.mode,
  reviews,
  ...(council ? { council } : {}),
  report,
  publicationState: 'owner-validation-required',
  ownerAction: 'Validate the merged report against the reviewer packet and approved manifest, then publish it as the one review artifact.',
};
