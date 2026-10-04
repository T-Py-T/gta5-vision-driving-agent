# GTA V Vision Driving Agent

[![Headless policy checks](https://github.com/T-Py-T/gta5-vision-driving-agent/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/T-Py-T/gta5-vision-driving-agent/actions/workflows/test.yml?query=branch%3Amain)

**Teach a car to drive in Grand Theft Auto V by watching you play it.**

The agent screenshots the game window, feeds the pixels to a convolutional
network, picks one of nine keyboard actions, and presses the keys. When the
picture stops changing for long enough, it assumes the car is wedged against
something and reverses out.

No game API, no memory reading, no mod. It sees the same screen you do and
presses the same four keys you would.

<a id="evidence-status"></a>

## Status: no driving result is published here

**There is no published number for how well this drives.** No score, no success
rate, no distance, no video. This repository has never retained an evaluation
run, and nothing in the tree should be read as one.

What is missing, concretely: the training data (local `.npy` captures, never
committed), the trained weights, any gameplay recording, and any record of a
measured drive. What is here is the implementation and a small headless test
suite that checks the action encoding.

If you are looking for a benchmark, this is not that. If you want to see how an
imitation-learning driving loop was wired together end to end, keep reading.

## Contents

- [How it works](#how-it-works)
- [The nine actions](#the-nine-actions)
- [Getting started](#getting-started)
- [Local validation](#local-validation)
- [Running the full loop on Windows](#running-the-full-loop-on-windows)
- [Project layout](#project-layout)
- [Known rough edges](#known-rough-edges)
- [Contributing](#contributing)
- [License](#license)

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

**Capture.** [`src/collect_data.py`](src/collect_data.py) grabs the desktop
region `(0, 40)` to `(1920, 1120)` — a 1080p game view below the title bar —
converts BGR to RGB, and downsizes each frame to 480×270. Every frame is paired
with whichever of W, A, S, and D you were holding at that instant. Batches of
500 frame-label pairs are written out as NumPy `.npy` files. `T` pauses and
resumes.

**Label.** [`src/policy.py`](src/policy.py) turns a set of pressed keys into a
nine-class one-hot vector. It is deliberately dependency-free so the encoding
can be tested without TensorFlow, OpenCV, or a game.

**Train.** [`src/train_model.py`](src/train_model.py) loads the `.npy` batches,
holds out the last 50 frames of each as validation, and fits a TFLearn
Inception-v3 from [`src/models.py`](src/models.py). That file carries thirteen
architecture variants accumulated over the project — AlexNet, ResNeXt,
Inception-v3 in 2D and 3D, an LSTM variant, and several custom "sentnet" nets.
[`src/xception.py`](src/xception.py) is a separate Keras Xception experiment.

**Drive.** [`src/test_model.py`](src/test_model.py) runs the same capture loop,
predicts, and scales the nine raw scores by a hand-tuned bias vector before
taking the argmax:

```python
prediction = np.array(prediction) * np.array([4.5, 0.1, 0.1, 0.1, 1.8, 1.8, 0.5, 0.5, 0.2])
```

Forward is boosted 4.5×, the forward diagonals 1.8×, and reverse and the pure
turns are damped to 0.1 — a hand-tuned correction sitting between the network
and the keyboard. The winning action becomes a set of `PressKey`/`ReleaseKey`
calls.

**Recover.** [`src/motion.py`](src/motion.py) measures how many pixels changed
between frames using `cv2.absdiff` and a threshold. `test_model.py` keeps a
rolling window of the last 25 of those counts; when the average drops below
800, it declares the car stuck and runs one of four randomized escape
maneuvers — reverse, then turn out — for one to two seconds each.

## The nine actions

Every prediction collapses to exactly one of these. Unsupported combinations
(`W`+`S`, or a non-driving key) fall through to `no-key`, so a label always has
exactly one active class.

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

## Getting started

What you need depends on how far you want to go.

**To read the code and run the tests:** Python 3.11 or 3.12 and nothing else.
The policy module and its tests have no third-party imports.

**To train or drive:** all of the above, plus a Windows machine, a legally
obtained copy of GTA V, a display to capture, a TensorFlow/TFLearn environment
the legacy model code still imports under, and a dataset you record yourself.
None of those last four ship with this repository and none can be substituted.
The capture and keyboard modules import `win32gui`, `win32ui`, `win32con`, and
`win32api`; they will not run on Linux or macOS.

```bash
git clone https://github.com/T-Py-T/gta5-vision-driving-agent.git
cd gta5-vision-driving-agent
```

The full dependency set — TensorFlow, TFLearn, OpenCV, NumPy, pandas, pynput —
installs with [uv](https://docs.astral.sh/uv/):

```bash
uv sync --extra dev
```

Expect friction here. TFLearn is unmaintained and its compatibility with modern
TensorFlow varies by Python version. Once a combination imports successfully,
keep the lockfile.

<a id="local-validation"></a>

## Local validation

You can verify the part of this project that does not need a game. From a fresh
clone, with no dependencies installed:

```bash
python -m pytest tests/test_policy.py -q
python -m compileall -q src
```

The first command checks the action encoding; the second checks that every
source file parses. This is exactly what
[CI](.github/workflows/test.yml) runs on every pull request, and on a clean
checkout it looks like this:

```console
$ python -m pytest tests/test_policy.py -q
..                                                                       [100%]
2 passed in 0.01s
```

Neither command launches GTA V, imports TensorFlow, captures the screen, or
sends a keystroke.

### A real example

The label encoder is the one piece you can exercise directly. Start `python`
from the repository root:

```python
>>> from src.policy import ACTION_LABELS, keys_to_output
>>> ACTION_LABELS
('forward', 'reverse', 'left', 'right', 'forward-left', 'forward-right', 'reverse-left', 'reverse-right', 'no-key')
>>> keys_to_output(["W", "D"])        # accelerating into a right turn
[0, 0, 0, 0, 0, 1, 0, 0, 0]
>>> keys_to_output(["W", "S"])        # gas and brake together -> no-key
[0, 0, 0, 0, 0, 0, 0, 0, 1]
```

That one-hot vector is the training target for a frame, and the same ordering
is what `test_model.py` reads back out of the network. A model trained against
a different label order will send the wrong controls.

## Running the full loop on Windows

Each stage is a separate script, run in order. Paths and model names live
inside the scripts rather than in a config file, so read each one before you run
it.

```powershell
uv run python src/collect_data.py          # record demonstrations
uv run python src/training/balance_data.py # even out the class distribution
uv run python src/train_model.py           # fit a model on your .npy batches
uv run python src/test_model.py            # let it drive
```

Before the first run, set the capture region in `collect_data.py` and the
`GAME_WIDTH`, `GAME_HEIGHT`, and region values in `test_model.py` to match your
monitor and window layout. Before training, set the dataset path, `MODEL_NAME`,
and `PREV_MODEL` in `train_model.py`. Before driving, point `MODEL_NAME` in
`test_model.py` at a checkpoint.

A safety note that is not boilerplate: `test_model.py` emits virtual key events
to whatever window has focus. If GTA V loses focus mid-run, your agent starts
typing W, A, S, and D into something else. Start in a windowed session, park the
car somewhere harmless, confirm the `T` pause key registers, and keep the
terminal in reach to kill the process.

[`docs/windows-workflow.md`](docs/windows-workflow.md) walks the same path in
more detail, including which files still hold machine-specific values.

## Project layout

| Path | Purpose |
| --- | --- |
| [`src/collect_data.py`](src/collect_data.py) | Capture frames and the currently pressed driving keys |
| [`src/policy.py`](src/policy.py) | Convert key combinations into the nine-class one-hot label |
| [`src/grabscreen.py`](src/grabscreen.py) | Windows desktop region capture |
| [`src/getkeys.py`](src/getkeys.py) | Poll which keys are held |
| [`src/directkeys.py`](src/directkeys.py), [`src/keys.py`](src/keys.py) | Send virtual key events to the game |
| [`src/models.py`](src/models.py) | Thirteen TFLearn convolutional architectures |
| [`src/xception.py`](src/xception.py) | Separate Keras Xception experiment |
| [`src/train_model.py`](src/train_model.py) | Train from local `.npy` frame batches |
| [`src/test_model.py`](src/test_model.py) | Run inference and emit keyboard controls |
| [`src/motion.py`](src/motion.py) | Frame-difference motion estimate used for stuck detection |
| [`src/weighting_class_distributor.py`](src/weighting_class_distributor.py) | Sweep per-class output weights against a local validation set (inputs not in repo) |
| [`src/training/`](src/training) | Earlier three-class data prep and AlexNet experiments |
| [`tests/test_policy.py`](tests/test_policy.py) | Headless regression tests for action encoding |

## Known rough edges

This is a legacy codebase preserved as it was, not a maintained package. Known
issues, so you do not have to find them yourself:

- **Hard-coded drive letters.** `collect_data.py` rolls batches onto
  `X:/pygta5/phase7-larger-color/`, and `train_model.py` reads from
  `J:/phase10-random-padded/`. Both are from the original development machine.
- **Empty model names.** `MODEL_NAME` and `PREV_MODEL` are `''` in
  `train_model.py` and `test_model.py`. They must be filled in before either
  script will load or save anything.
- **A live NameError in the drive loop.** `test_model.py` assigns
  `delta_count_last` but later appends `delta_count`, which is never defined.
  The stuck-detection path will raise until that is reconciled.
- **Two generations of code in one tree.** `src/training/create_training_data.py`
  (160×120 grayscale) and `src/training/balance_data.py` both still encode the
  earlier three-class left / forward / right label set. Neither matches the
  nine-class 480×270 pipeline, so the balancing step needs adapting before use.
- **Undeclared imports.** `train_model.py` imports `tqdm`, which is not in
  `pyproject.toml`. `otherception3` in `models.py` calls `tf.device` without
  importing TensorFlow.

## Contributing

Issues and pull requests are welcome, especially ones that keep this runnable
for the next person who finds it. [`CONTRIBUTING.md`](CONTRIBUTING.md) has the
workflow; the short version:

- One concern per pull request, branched from `main`.
- Run `python -m pytest tests/test_policy.py -q` and `python -m compileall -q src`
  before you open it.
- Never commit datasets, model weights, or gameplay captures. Screen recordings
  of a desktop can contain more than the game.
- Do not add a driving score, success rate, or benchmark to the docs unless the
  run that produced it is committed alongside it.

See also [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md),
[`SECURITY.md`](SECURITY.md), and [`SUPPORT.md`](SUPPORT.md).

## License

Repository-specific additions are under the [MIT License](LICENSE).

This project began from the [`Sentdex/pygta5`](https://github.com/Sentdex/pygta5)
tutorial codebase and retains files under other terms: `src/models.py` carries
Google's Apache-2.0 notice, and `src/motion.py` carries Noah Spurrier's
ISC-style notice. Those terms remain in effect — the MIT license does not
relicense them. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

This project is not affiliated with or endorsed by Rockstar Games, and it ships
no game assets. You need your own copy of GTA V.

## More documentation

| Document | What it covers |
| --- | --- |
| [docs/windows-workflow.md](docs/windows-workflow.md) | Stage-by-stage Windows experiment guide |
| [docs/OPEN_PROBLEMS.md](docs/OPEN_PROBLEMS.md) | What is unresolved and why no result is published |
| [ROADMAP.md](ROADMAP.md) | Planned work |
| [CHANGELOG.md](CHANGELOG.md) | Record of merged changes on `main` |
| [CITATION.cff](CITATION.cff) | Citation metadata |
