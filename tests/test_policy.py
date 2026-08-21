from src.policy import ACTION_LABELS, keys_to_output


def test_each_supported_action_has_one_stable_class() -> None:
    expected = {
        ("W",): 0,
        ("S",): 1,
        ("A",): 2,
        ("D",): 3,
        ("W", "A"): 4,
        ("W", "D"): 5,
        ("S", "A"): 6,
        ("S", "D"): 7,
    }

    for keys, index in expected.items():
        encoded = keys_to_output(keys)
        assert len(encoded) == len(ACTION_LABELS)
        assert sum(encoded) == 1
        assert encoded[index] == 1


def test_unknown_or_empty_input_maps_to_no_key() -> None:
    assert keys_to_output([]) == [0, 0, 0, 0, 0, 0, 0, 0, 1]
    assert keys_to_output(["T"]) == [0, 0, 0, 0, 0, 0, 0, 0, 1]
    assert keys_to_output(["W", "S"]) == [0, 0, 0, 0, 0, 0, 0, 0, 1]

