# Security policy

> Tip-cite bank: base main `ec526c26` + PR #28. Steward resolves after merge; no `READY` claim.

## Supported versions

Security fixes apply to the current `main` branch. Older tags and forks are
unsupported unless explicitly noted in a release.

## Reporting a vulnerability

Do not open a public issue that includes credentials, exploit details, or
private environment data. Prefer GitHub's private vulnerability reporting when
the repository Security tab offers **Report a vulnerability**. If that option
is unavailable, email [`tnt850910@aol.com`](mailto:tnt850910@aol.com) with the
subject prefix `[SECURITY] gta5-vision-driving-agent` before sharing sensitive
details.

Include the affected revision, a minimal reproduction with synthetic or local
game-capture fixtures, expected impact, and any suggested mitigation. The
maintainer aims to acknowledge valid reports within a few business days. That
is an acknowledgment window, not a commitment to fix or disclose on a fixed
schedule.

## Repository boundary

This repository is a legacy GTA V vision-driving research scaffold: screen
capture, imitation-learning policies, CNN experiments, and motion recovery.
It is not a hosted service and does not operate game clients or accounts on
behalf of users.

Treat local capture pipelines and model weights as untrusted automation over
a personal machine. Do not commit credentials, game account tokens, private
capture paths tied to a real identity, or third-party API secrets. Prefer
synthetic or sanitized fixtures in issues, pull requests, and retained
artifacts.

## Evidence boundary

This policy makes no `READY` claim and does not declare production readiness. Do not
infer a score, benchmark, driving-performance result, or live evaluation from
source inspection, tests, screenshots, or documentation. For the active unresolved
evidence boundaries and held decisions, see
[docs/OPEN_PROBLEMS.md](docs/OPEN_PROBLEMS.md).
