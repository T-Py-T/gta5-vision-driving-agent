"""Dependency-free action encoding for the GTA V driving experiment."""

from __future__ import annotations

ACTION_LABELS = (
    "forward",
    "reverse",
    "left",
    "right",
    "forward-left",
    "forward-right",
    "reverse-left",
    "reverse-right",
    "no-key",
)

_KEY_TO_INDEX = {
    frozenset({"W"}): 0,
    frozenset({"S"}): 1,
    frozenset({"A"}): 2,
    frozenset({"D"}): 3,
    frozenset({"W", "A"}): 4,
    frozenset({"W", "D"}): 5,
    frozenset({"S", "A"}): 6,
    frozenset({"S", "D"}): 7,
}


def keys_to_output(keys: list[str] | set[str] | tuple[str, ...]) -> list[int]:
    """Encode pressed driving keys as the experiment's nine-class one-hot vector.

    Non-driving keys are ignored. Unsupported combinations intentionally map to
    ``no-key`` so the label always has exactly one active class.
    """

    driving_keys = frozenset(key.upper() for key in keys if key.upper() in "WASD")
    action_index = _KEY_TO_INDEX.get(driving_keys, len(ACTION_LABELS) - 1)
    output = [0] * len(ACTION_LABELS)
    output[action_index] = 1
    return output

