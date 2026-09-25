# GTA V Vision Driving Agent

[![Headless policy checks](https://github.com/T-Py-T/gta5-vision-driving-agent/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/T-Py-T/gta5-vision-driving-agent/actions/workflows/test.yml?query=branch%3Amain)

A computer-vision driving experiment that learns a nine-action policy from GTA
V screen captures and keyboard demonstrations. The agent observes the game as
pixels, predicts a driving action, sends keyboard input, and uses frame-to-frame
motion to detect when the vehicle may be stuck.

This is a legacy Windows experiment. Its training data and model weights are
not included, so running the full loop requires collecting a local dataset and
configuring a model path.

## Inspectable demo path

There is no hosted driving demo to claim: this repository does not include
trained weights, gameplay recordings, or a retained evaluation run. The
reproducible evidence is deliberately smaller and headless:

1. Run the [policy regression suite](tests/test_policy.py) and Python compilation
   checks without GTA V, TensorFlow, or screen capture.
2. Follow the [Windows workflow](docs/windows-workflow.md) to collect local
   demonstrations, train a model, and review the safety checks before enabling
   keyboard control.
3. Inspect the [architecture below](#how-it-works) and the linked source files
   to trace each stage from pixels to action output.

The workflow is an experiment guide, not a claim of driving performance.

## How it works

```text
Windows screen capture
        │
        ▼
crop, resize, and color conversion
        │
        ├──► frame + keyboard label batches
        │           │
        │           ▼
        │      class balancing
        │           │
        │           ▼
        └──────► CNN training
                    │
                    ▼
             nine action scores
                    │
                    ▼
          keyboard control + motion recovery
```

The action space contains forward, reverse, left, right, the four diagonal
combinations, and no key. [`src/policy.py`](src/policy.py) contains the shared
encoding used by the regression tests.

## Project layout

| Path | Purpose |
| --- | --- |
| [`src/collect_data.py`](src/collect_data.py) | Capture frames and the currently pressed driving keys |
| [`src/policy.py`](src/policy.py) | Convert key combinations into the nine-class one-hot label |
| [`src/training/`](src/training) | Dataset preparation and AlexNet experiments |
| [`src/models.py`](src/models.py) | TFLearn convolutional model definitions |
| [`src/train_model.py`](src/train_model.py) | Train a model from local `.npy` frame batches |
| [`src/test_model.py`](src/test_model.py) | Run model inference and emit keyboard controls |
| [`src/motion.py`](src/motion.py) | Estimate motion from adjacent frames for recovery behavior |
| [`tests/test_policy.py`](tests/test_policy.py) | Headless regression tests for action encoding |

## Setup

Prerequisites for the full experiment:

- Windows with GTA V running in a consistent window or display layout;
- Python 3.11 or 3.12;
- locally collected training data;
- a compatible TensorFlow/TFLearn environment; and
- permission for the process to capture the screen and send keyboard input.

```bash
git clone https://github.com/T-Py-T/gta5-vision-driving-agent.git
cd gta5-vision-driving-agent
uv sync --extra dev
```

Before training, update the dataset path, `MODEL_NAME`, and `PREV_MODEL` values
in [`src/train_model.py`](src/train_model.py). Before live inference, set the
model path and screen dimensions in [`src/test_model.py`](src/test_model.py).

The complete [Windows workflow](docs/windows-workflow.md) lists the files that
still contain machine-specific paths, the order of operations, and the safety
checks to perform before the script can send keyboard input.

The capture and direct-keyboard modules are Windows-specific. Test them in a
safe game session and keep a manual stop key available before enabling the
control loop.

## Collect, train, and run

The historical scripts are intentionally separate so each stage can be
inspected and configured:

```bash
uv run python src/collect_data.py
uv run python src/training/balance_data.py
uv run python src/train_model.py
uv run python src/test_model.py
```

Paths and model settings are defined in the scripts rather than through a
single configuration file. Review them before running a stage; the defaults
reflect the original development machine.

## Local validation

The action contract can be checked without GTA V, TensorFlow, screen capture,
or model files:

```bash
python -m pytest tests/test_policy.py -q
python -m compileall -q src
```

These commands validate the dependency-free policy module and Python syntax.
They do not launch the game or send keyboard input.

The repository does not include a trained model, source gameplay recordings, or
a retained evaluation run. Its durable evidence is the implementation itself
and the headless action-encoding regression suite.

## Licensing

Repository-specific additions are available under the [MIT License](LICENSE).
The project began from the
[`Sentdex/pygta5`](https://github.com/Sentdex/pygta5) tutorial codebase and also
contains files with Apache-2.0 and ISC notices. Those original notices and
terms remain in effect; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Evidence status

> Tip-cite bank: base main `0d7f54c0` + PR #N. Steward resolves after merge; no `READY` claim.

For the active inventory of unresolved evidence boundaries and held decisions, see [docs/OPEN_PROBLEMS.md](docs/OPEN_PROBLEMS.md).

This repository is **NOT READY** for a driving-performance claim. It contains
no trained weights, gameplay recordings, or retained evaluation run. The
headless checks validate policy encoding and Python syntax only; they do not
establish a benchmark score or a `READY` status.
