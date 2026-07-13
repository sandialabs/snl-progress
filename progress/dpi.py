"""DPI / high-DPI scaling helpers for cross-platform consistency."""

import sys
from PySide6.QtWidgets import QApplication


def is_windows() -> bool:
    return sys.platform == "win32"


def get_scale_factor() -> float:
    """Return the primary screen device-pixel-ratio (e.g. 1.0, 1.25, 1.5, 2.0)."""
    screen = QApplication.primaryScreen()
    if screen is None:
        return 1.0
    return screen.devicePixelRatio()


def get_logical_dpi() -> float:
    """Return the logical DPI of the primary screen."""
    screen = QApplication.primaryScreen()
    if screen is None:
        return 96.0
    return screen.logicalDotsPerInch()


def scaled(value: int | float) -> int:
    """Scale a logical-pixel value by the screen's device-pixel-ratio.

    Useful for widget sizes, margins, and paddings that should remain
    physically consistent across different DPI settings.
    """
    return int(value * get_scale_factor())
