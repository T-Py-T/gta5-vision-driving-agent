# GTA V Vision Driving Agent

A legacy computer-vision driving-agent study that learns a nine-action policy
from screen captures and keyboard demonstrations. The repository is useful as
an inspectable implementation case study: it shows the data path from Windows
screen capture through convolutional inference to direct keyboard control.

> [!NOTE]
> This is an archived experiment, not a current production package. The source
> is retained to make the architecture and technical decisions reviewable. No
> model weights, training dataset, benchmark run, or reproducible gameplay
> result is published here, so this repository makes no accuracy, frame-rate,
> convergence, or gameplay-performance claim.

## What the public repository demonstrates

| Evidence | Where to inspect it | What it proves |
| --- | --- | --- |
| Nine-action imitation policy | [`src/policy.py`](src/policy.py) | Deterministic encoding for forward, reverse, steering combinations, and no-key |
| Windows frame capture | [`src/grabscreen.py`](src/grabscreen.py) | Region-based desktop capture for visual observations |
| CNN experiments | [`src/models.py`](src/models.py), [`src/training/alexnet.py`](src/training/alexnet.py) | Multiple TFLearn convolutional architectures with a nine-class output |
| Data collection and balancing | [`src/collect_data.py`](src/collect_data.py), [`src/training/balance_data.py`](src/training/balance_data.py) | Keyboard-labelled frame collection and class-balancing workflow |
| Closed-loop control | [`src/test_model.py`](src/test_model.py), [`src/motion.py`](src/motion.py) | Prediction-to-key mapping plus motion-based stuck detection |
| Headless regression check | [`tests/test_policy.py`](tests/test_policy.py) | The action-encoding contract can be verified without GTA V, Windows input, or model files |

## Architecture

```text
Windows desktop capture
        │
        ▼
crop + resize + RGB conversion
        │
        ├──────────────► labelled frame batches ──► balancing ──► CNN training
        │                                                        │
        └────────────────────────────────────────────────────────▼
                                                      nine action scores
                                                               │
                                                               ▼
                                                 keyboard control + motion
                                                      recovery heuristic
```

The code explores an imitation-learning loop rather than a game API: the agent
observes pixels, learns from recorded key presses, and emits one of nine
discrete driving actions. That boundary makes the approach portable in
principle, while also making it sensitive to screen geometry, operating-system
input APIs, and the quality of the demonstration data.

## Evidence boundary

The repository contains source code and dependency metadata only. It does not
retain:

- the original demonstration dataset;
- trained weights or a model card;
- training curves or evaluation seeds;
- a captured end-to-end gameplay run; or
- hardware-normalized latency or frame-rate measurements.

Those omissions mean the code supports an architecture discussion, not a
quantitative performance claim. Reproducing the full experiment requires a
Windows host, a licensed GTA V installation, compatible legacy TensorFlow /
TFLearn dependencies, locally collected demonstrations, and configured model
paths.

## Local validation

The policy contract is intentionally dependency-light:

```bash
python -m pytest tests/test_policy.py -q
python -m compileall -q src
```

The Windows capture, training, and live-control scripts are historical and are
not exercised by the headless test. Their dataset and model paths must be
configured before use.

## Repository map

```text
src/
├── collect_data.py          # capture frames and keyboard labels
├── policy.py                # nine-action encoding contract
├── train_model.py           # historical training loop
├── test_model.py            # live inference and direct control loop
├── models.py                # TFLearn CNN experiments
├── motion.py                # motion-delta recovery signal
└── training/                # AlexNet and dataset-preparation utilities
tests/
└── test_policy.py           # headless action-contract regression tests
```

## Provenance and licensing

This project began from the public
[`Sentdex/pygta5`](https://github.com/Sentdex/pygta5) tutorial lineage and keeps
third-party notices in source files where present. The upstream repository is
MIT licensed; individual retained files may carry additional compatible
notices such as Apache-2.0 or ISC. No new repository-wide license is asserted
here beyond those existing notices.
