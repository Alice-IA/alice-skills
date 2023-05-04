"""Defines a timer object."""
from datetime import timedelta
from typing import Optional

from alice.util.format import nice_duration
from alice.util.time import now_utc
from .util import format_timedelta

BACKGROUND_COLORS = ("#22A7F0", "#40DBB0", "#BDC3C7", "#4DE0FF")


class CountdownTimer:
    """Data attributes that define a timer."""

    _speakable_duration = None

    def __init__(self, duration: timedelta, name: str):
        self.duration = duration
        self.name = name
        self.index = None
        self.expiration = now_utc() + duration
        self.expiration_announced = False
        self.ordinal = 0

    @property
    def expired(self) -> bool:
        """Boolean value representing whether or not the timer has expired."""
        return self.expiration < now_utc()

    @property
    def speakable_duration(self) -> str:
        """Generate a string that can be used to speak the timer's initial duration."""
        if self._speakable_duration is None:
            self._speakable_duration = nice_duration(self.duration)

        return self._speakable_duration

    @property
    def time_remaining(self) -> Optional[timedelta]:
        """The amount of time remaining until the timer expires."""
        if self.expired:
            time_remaining = None
        else:
            time_remaining = self.expiration - now_utc()

        return time_remaining

    @property
    def percent_remaining(self) -> float:
        """The percentage of the timer duration that remains until expiration."""
        if self.expired:
            percent_remaining = None
        else:
            percent_remaining = (
                self.time_remaining.total_seconds() / self.duration.total_seconds()
            )

        return percent_remaining

    @property
    def time_since_expiration(self) -> Optional[timedelta]:
        """The amount of time elapsed since the timer expired."""
        if self.expired:
            time_since_expiration = now_utc() - self.expiration
        else:
            time_since_expiration = None

        return time_since_expiration

    @property
    def display_data(self) -> dict:
        """Build the name/value pairs to be passed to the GUI."""
        color_index = (self.index % 4) - 1
        if self.expired:
            expiration_delta = "-" + format_timedelta(self.time_since_expiration)
        else:
            expiration_delta = format_timedelta(self.time_remaining)

        return dict(
            backgroundColor=BACKGROUND_COLORS[color_index],
            expired=self.expired,
            percentRemaining=self.percent_remaining,
            timerName=self.name,
            timeDelta=expiration_delta,
        )
