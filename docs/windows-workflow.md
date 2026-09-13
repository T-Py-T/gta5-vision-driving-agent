# Windows experiment workflow

The full vision-driving loop must run on Windows because it captures a desktop
region and emits virtual key events. Work through the stages separately; do not
start live control until capture geometry and the pause control have been
checked in a safe game session.

## 1. Prepare the environment

Use Python 3.9 through 3.12 and install the project with its development tools:

```powershell
git clone https://github.com/T-Py-T/gta5-vision-driving-agent.git
Set-Location gta5-vision-driving-agent
uv sync --extra dev
uv run pytest tests/test_policy.py -q
```

TensorFlow and TFLearn compatibility can vary by Python version. Preserve a
working lockfile and environment once the historical model stack imports
successfully.

## 2. Check capture geometry

The original scripts assume a 1920 by 1080 game view and crop the desktop from
`(0, 40)` to `(1920, 1120)`. Update these values for the current monitor and
window layout before collecting data:

- [`src/collect_data.py`](../src/collect_data.py): capture region and output
  batch path
- [`src/test_model.py`](../src/test_model.py): `GAME_WIDTH`, `GAME_HEIGHT`, and
  capture region

Use a windowed game session first. Confirm that the captured frame contains the
road view and no private desktop content before saving a batch.

## 3. Collect demonstrations

```powershell
uv run python src/collect_data.py
```

The collector labels each frame from the currently pressed W, A, S, and D keys.
Press `T` to pause or resume collection. Each batch contains 500 frame-label
pairs in a NumPy file. Store these files outside Git; gameplay captures may be
large and can contain on-screen personal information.

## 4. Balance and train

Update the input glob in the balancing script and the data, model, and checkpoint
paths in [`src/train_model.py`](../src/train_model.py), then run:

```powershell
uv run python src/training/balance_data.py
uv run python src/train_model.py
```

Keep the nine output classes in the same order as
[`src/policy.py`](../src/policy.py). A model trained against a different label
order will send the wrong controls.

## 5. Run live inference

Set `MODEL_NAME` in [`src/test_model.py`](../src/test_model.py) to a compatible
trained checkpoint. Start GTA V in the tested window layout, keep the window in
focus, and leave a safe area in the game before running:

```powershell
uv run python src/test_model.py
```

Press `T` to pause the loop. Be prepared to terminate the Python process if the
game loses focus or the pause key is not detected. The script can issue W, A, S,
and D events to whichever window receives them.

## What the headless tests cover

`tests/test_policy.py` verifies the one-hot action encoding for straight,
reverse, turns, diagonals, unsupported combinations, and no-key input. It does
not validate screen capture, TensorFlow/TFLearn compatibility, checkpoint
quality, driving performance, or keyboard delivery.
