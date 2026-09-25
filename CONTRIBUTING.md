# Contributing

> Tip-cite bank: base main `093465d3` + PR #29. Steward resolves after merge; no `READY` claim; this guide does not establish `READY` status.

Thanks for helping improve this legacy Windows vision-driving experiment. Keep
changes focused, reviewable, and honest about what the repository can support.

## Before opening a pull request

- Start from the current `main` branch and use a short branch name that
  describes the change.
- Keep one concern per pull request and explain the files, behavior, or
  documentation affected.
- Do not commit credentials, local datasets, model weights, generated output,
  local environments, or editor settings.
- Preserve third-party notices and licensing terms when changing upstream-
  derived code or assets.

## Evidence and claims

Read the [README evidence status](README.md#evidence-status) before describing
results. This repository has no retained trained weights, gameplay recordings,
or evaluation run. Do not claim a benchmark score, driving performance, or
`READY` status that the retained evidence does not support. A contribution
guide is not evidence of readiness; do not invent scores or evaluation
results.

## Local validation

The documented headless checks do not require GTA V, TensorFlow, screen
capture, or model files:

```bash
python -m pytest tests/test_policy.py -q
python -m compileall -q src
```

If a change affects the Windows experiment workflow, also review the
[Windows workflow](docs/windows-workflow.md) and describe any machine-specific
assumptions in the pull request. Never enable keyboard control without a safe
game session and a manual stop key.

## Pull requests

1. Describe the change, its evidence, and the validation you ran.
2. Add or update tests for executable behavior; keep documentation changes
   limited to the claim they can support.
3. Keep performance language narrower than the retained evaluation supports.
4. Wait for the pull-request checks to pass before requesting merge.

