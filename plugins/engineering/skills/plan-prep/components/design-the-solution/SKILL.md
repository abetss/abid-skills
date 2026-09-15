# Design the Solution

> Compose the solution-design concerns needed to make the work implementation-ready.

## Need

Different work needs different design depth. Select only the concerns needed to define a coherent solution without turning technical design into a separate planning component. The approved outputs of the selected concerns are the technical design.

## Inputs

- Requirements or an equivalent statement of scope
- Available findings from other selected plan-prep components
- Relevant codebase access and project instructions when a selected concern requires them

Available inputs improve fidelity but do not impose an execution order.

## Concerns

| Concern | Read when selected | Select when |
|---|---|---|
| Desired flows | `design-flows.md` | End-to-end behavior, branches, or data movement need definition |
| Modules and ownership boundaries | `design-modules-and-boundaries.md` | Responsibilities, placement, or dependencies between modules need definition |
| Interfaces, types, validation schemas, and data contracts | `design-interfaces-types-and-schemas.md` | Collaborating parts need explicit contracts or data shapes |
| Architecture-decision resolution | `resolve-architecture-decisions.md` | Material architecture points are routed to this component for resolution |

`Discover Existing Capabilities and Solutions` supplies native-platform and nearby adopt/extend/build evidence when applicable. `Research Solution Precedents` supplies broader architectural evidence when useful. Both remain independently selected components; use their available findings where they materially support a concern.

## Procedure

1. Select the concerns required for this work and state what each must resolve. Selection is complete when every known solution-design gap belongs to a selected concern or is explicitly out of scope.
2. Map the actual dependencies between selected concerns. At each stage, run every dependency-ready concern concurrently up to available capacity. Serialize only a true input dependency, user checkpoint, or single-writer integration; there is no default sequence. Get user approval on the concern selection and dependency plan.
3. Read and follow each selected concern document. Throughout every concern, surface architecture points through `../architecture-decision-protocol.md`; route rather than duplicate its lifecycle rules. Revisit the dependency map when a concern produces input or a blocking decision for another concern.
4. Integrate the approved concern outputs and check them for contradictions. Put returned module/boundary and interface/contract sections in `technical-design.md`; retain each other concern's specified output. Apply the architecture protocol's build-versus-reuse evidence gate. The solution design is complete when every selected concern has a completed, user-approved output, their shared boundaries and contracts agree, and blocking architecture or discovery points affecting the design are resolved.

There is no separate Define Technical Design pass: the aggregate of the selected concern outputs is the technical design.
