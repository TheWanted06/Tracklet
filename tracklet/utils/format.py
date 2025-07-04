# tracklet/utils/formats.py

from datetime import datetime
from rich.console import Console
from rich.text import Text
from rich.style import Style

console = Console()

# --- Date & Time Formatting ---

def format_datetime(dt_str: str) -> str:
    """Parse ISO string and return a human-readable datetime."""
    try:
        dt = datetime.fromisoformat(dt_str)
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return dt_str


# --- Status & Tag Styling ---

STATUS_STYLES = {
    "todo": Style(color="bright_blue", bold=True),
    "in_progress": Style(color="yellow", bold=True),
    "completed": Style(color="green", bold=True),
    "blocked": Style(color="red", bold=True),
    "default": Style(color="white")
}

def status_text(status: str) -> Text:
    """Return a styled Text object for a given status."""
    style = STATUS_STYLES.get(status, STATUS_STYLES["default"])
    return Text(status.replace("_", " ").title(), style=style)


# --- General Colored Output ---

def print_colored(message: str, color: str = "white", bold: bool = False):
    """Print any message with rich formatting."""
    style = Style(color=color, bold=bold)
    console.print(Text(message, style=style))


# --- Tags or Info Lists ---

def format_tags(tags: list[str]) -> Text:
    """Return a comma-separated colored tag list."""
    tag_text = Text()
    for i, tag in enumerate(tags):
        tag_text.append(tag, style=Style(color="magenta"))
        if i < len(tags) - 1:
            tag_text.append(", ")
    return tag_text
