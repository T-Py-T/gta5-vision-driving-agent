# Open problems and held decisions

**Status:** active inventory. This page is a docs record, not an acceptance gate,
scorecard, release declaration, or `READY` claim.

This repository is a legacy Windows vision-driving experiment. It has useful
source and headless policy evidence, but it does not retain the local dataset,
trained weights, gameplay recordings, or an evaluation run. The items below
keep those boundaries visible without turning missing evidence into a score.

## Scope and evidence boundary

The portfolio covered here is the path from GTA V screen pixels to one of nine
keyboard-action classes, followed by optional keyboard control and motion-based
stuck recovery. The repository can show implementation details and run the
headless policy regression and Python compilation checks. Those checks do not
run GTA V, exercise screen capture, send keyboard input, or establish driving
performance.

## Open items

### [GAP] Reproducible dataset and model provenance is incomplete

Training data and model weights are local inputs and are not retained in this
repository. The historical scripts also contain machine-specific paths and
model settings. A future reproducible run needs an authorized dataset and
model record, preprocessing/configuration details, dependency versions, and a
traceable artifact reference; this inventory does not infer any of them.

### [UNTESTED] Gameplay and simulation evidence is not retained

There is no source gameplay recording or retained GTA V run showing the agent
collecting frames, predicting actions, controlling the vehicle, or recovering
from a stuck state. The Windows workflow is an experiment guide, not evidence
that the closed loop works in a current game or environment.

### [GAP] Evaluation protocol and telemetry are undefined for a retained run

No retained evaluation defines routes or scenarios, initialization conditions,
run duration, intervention rules, failure categories, telemetry fields, or
repetition requirements. Until an authorized evaluation records those inputs
and its raw outputs, driving-performance metrics cannot be compared or
reported. Do not invent scores, success rates, or other results.

### [UNTESTED] Action coverage and behavior under live input remain open

The policy module and regression tests cover the nine-action encoding contract,
but they do not establish that a trained policy sees representative class
coverage or behaves safely under live keyboard control. Class distributions,
latency, key-release behavior, and motion-recovery behavior require a bounded
Windows test with a manual stop path and retained evidence.

### [GAP] Platform and dependency portability is unresolved

Capture and direct-keyboard behavior are Windows-specific and the full training
path depends on a compatible TensorFlow/TFLearn environment. The headless
checks intentionally avoid those dependencies. A future operator must record
the authorized OS, game/display configuration, dependency environment, and
screen/input assumptions rather than treating the local checks as portability
proof.

## Held decisions

- Do not publish a driving-performance score, benchmark, success rate, or
  comparative result from this repository.
- Do not claim `READY`, production readiness, or a working live driving loop
  from source inspection, policy tests, compilation checks, screenshots, or
  documentation alone.
- Do not treat synthetic, partial, or unretained gameplay evidence as a
  substitute for a bounded evaluation with its raw artifacts and telemetry.
- Before any live control test, use an authorized safe game session, verify a
  manual stop key, and retain the configuration and run record needed to
  interpret the result.
- Keep local datasets, model weights, credentials, and machine-specific
  settings out of the repository unless their inclusion is explicitly safe and
  authorized.

## Evidence and tip-cite protocol

Keep implementation evidence, headless-check evidence, live gameplay evidence,
and evaluation telemetry distinct. When an item changes, add the authoritative
run record, artifact reference, or reproducible test result rather than
turning an unresolved item into a summary score.

For ship handoffs, a tip-cite is a trace pointer consisting of at least eight
hexadecimal characters from the relevant `main` tip plus the PR number. The
Steward resolves that pointer after merge to the new `main` tip. A tip-cite is
not approval and never implies `READY`.

Example format:

> Tip-cite bank: base main `0d7f54c0` + PR #N. Steward resolves; no READY claim.

The README footer carries the ship-specific bank entry. Keep it factual,
resolvable, and explicit about the absence of a `READY` claim.

## Explicit non-claims

- No item above is `READY`.
- No score, metric, driving-performance result, or comparative result is
  asserted.
- No live GTA V run, trained model, dataset, or evaluation telemetry is
  inferred from repository artifacts.
- No future evaluation is authorized by this inventory.
