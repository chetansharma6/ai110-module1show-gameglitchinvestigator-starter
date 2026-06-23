from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)


# ---------------------------------------------------------------------------
# check_guess: the high/low hint bug
#
# Bug: a guess that is too HIGH must tell the player to go LOWER (and vice
# versa). The original code swapped these messages. check_guess returns a
# (outcome, message) tuple, so we assert on both parts.
# ---------------------------------------------------------------------------

def test_check_guess_win():
    assert check_guess(50, 50) == ("Win", "🎉 Correct!")


def test_check_guess_too_high_tells_player_to_go_lower():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message
    assert "HIGHER" not in message


def test_check_guess_too_low_tells_player_to_go_higher():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message
    assert "LOWER" not in message


# ---------------------------------------------------------------------------
# get_range_for_difficulty: the Hard-range bug
#
# Bug: Hard must span 1..200 (it was previously 1..50). Unknown difficulties
# fall back to the Normal range.
# ---------------------------------------------------------------------------

def test_range_easy():
    assert get_range_for_difficulty("Easy") == (1, 20)


def test_range_normal():
    assert get_range_for_difficulty("Normal") == (1, 100)


def test_range_hard_is_1_to_200():
    assert get_range_for_difficulty("Hard") == (1, 200)


def test_range_unknown_defaults_to_normal():
    assert get_range_for_difficulty("Lunatic") == (1, 100)


# ---------------------------------------------------------------------------
# update_score: the off-by-one and bogus-bonus bugs
#
# Bug 1: a win on the first attempt should award the full 100 points.
#        The formula is 100 - 10 * (attempt_number - 1), floored at 10.
# Bug 2: wrong guesses always deduct 5 — there is no even-attempt bonus.
# ---------------------------------------------------------------------------

def test_win_on_first_attempt_awards_full_100():
    assert update_score(0, "Win", 1) == 100


def test_win_points_decay_by_attempt():
    assert update_score(0, "Win", 3) == 80


def test_win_points_floored_at_10():
    # Attempt 20 would compute 100 - 190 = -90, must be clamped to +10.
    assert update_score(0, "Win", 20) == 10


def test_too_high_always_deducts_5_on_even_attempt():
    # Bug: an even attempt number must NOT grant a bonus.
    assert update_score(100, "Too High", 2) == 95


def test_too_high_deducts_5_on_odd_attempt():
    assert update_score(100, "Too High", 3) == 95


def test_too_low_deducts_5():
    assert update_score(100, "Too Low", 4) == 95


def test_unknown_outcome_leaves_score_unchanged():
    assert update_score(42, "Whatever", 1) == 42


# ---------------------------------------------------------------------------
# parse_guess: input-handling bugs
#
# Returns (ok, guess_int, error_message).
# ---------------------------------------------------------------------------

def test_parse_guess_valid_integer():
    assert parse_guess("7") == (True, 7, None)


def test_parse_guess_truncates_decimal():
    ok, value, error = parse_guess("7.9")
    assert ok is True
    assert value == 7
    assert error is None


def test_parse_guess_none_is_rejected():
    ok, value, error = parse_guess(None)
    assert ok is False
    assert value is None
    assert error == "Enter a guess."


def test_parse_guess_empty_string_is_rejected():
    ok, value, error = parse_guess("")
    assert ok is False
    assert value is None
    assert error == "Enter a guess."


def test_parse_guess_non_numeric_is_rejected():
    ok, value, error = parse_guess("abc")
    assert ok is False
    assert value is None
    assert error == "That is not a number."
