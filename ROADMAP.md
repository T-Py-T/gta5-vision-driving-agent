# Roadmap

> Tip-cite bank: base main `ded97f66` + PR #38. Steward resolves after merge; no
> `READY` claim.

**Status:** planning inventory. This page is docs-only. It does not establish
acceptance, release readiness, driving-performance results, or a `READY`
claim.

## Baseline on main

This roadmap is written against `main` after
[T-Py-T/gta5-vision-driving-agent #38](https://github.com/T-Py-T/gta5-vision-driving-agent/pull/38)
(`ded97f66`), which added [CHANGELOG.md](CHANGELOG.md). Earlier hireability
documentation ships remain recorded there. Nothing below upgrades that baseline
to `READY`.

## What is inspectable today

The README describes a bounded evidence path that exists on `main` without
GTA V, trained weights, or retained gameplay recordings:

- the nine-action policy contract in [`src/policy.py`](src/policy.py);
- the headless regression suite in [`tests/test_policy.py`](tests/test_policy.py);
- Python syntax checks via `python -m compileall -q src`; and
- the staged Windows experiment guide in
  [docs/windows-workflow.md](docs/windows-workflow.md).

These artifacts support code review and local headless validation. They are not
a driving-performance result and do not authorize live control without a
separate bounded Windows test.

## Planned work

The items below are derived from [README.md](README.md) and
[docs/OPEN_PROBLEMS.md](docs/OPEN_PROBLEMS.md). Labels follow the open-problems
inventory. None of them are complete, scored, or `READY`.

### [GAP] Reproducible dataset and model provenance

Training data and model weights are local inputs and are not retained in this
repository. Historical scripts still contain machine-specific paths and model
settings.

Planned documentation and operator work:

- record an authorized dataset and model artifact reference outside Git when one
  exists;
- document preprocessing, configuration, and dependency versions for any future
  reproducible run; and
- trace the collect → balance → train path described in the README and Windows
  workflow without inferring missing artifacts.

### [UNTESTED] Gameplay and simulation evidence

There is no source gameplay recording or retained GTA V run showing collection,
inference, keyboard control, or motion-based stuck recovery.

Planned work:

- run the closed loop only in an authorized safe game session with a manual stop
  key, following [docs/windows-workflow.md](docs/windows-workflow.md);
- retain configuration, capture geometry, and run records needed to interpret
  any result; and
- treat the workflow as an experiment guide until bounded evidence is retained.

### [GAP] Evaluation protocol and telemetry

No retained evaluation defines routes, initialization, run duration,
intervention rules, failure categories, telemetry fields, or repetition
requirements.

Planned work:

- define an evaluation protocol before reporting any driving outcome;
- record raw telemetry and artifacts for any authorized evaluation; and
- avoid inventing scores, success rates, or comparative results until that
  protocol and its outputs exist.

### [UNTESTED] Action coverage and live-input behavior

The policy module and regression tests cover the nine-action encoding contract
only. They do not establish class coverage, latency, key-release behavior, or
motion-recovery behavior under live keyboard control.

Planned work:

- verify representative class coverage during collection and training on an
  authorized Windows setup;
- exercise keyboard control with the pause/stop path documented in the Windows
  workflow; and
- retain evidence for motion-recovery behavior in [`src/motion.py`](src/motion.py)
  during any bounded live test.

### [GAP] Platform and dependency portability

Capture and direct-keyboard modules are Windows-specific. The full training
path depends on a compatible TensorFlow/TFLearn environment that the headless
checks intentionally avoid.

Planned work:

- record the authorized OS, game or display configuration, dependency
  environment, and screen or input assumptions for any future operator run;
- preserve a working lockfile and environment once the historical model stack
  imports successfully, as noted in the Windows workflow; and
- treat headless policy and compilation checks as portability evidence for the
  dependency-free modules only.

## Held decisions

These boundaries remain in force while the items above are open:

- do not publish a driving-performance score, benchmark, success rate, or
  comparative result from this repository;
- do not claim `READY`, production readiness, or a working live driving loop
  from source inspection, policy tests, compilation checks, screenshots, or
  documentation alone;
- do not treat synthetic, partial, or unretained gameplay evidence as a
  substitute for a bounded evaluation with raw artifacts and telemetry; and
- keep local datasets, model weights, credentials, and machine-specific settings
  out of the repository unless inclusion is explicitly safe and authorized.

See [docs/OPEN_PROBLEMS.md](docs/OPEN_PROBLEMS.md) for the active inventory and
tip-cite protocol.

## Explicit non-claims

- No roadmap item is `READY`.
- No score, metric, driving-performance result, or comparative result is
  asserted or planned as a target number here.
- No live GTA V run, trained model, dataset, or evaluation telemetry is inferred
  from repository artifacts.
- Completing documentation listed here does not by itself authorize live control
  or establish driving performance.
