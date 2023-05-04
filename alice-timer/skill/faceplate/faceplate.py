"""Manage what is displayed on the faceplate of the Mark I for the timer skill."""
from pathlib import Path

CHARACTER_WIDTH = 3
COLON_WIDTH = 2
HYPHEN_WIDTH = 2
FACEPLATE_WIDTH = 32
TIMER_INDEX_WIDTH = 6
SPACING = 1


class FaceplateRenderer:
    """Render timer information on the Mark I display."""

    def __init__(self, enclosure, timer):
        self.enclosure = enclosure
        self.timer_index = timer.index
        self.timer_display = timer.display_data["timeDelta"]
        self.multiple_active_timers = False
        self.character_directory = Path(__file__).parent.joinpath("characters")
        self.x_coordinate = 0
        self.y_coordinate = 2

    def render(self):
        """Main function to render a timer on the faceplate."""
        if self.multiple_active_timers:
            self._render_timer_index()
        self._calculate_timer_x_coordinate()
        for character in self.timer_display:
            self._render_character(character)

    def _render_timer_index(self):
        """If there are multiple timers, display a numeric identifier."""
        self.x_coordinate += SPACING
        self._render_character(str(self.timer_index))

    def _calculate_timer_x_coordinate(self):
        """Determine where on the faceplate to start the timer display."""
        timer_width = 0
        for character in self.timer_display:
            if character == ":":
                timer_width += COLON_WIDTH
            elif character == "-":
                timer_width = HYPHEN_WIDTH + SPACING
            else:
                timer_width += CHARACTER_WIDTH + SPACING
        timer_width -= 1
        self.x_coordinate += (FACEPLATE_WIDTH - timer_width) // 2

    def _render_character(self, character):
        """Render a single character on the display and advance the x-coordinate."""
        if character == ":":
            file_name = "colon.png"
            character_width = COLON_WIDTH
        elif character == "-":
            file_name = "negative.png"
            character_width = HYPHEN_WIDTH + SPACING
        else:
            file_name = character + ".png"
            character_width = CHARACTER_WIDTH + SPACING
        path = self.character_directory.joinpath(file_name)
        self.enclosure.mouth_display_png(
            str(path), x=self.x_coordinate, y=self.y_coordinate, refresh=False
        )
        self.x_coordinate += character_width
