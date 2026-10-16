# Contributing

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

Read [README — Status](README.md#evidence-status) before describing results. Only
report benchmark scores or driving performance that a committed run supports.

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
