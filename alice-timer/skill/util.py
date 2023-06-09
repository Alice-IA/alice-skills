"""Utility functions for the timer skill."""
import re
from datetime import timedelta
from typing import Optional, Tuple

from alice.util.format import pronounce_number
from alice.util.log import LOG
from alice.util.parse import extract_duration, extract_number


def extract_timer_duration(utterance: str) -> Tuple[Optional[timedelta], Optional[str]]:
    """Extract duration in seconds.

    Args:
        utterance: Full request, e.g. "set a 30 second timer"

    Returns
        Number of seconds requested (or None if no duration was extracted) and remainder
        of utterance
    """
    normalized_utterance = _normalize_utterance(utterance)
    extract_result = extract_duration(normalized_utterance)
    if extract_result is None:
        duration = remaining_utterance = None
    else:
        duration, remaining_utterance = extract_result
    if duration is None:
        LOG.info("No duration found in request")
    else:
        LOG.info("Duration of {} found in request".format(duration))

    return duration, remaining_utterance


def _normalize_utterance(utterance: str) -> str:
    """Make the duration of the timer in the utterance consistent for parsing.

    Some STT engines return "30-second timer" not "30 second timer".

    Args:
        utterance: Full request, e.g. "set a 30 second timer"

    Returns:
        The same utterance with any dashes replaced by spaces.

    """
    # TODO: Fix inside parsers
    return utterance.replace("-", " ")


def remove_conjunction(conjunction: str, utterance: str) -> str:
    """Remove the specified conjunction from the utterance.

    For example, remove the " and" left behind from extracting "1 hour" and "30 minutes"
    from "for 1 hour and 30 minutes".  Leaving it behind can confuse other intent
    parsing logic.

    Args:
        conjunction: translated conjunction (like the word "and") to be
            removed from utterance
        utterance: Full request, e.g. "set a 30 second timer"

    Returns:
        The same utterance with any dashes replaced by spaces.

    """
    pattern = r"\s\s{}".format(conjunction)
    remaining_utterance = re.sub(pattern, "", utterance, flags=re.IGNORECASE)

    return remaining_utterance


def extract_ordinal(utterance: str) -> str:
    """Extract ordinal number from the utterance.

    Args:
        utterance: Full request, e.g. "set a 30 second timer"

    Returns:
        An integer representing the numeric value of the ordinal or None if no ordinal
        is found in the utterance.
    """
    ordinal = None
    extracted_number = extract_number(utterance, ordinals=True)
    if type(extracted_number) == int:
        ordinal = extracted_number

    return ordinal


def get_speakable_ordinal(ordinal) -> str:
    """Get speakable ordinal if other timers exist with same duration.

    Args:
        ordinal: if more than one timer exists for the same duration, this value will
            indicate if it is the first, second, etc. instance of the duration.

    Returns:
        The ordinal that can be passed to TTS (i.e. "first", "second")
    """
    return pronounce_number(ordinal, ordinals=True)


def format_timedelta(time_delta: timedelta) -> str:
    """Convert number of seconds into a displayable time string.

    Args:
        time_delta: an amount of time to convert to a displayable string.

    Returns:
        the value to display on a device's screen or faceplate.
    """
    hours = abs(time_delta // timedelta(hours=1))
    minutes = abs((time_delta - timedelta(hours=hours)) // timedelta(minutes=1))
    seconds = abs(
        (time_delta - timedelta(hours=hours) - timedelta(minutes=minutes))
        // timedelta(seconds=1)
    )
    if hours:
        time_elements = [str(hours), str(minutes).zfill(2), str(seconds).zfill(2)]
    else:
        time_elements = [str(minutes).zfill(2), str(seconds).zfill(2)]
    formatted_time_delta = ":".join(time_elements)

    return formatted_time_delta
