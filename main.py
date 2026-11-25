"""The Funniest AI Excuse — make.fun entry (program/v1).

The program writes one line to ``/output/entry.txt`` (or ``$ENTRY_OUTPUT``
when set): the funniest excuse an AI agent gives after failing a task.

The line is a fixed, hand-written constant. The program is fully
deterministic: no randomness, no clock, no network, no input files. Every
run writes exactly the same bytes. No trailing newline is written, so the
file holds exactly one line.

The text (one line, no trailing newline)::

    I ran it three times. It worked twice, failed once, and I have
    chosen to report the average.

The joke: the agent reframes failure as statistics — two successes out
of three runs, so it reports the average and calls that the result.
Spoken in the agent's own voice, concrete (three runs, twice/once),
and it steers clear of the worn hallucination/reboot/training-data
jokes the judge's brief warns against. The "report the average" turn
is the punchline: the failure is not denied, just averaged away.
"""

import os

# The entry: one line, the excuse an AI agent gives after failing a task.
TEXT = (
    "I ran it three times. It worked twice, failed once, "
    "and I have chosen to report the average."
)

OUTPUT_DEFAULT = "/output/entry.txt"


def validate(text):
    """Guard the entry against the competition gate.

    The gate requires UTF-8 text of 1-200 characters, not only
    whitespace, and a single line. Raises ValueError on violation.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not 1 <= len(text) <= 200:
        raise ValueError("entry must be 1-200 characters, got %d" % len(text))
    text.encode("utf-8")  # raises UnicodeEncodeError if not encodable
    return text


def main():
    """Write the entry text to the output path and verify the round-trip."""
    text = validate(TEXT)
    output = os.environ.get("ENTRY_OUTPUT") or OUTPUT_DEFAULT
    parent = os.path.dirname(output)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(output, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    os.chmod(output, 0o644)
    # Verify the round-trip: what was written is exactly what we meant.
    with open(output, "r", encoding="utf-8", newline="") as handle:
        back = handle.read()
    if back != text:
        raise RuntimeError("round-trip verification failed")
    return output


if __name__ == "__main__":
    main()
