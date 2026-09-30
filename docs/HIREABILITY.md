# Hireability and discoverability

> Tip-cite bank: base main `b1c400a2` + this PR pending Steward; provenance only; never
> `READY`.

This page is a navigation surface for reviewers and for GitHub/wiki discovery. It does
not establish acceptance, release readiness, driving-performance results, benchmark
scores, or a `READY` claim.

## Purpose

Legacy Windows experiment: learn a nine-action driving policy from GTA V screen
captures and keyboard demonstrations. Pixels in, predicted keys out, with optional
motion-based recovery when the vehicle may be stuck. Training data and model weights
are not shipped with the repository.

## Stack

| Layer | Technologies |
| --- | --- |
| Language | Python 3.11–3.12 (`uv` for installs) |
| ML | TensorFlow, TFLearn, NumPy, pandas |
| Vision / I/O | OpenCV, Windows screen capture, keyboard hooks (`pynput`) |
| Quality | pytest, ruff, mypy (dev extra) |

See [`pyproject.toml`](../pyproject.toml) for dependency pins.

## Smallest verifiable demo

No hosted driving demo, trained weights, or retained evaluation run ships here. The
bounded evidence path is headless and inspectable:

```bash
git clone https://github.com/T-Py-T/gta5-vision-driving-agent.git
cd gta5-vision-driving-agent
uv sync --extra dev
python -m pytest tests/test_policy.py -q
python -m compileall -q src
```

These checks exercise the [policy contract](../src/policy.py) and Python syntax only.
They do not launch GTA V, load a model, or send keyboard input.

For the full Windows capture → train → control loop (local data and paths required),
follow [windows-workflow.md](windows-workflow.md).

## Review path (hiring-oriented)

1. [Policy encoding](../src/policy.py) and [headless regression suite](../tests/test_policy.py).
2. [Windows workflow](windows-workflow.md) for configuration and safety checks before
   keyboard control.
3. [OPEN_PROBLEMS.md](OPEN_PROBLEMS.md) for unresolved evidence boundaries.

This shows inspectable implementation and bounded validation; it is not live-driving
evidence and implies no score or `READY` status.

## Suggested GitHub topics

Repository maintainers may apply topic tags such as:

`computer-vision`, `machine-learning`, `tensorflow`, `python`, `opencv`, `gta5`,
`imitation-learning`, `game-ai`, `windows`

Topics aid search only; they do not certify results or readiness.

## License

Repository-specific additions are under the [MIT License](../LICENSE). The project
descends from [`Sentdex/pygta5`](https://github.com/Sentdex/pygta5); Apache-2.0 and
ISC notices remain in [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).

## Related docs

| Document | Role |
| --- | --- |
| [../README.md](../README.md) | Project overview and evidence status |
| [README.md](README.md) | Documentation index |
| [OPEN_PROBLEMS.md](OPEN_PROBLEMS.md) | Active evidence boundaries |
