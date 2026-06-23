# FIX: Refactored this function out of app.py into logic_utils.py with the agent.
def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""

    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    # FIX: agent confirmed Hard range should be 1..200 (was broken at 1..50).
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


# FIX: Refactored out of app.py with the agent; handles None/empty/decimal/non-numeric input.
def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


# FIX: Moved here from app.py with the agent; corrected the inverted hint bug we found together.
def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    # FIX: hints now point the right way (too high -> LOWER, too low -> HIGHER).
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"


# FIX: Refactored out of app.py with the agent and corrected the scoring bugs we traced.
def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""

    if outcome == "Win":
        # FIX: off-by-one corrected (attempt_number - 1) so a 1st-attempt win scores 100.
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    # FIX: removed the bogus even-attempt bonus; wrong guesses always deduct 5.
    if outcome == "Too High":
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
