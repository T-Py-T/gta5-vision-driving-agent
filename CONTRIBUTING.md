# Contributing

> Tip-cite bank: base main `9d13043` + this PR pending Steward; provenance only; never
> `READY`.

Thanks for helping improve this legacy Windows vision-driving experiment. Keep
changes focused, reviewable, and honest about what the repository can support.

## Before opening a pull request

- Start from the current `main` branch and use a short branch name that
  describes the change.
- Keep one concern per pull request and explain the files, behavior, or
  documentation affected.
- Do not commit credentials, local datasets, model weights, generated output,
  local environments, or editor settings. Report security issues via
  [SECURITY.md](SECURITY.md), not a public issue with exploit details.
- Preserve third-party notices and licensing terms when changing upstream-
  derived code or assets.

## Evidence and claims

Read [README — Evidence status](README.md#evidence-status) and
[docs/HIREABILITY.md](docs/HIREABILITY.md) before describing results. Do not
claim benchmark scores, driving performance, or `READY` status that the
retained evidence does not support.

## Local validation

Use the headless checks in [README — Local validation](README.md#local-validation).
For Windows capture or keyboard control changes, also review
[docs/windows-workflow.md](docs/windows-workflow.md) and note machine-specific
assumptions in the pull request.

## Pull requests

1. Describe the change, its evidence, and the validation you ran.
2. Add or update tests for executable behavior; keep documentation aligned with
   what you can support.
3. Wait for pull-request checks to pass before requesting merge.
