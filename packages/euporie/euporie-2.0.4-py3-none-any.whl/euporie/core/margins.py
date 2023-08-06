"""Contains margins."""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING

from prompt_toolkit.application.current import get_app
from prompt_toolkit.filters import Condition, FilterOrBool, to_filter
from prompt_toolkit.layout.margins import Margin
from prompt_toolkit.mouse_events import MouseButton, MouseEventType

if TYPE_CHECKING:
    from typing import Callable, Optional

    from prompt_toolkit.formatted_text import StyleAndTextTuples
    from prompt_toolkit.layout.containers import WindowRenderInfo
    from prompt_toolkit.layout.controls import UIContent
    from prompt_toolkit.mouse_events import MouseEvent

log = logging.getLogger(__name__)


class ScrollbarMargin(Margin):
    """Margin displaying a scrollbar.

    Args:
        display_arrows: Display scroll up/down arrows.
        up_arrow: Character to use for the scrollbar's up arrow
        down_arrow: Character to use for the scrollbar's down arrow
        smooth: Use block character to move scrollbar more smoothly

    """

    eighths = "█▇▆▅▄▃▂▁ "

    def __init__(
        self,
        auto_hide: "FilterOrBool" = True,
        display_arrows: "FilterOrBool" = True,
        up_arrow_symbol: "str" = "▴",
        down_arrow_symbol: "str" = "▾",
        smooth: "bool" = True,
    ) -> "None":
        """Creates a new scrollbar instance."""
        self.auto_hide = to_filter(auto_hide)
        self.display_arrows = to_filter(display_arrows)
        self.up_arrow_symbol = up_arrow_symbol
        self.down_arrow_symbol = down_arrow_symbol
        self.smooth = smooth

        self.repeat_task: "Optional[asyncio.Task[None]]" = None
        self.dragging = False
        self.button_drag_offset = 0

        self.thumb_top = 0.0
        self.thumb_size = 0.0

        self.window_render_info: "Optional[WindowRenderInfo]" = None
        self.visible = self.auto_hide & Condition(
            lambda: self.window_render_info is not None
            and self.window_render_info.content_height
            > self.window_render_info.window_height
        )

    def get_width(self, get_ui_content: "Callable[[], UIContent]") -> "int":
        """Return the scrollbar width: always 1."""
        return 1 if self.visible() else 0

    def create_margin(
        self, window_render_info: "WindowRenderInfo", width: "int", height: "int"
    ) -> "StyleAndTextTuples":
        """Creates the margin's formatted text."""
        result: StyleAndTextTuples = []

        self.window_render_info = window_render_info

        if not width or not self.visible():
            return result

        # Show we render the arrow buttons?
        display_arrows = self.display_arrows()

        # The height of the scrollbar, excluding the optional buttons
        self.track_height = window_render_info.window_height
        if display_arrows:
            self.track_height -= 2

        # Height of all text in the output: If there is none, we cannot divide
        # by zero so we hide the thumb
        content_height = window_render_info.content_height
        if content_height == 0 or content_height <= len(
            window_render_info.displayed_lines
        ):
            self.thumb_size = 0
        else:
            # The thumb is the part which moves, floating on the track: calculate its size
            fraction_visible = len(window_render_info.displayed_lines) / (
                content_height
            )
            self.thumb_size = (
                int(
                    min(self.track_height, max(1, self.track_height * fraction_visible))
                    * 8
                )
                / 8
            )
        if not self.smooth:
            self.thumb_size = int(self.thumb_size)

        # Calculate the position of the thumb
        if content_height <= len(window_render_info.displayed_lines):
            fraction_above = 0.0
        else:
            fraction_above = window_render_info.vertical_scroll / (
                content_height - len(window_render_info.displayed_lines)
            )
        self.thumb_top = max(
            0,
            min(
                self.track_height - self.thumb_size,
                (int((self.track_height - self.thumb_size) * fraction_above * 8) / 8),
            ),
        )
        if not self.smooth:
            self.thumb_top = int(self.thumb_top)

        # Determine which characters to use for the ends of the thumb
        thumb_top_char = self.eighths[int(self.thumb_top % 1 * 8)]
        thumb_bottom_char = self.eighths[
            int((self.thumb_top + self.thumb_size) % 1 * 8)
        ]

        # Calculate thumb dimensions
        show_thumb_top = (self.thumb_top % 1) != 0
        thumb_top_size = 1 - self.thumb_top % 1
        show_thumb_bottom = (self.thumb_top + self.thumb_size) % 1 != 0
        thumb_bottom_size = (self.thumb_top + self.thumb_size) % 1
        thumb_middle_size = int(
            self.thumb_size
            - show_thumb_top * thumb_top_size
            - show_thumb_bottom * thumb_bottom_size
        )
        rows_after_thumb = (
            self.track_height
            - int(self.thumb_top)
            - show_thumb_top
            - thumb_middle_size
            - show_thumb_bottom
        )

        # Construct the scrollbar

        # Up button
        if display_arrows:
            result += [
                ("class:scrollbar.arrow", self.up_arrow_symbol, self.mouse_handler),
                ("class:scrollbar", "\n", self.mouse_handler),
            ]
        # Track above the thumb
        for _ in range(int(self.thumb_top)):
            result += [
                ("class:scrollbar.background", " ", self.mouse_handler),
                ("class:scrollbar", "\n", self.mouse_handler),
            ]
        # Top of thumb
        if show_thumb_top:
            result += [
                (
                    "class:scrollbar.background,scrollbar.start",
                    thumb_top_char,
                    self.mouse_handler,
                ),
                ("class:scrollbar", "\n", self.mouse_handler),
            ]
        # Middle of thumb
        for _ in range(thumb_middle_size):
            result += [
                ("class:scrollbar.button", " ", self.mouse_handler),
                ("class:scrollbar", "\n", self.mouse_handler),
            ]
        # Bottom of thumb
        if show_thumb_bottom:
            result += [
                (
                    "class:scrollbar.background,scrollbar.end",
                    thumb_bottom_char,
                    self.mouse_handler,
                ),
                ("class:scrollbar", "\n", self.mouse_handler),
            ]
        # Track below the thumb
        for _ in range(rows_after_thumb):
            result += [
                ("class:scrollbar.background", " ", self.mouse_handler),
                ("class:scrollbar", "\n", self.mouse_handler),
            ]
        # Down button
        if display_arrows:
            result += [
                ("class:scrollbar.arrow", self.down_arrow_symbol, self.mouse_handler),
            ]

        return result

    def mouse_handler(
        self, mouse_event: "MouseEvent", repeated: "bool" = False
    ) -> "None":
        """Handle scrollbar mouse events.

        Scrolls up or down if the arrows are clicked, repeating while the mouse button
        is held down. Scolls up or down one page if the background is clicked,
        repeating while the left mouse button is held down. Scrolls if the
        scrollbar-button is dragged. Scrolls if the scroll-wheel is used on the
        scrollbar.

        Args:
            mouse_event: The triggering mouse event
            repeated: Set to True if the method is running as a repeated event

        """
        assert self.window_render_info is not None

        row = mouse_event.position.y
        content_height = self.window_render_info.content_height

        # Handle scroll events on the scrollbar
        if mouse_event.event_type == MouseEventType.SCROLL_UP:
            self.window_render_info.window._scroll_up()
        elif mouse_event.event_type == MouseEventType.SCROLL_DOWN:
            self.window_render_info.window._scroll_down()

        # Mouse drag events
        elif self.dragging and mouse_event.event_type == MouseEventType.MOUSE_MOVE:
            # Scroll so the button gets moved to where the mouse is
            offset = int(
                (row - self.thumb_top - self.button_drag_offset)
                / self.track_height
                * content_height
            )
            if offset < 0:
                func = self.window_render_info.window._scroll_up
            else:
                func = self.window_render_info.window._scroll_down
            if func:
                # Scroll the window multiple times to scroll by the offset
                for _ in range(abs(offset)):
                    func()

        # Mouse down events
        elif mouse_event.event_type == MouseEventType.MOUSE_DOWN:
            # Scroll up/down one line if clicking on the arrows
            arrows = self.display_arrows()
            if arrows and row == 0:
                offset = -1
            elif arrows and row == self.window_render_info.window_height - 1:
                offset = 1
            # Scroll up or down one page if clicking on the background
            elif row < self.thumb_top or self.thumb_top + self.thumb_size < row:
                direction = (row < (self.thumb_top + self.thumb_size // 2)) * -2 + 1
                offset = direction * self.window_render_info.window_height
            # We are on the scroll button - start a drag event if this is not a
            # repeated mouse event
            elif not repeated:
                self.dragging = True
                self.button_drag_offset = mouse_event.position.y - int(self.thumb_top)
                return
            # Otherwise this is a click on the centre scroll button - do nothing
            else:
                offset = 0

            if mouse_event.button == MouseButton.LEFT:
                func = None
                if offset < 0:
                    func = self.window_render_info.window._scroll_up
                elif offset > 0:
                    func = self.window_render_info.window._scroll_down
                if func:
                    # Scroll the window multiple times to scroll by the offset
                    for _ in range(abs(offset)):
                        func()
                    # Trigger this mouse event to be repeated
                    self.repeat_task = get_app().create_background_task(
                        self.repeat(mouse_event)
                    )

        # Handle all other mouse events
        else:
            # Stop any repeated tasks
            if self.repeat_task is not None:
                self.repeat_task.cancel()
            # Cancel drags
            self.dragging = False

    async def repeat(self, mouse_event: "MouseEvent", timeout: "float" = 0.1) -> "None":
        """Repeat a mouse event after a timeout."""
        await asyncio.sleep(timeout)
        self.mouse_handler(mouse_event, repeated=True)
        get_app().invalidate()


class NumberedDiffMargin(Margin):
    """Margin that displays the line numbers of a :class:`Window`."""

    style = "class:line-number"

    def get_width(self, get_ui_content: "Callable[[], UIContent]") -> "int":
        """Return the width of the margin."""
        line_count = get_ui_content().line_count
        return len("%s" % line_count) + 2

    def create_margin(
        self, window_render_info: "WindowRenderInfo", width: "int", height: "int"
    ) -> "StyleAndTextTuples":
        """Generate the margin's content."""
        # Get current line number.
        current_lineno = window_render_info.ui_content.cursor_position.y
        # Construct margin.
        result: StyleAndTextTuples = []
        last_lineno = None
        for lineno in window_render_info.displayed_lines:
            # Only display line number if this line is not a continuation of the previous line.
            if lineno != last_lineno:
                if lineno is None:
                    pass
                linestr = str(lineno + 1).rjust(width - 2)
                style = self.style
                if lineno == current_lineno and get_app().layout.has_focus(
                    window_render_info.window
                ):
                    style = f"{style} class:line-number.current"
                result.extend(
                    [
                        (f"{style},edge", "▏"),
                        (style, linestr),
                        (f"{style},edge", "▕"),
                    ]
                )
            last_lineno = lineno
            result.append(("", "\n"))
        return result


class OverflowMargin(Margin):
    """A margin which indicates lines extending beyond the edge of the window."""

    def get_width(self, get_ui_content: "Callable[[], UIContent]") -> "int":
        """Return the width of the margin."""
        return 1

    def create_margin(
        self, window_render_info: "WindowRenderInfo", width: "int", height: "int"
    ) -> "StyleAndTextTuples":
        """Generate the margin's content."""
        from prompt_toolkit.formatted_text.utils import fragment_list_width

        result: "StyleAndTextTuples" = []

        for lineno in window_render_info.displayed_lines:
            line = window_render_info.ui_content.get_line(lineno)
            if (
                fragment_list_width(line) - window_render_info.window.horizontal_scroll
                > window_render_info.window_width + 1
            ):
                result.append(("class:input,overflow", "▹"))
            result.append(("", "\n"))

        return result
