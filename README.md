# GTA V Vision Driving Agent

[![Headless policy checks](https://github.com/T-Py-T/gta5-vision-driving-agent/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/T-Py-T/gta5-vision-driving-agent/actions/workflows/test.yml?query=branch%3Amain)

**Watch the game. Copy the keys. Drive with nothing but pixels.**

This is an imitation-learning loop for Grand Theft Auto V that never reads game memory and never calls a mod API. It screenshots the window, learns which of nine keyboard actions you were holding, and later presses those same keys. When the picture stops changing, it assumes the car is stuck and tries to reverse out.

You can run the piece that does not need the game in about a minute. The piece that drives needs Windows, your own copy of GTA V, and a dataset you record yourself. No weights ship here, and no drive has been retained.

<a id="evidence-status"></a>

## No driving result lives in this repository

There is no published score, distance, success rate, or video. The tree has no model weights and no gameplay footage. Training captures are local `.npy` files and are not committed. Nothing in a filename, a comment, or a checkpoint that is not in this tree should be treated as a result, because no evaluation run is retained here.

What you can verify today is the action encoding and that the Python sources parse. That is the demo below. It is not a driving benchmark.

## Why try it

Most driving agents hide behind a simulator API. This one is the opposite experiment: the only sensor is a screen rectangle, and the only actuator is W, A, S, and D. The interesting part is the seam between a nine-class convolutional policy and a hand-written recovery behavior that does not trust the network when the car stops moving.

The code is legacy and rough. It is still a complete loop, and the contract that turns keys into labels is small enough to test with no dependencies.

## Contents

- [How a frame becomes a keypress](#how-a-frame-becomes-a-keypress)
- [The nine actions](#the-nine-actions)
- [Worked example](#worked-example)
- [The demo you can run](#local-validation)
- [Getting started](#getting-started)
- [Windows and GTA V](#windows-and-gta-v)
- [Known rough edges](#known-rough-edges)
- [Contributing](#contributing)
- [License](#license)

## How a frame becomes a keypress

```text
screen region (0, 40) → (1920, 1120)
        │
        ▼
resize to 480×270, BGR → RGB
        │
        ├── recorded with the keys you were holding
        │         │
        │         ▼
        │    last 50 frames of each batch held out
        │         │
        │         ▼
        └── TFLearn Inception-v3, nine outputs
                  │
                  ▼
        scores × a fixed bias, then argmax
                  │
                  ▼
        PressKey / ReleaseKey, plus stuck recovery
```

**Record.** [`src/collect_data.py`](src/collect_data.py) grabs that 1080p region under the title bar, resizes each frame to 480×270, and stores the frame with a nine-class label. Every 500 pairs it writes a `.npy` batch. `T` pauses.

**Label.** [`src/policy.py`](src/policy.py) is dependency-free. Unsupported combinations, including W and S together, become `no-key`, so a label always has exactly one `1`.

**Train.** [`src/train_model.py`](src/train_model.py) walks local batches, holds out the last 50 frames of each file, and fits the TFLearn Inception-v3 alias of `inception_v3` in [`src/models.py`](src/models.py). That file still contains thirteen architecture functions (AlexNet, ResNeXt, Inception-v3 in 2D and 3D, an LSTM variant, and several sentnet nets). [`src/xception.py`](src/xception.py) is a separate Keras experiment and is not what the drive script loads.

**Drive.** [`src/test_model.py`](src/test_model.py) predicts, then scales the nine scores before the argmax:

```python
prediction = np.array(prediction) * np.array([4.5, 0.1, 0.1, 0.1, 1.8, 1.8, 0.5, 0.5, 0.2])
```

Forward is multiplied by 4.5, the two forward diagonals by 1.8, and reverse and the pure turns by 0.1. That vector is a hand-tuned correction, not something the network learned.

**Recover.** [`src/motion.py`](src/motion.py) counts pixels that changed. The drive loop keeps the last 25 counts and, when their average drops below 800, runs a short reverse-and-turn escape. That path is currently broken by a name error described under [Known rough edges](#known-rough-edges).

## The nine actions

| Index | Action | Keys |
| --- | --- | --- |
| 0 | `forward` | W |
| 1 | `reverse` | S |
| 2 | `left` | A |
| 3 | `right` | D |
| 4 | `forward-left` | W + A |
| 5 | `forward-right` | W + D |
| 6 | `reverse-left` | S + A |
| 7 | `reverse-right` | S + D |
| 8 | `no-key` | — |

A model trained against a different order will press the wrong keys. The tests exist to stop that from drifting.

## Worked example

From the repository root, with Python 3.11 or 3.12 and no third-party packages:

```python
from src.policy import ACTION_LABELS, keys_to_output

ACTION_LABELS
# ('forward', 'reverse', 'left', 'right', 'forward-left',
#  'forward-right', 'reverse-left', 'reverse-right', 'no-key')

keys_to_output(["W", "D"])   # accelerate through a right turn
# [0, 0, 0, 0, 0, 1, 0, 0, 0]

keys_to_output(["W", "S"])   # gas and brake together is not a class
# [0, 0, 0, 0, 0, 0, 0, 0, 1]
```

That vector is the training target for a frame, and it is the order `test_model.py` reads back out of the network.

<a id="local-validation"></a>

## The demo you can run

This is the headless path. It does not launch GTA V, import TensorFlow, capture the screen, or send a key.

```bash
python -m pytest tests/test_policy.py -q
python -m compileall -q src
```

Use Python 3.11 or 3.12. [`pyproject.toml`](pyproject.toml) requires `>=3.11,<3.13`. [CI](.github/workflows/test.yml) installs `pytest==8.4.2` on Python 3.11 and runs those two commands on pull requests. A clean run looks like this:

```text
..                                                                       [100%]
2 passed in 0.01s
```

`compileall` prints nothing when every file under `src/` parses.

There is no screenshot in this repository, so there is nothing to show for a drive. If you want to see the car move, that only happens on the Windows path below, and only after you record data and train a model that this tree does not contain.

## Getting started

```bash
git clone https://github.com/T-Py-T/gta5-vision-driving-agent.git
cd gta5-vision-driving-agent
python -m pytest tests/test_policy.py -q
```

The policy module imports nothing outside the standard library. The rest of the project declares TensorFlow, TFLearn, OpenCV, NumPy, pandas, and pynput:

```bash
uv sync --extra dev
```

That install was not executed while writing this page. TFLearn is unmaintained, and whether it imports on a current TensorFlow wheel depends on the Python version you pin. Treat a successful import as something you have to confirm locally, then keep the lockfile.

## Windows and GTA V

**Not run from this checkout.** Capture and keyboard control import `win32gui`, `win32ui`, `win32con`, and `win32api`. They will not start on macOS or Linux. You also need a legally obtained copy of GTA V and a display. This repository ships neither.

The scripts are separate, and the paths and model names are constants inside them. Read each file before you run it.

```powershell
uv run python src/collect_data.py
uv run python src/training/balance_data.py
uv run python src/train_model.py
uv run python src/test_model.py
```

Before recording, match the capture region to your window. Before training, set `MODEL_NAME`, `PREV_MODEL`, and the dataset directory in `train_model.py`. Before driving, set `MODEL_NAME` in `test_model.py` to a checkpoint you produced. Both names are currently empty strings, and `train_model.py` still has `LOAD_MODEL = True`, so it tries to load that empty name immediately.

`test_model.py` sends virtual key events to whatever window is focused. If GTA V loses focus, the agent types into something else. Use a windowed session, start somewhere harmless, confirm `T` pauses, and keep a way to kill the process.

More of the same path is in [`docs/windows-workflow.md`](docs/windows-workflow.md).

## Known rough edges

Left as they are, on purpose. They are documented so the next person does not have to rediscover them.

- **Hard-coded drives.** The first 500-frame batch in `collect_data.py` is written to a relative `training_data-N.npy` in the working directory. Every batch after that goes to `X:/pygta5/phase7-larger-color/`. `train_model.py` reads `J:/phase10-random-padded/training_data-{i}.npy` for `i` in `1..1860` (`FILE_I_END`). Those letters are from the original machine.
- **Empty model names.** `MODEL_NAME` and `PREV_MODEL` are `''` in both `train_model.py` and `test_model.py`.
- **NameError on the stuck-car path.** `test_model.py` assigns `delta_count_last`, then appends `delta_count`, which is never defined. Recovery raises `NameError` until those names are reconciled. Product code is intentionally not changed here.
- **Three-class leftovers.** [`src/training/create_training_data.py`](src/training/create_training_data.py) still captures an 800×600 region, converts to grayscale, resizes to 160×120, and emits a three-class `[A, W, D]` vector. [`src/training/balance_data.py`](src/training/balance_data.py) still balances left / forward / right. Neither matches the nine-class 480×270 pipeline.
- **Imports the project file does not cover.** `train_model.py` imports `tqdm`, which is not listed in `pyproject.toml`. `otherception3` in `models.py` calls `tf.device` without importing TensorFlow.

## Contributing

Issues and pull requests are welcome. Branch from `main`, keep one concern per pull request, and run the two headless commands before opening it. Do not commit datasets, weights, or screen recordings. Do not add a driving score unless the run that produced it is committed with it.

Details are in [`CONTRIBUTING.md`](CONTRIBUTING.md). Also see [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md), [`SECURITY.md`](SECURITY.md), and [`SUPPORT.md`](SUPPORT.md).

## License

Repository-specific additions are [MIT](LICENSE).

This project started from the [`Sentdex/pygta5`](https://github.com/Sentdex/pygta5) tutorial code. `src/models.py` keeps Google's Apache-2.0 notice, and `src/motion.py` keeps Noah Spurrier's ISC-style notice. The MIT license does not relicense those files. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Not affiliated with or endorsed by Rockstar Games. No game assets are included. You need your own copy of GTA V.

| Also in the tree | |
| --- | --- |
| [docs/windows-workflow.md](docs/windows-workflow.md) | Windows experiment notes |
| [docs/OPEN_PROBLEMS.md](docs/OPEN_PROBLEMS.md) | Why no result is published |
| [ROADMAP.md](ROADMAP.md) | Planned work |
| [CHANGELOG.md](CHANGELOG.md) | Merged changes on `main` |
