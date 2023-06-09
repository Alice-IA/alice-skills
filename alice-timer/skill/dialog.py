"""Determine what the spoken response to a users timer request should be."""
from alice.util.format import nice_duration
from .util import get_speakable_ordinal

SINGLE_UNNAMED_TIMER_NAME = "Timer"


class TimerDialog:
    """Use information about a timer to determine what dialog should be spoken."""

    def __init__(self, timer, language):
        self.timer = timer
        self.language = language
        self.name = None
        self.data = None

    def build_add_dialog(self, timer_count: int):
        """Build the dialog to confirm the addition of a new timer.

        If there are multiple timers, speak the name of the timer as well for clarity.

        Args:
            timer_count: number of active timers
        """
        self.name = "started-timer"
        self.data = dict(duration=self.timer.speakable_duration)
        if timer_count > 1 or self.timer.name != "Timer":
            self.name += "-named"
            self.data.update(name=self.timer.name)
            self._check_for_ordinal()

    def build_status_dialog(self):
        """Build dialog for communicating the status of active timers."""
        if self.timer.expired:
            self.name = "time-elapsed"
            self.data = dict(
                time_diff=nice_duration(self.timer.time_since_expiration.seconds)
            )
        else:
            self.name = "time-remaining"
            self.data = dict(
                time_diff=nice_duration(self.timer.time_remaining.seconds)
            )
        self._check_for_named_timer()
        self._check_for_ordinal()
        self.data.update(duration=self.timer.speakable_duration)

    def build_details_dialog(self):
        """Build dialog used when asking a user which timer to select."""
        self.name = "timer-details"
        self.data = dict(duration=self.timer.speakable_duration)
        self._check_for_named_timer()
        self._check_for_ordinal()

    def build_cancel_dialog(self):
        """Build dialog used to confirm the cancellation of a timer."""
        self.name = "cancelled-timer"
        self.data = dict(duration=self.timer.speakable_duration)
        self._check_for_named_timer()
        self._check_for_ordinal()

    def build_cancel_confirm_dialog(self):
        """Build dialog used to confirm which timer will be cancelled."""
        self.name = "confirm-timer-to-cancel"
        timer_name = self.timer.name or self.timer.speakable_duration
        self.data = dict(name=timer_name)

    def build_expiration_announcement_dialog(self, timer_count: int):
        """Build dialog used to announce that a timer has expired."""
        self.name = "timer-expired"
        self.data = dict(duration=self.timer.speakable_duration)
        if timer_count > 1:
            self.name += "-named"
            self.data.update(name=self.timer.name)
            self._check_for_ordinal()

    def _check_for_named_timer(self):
        """Add the timer name to the dialog data, if one is available.

        Timers are assigned names if the user does not specify one.  The only time the
        timer name would not be included is when a single unnamed timer is active.
        """
        if self.timer.name != SINGLE_UNNAMED_TIMER_NAME:
            self.name += "-named"
            self.data.update(name=self.timer.name)

    def _check_for_ordinal(self):
        """Add the timer's ordinal value if one is available.

        This would occur if there are multiple timers with the same starting duration.
        """
        if self.timer.ordinal > 1:
            self.name += "-ordinal"
            speakable_ordinal = get_speakable_ordinal(self.timer.ordinal)
            self.data.update(ordinal=speakable_ordinal)
