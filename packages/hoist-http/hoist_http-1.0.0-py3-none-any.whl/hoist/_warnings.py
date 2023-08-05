import sys
import warnings
from typing import Optional, TextIO, Type, Union

from rich.console import Console
from rich.panel import Panel

# see https://github.com/Textualize/rich/issues/433

__all__ = ("warn",)


def _showwarning(
    message: Union[Warning, str],
    category: Type[Warning],
    filename: str,
    lineno: int,
    file: Optional[TextIO] = None,
    line: Optional[str] = None,
) -> None:
    msg = warnings.WarningMessage(
        message,
        category,
        filename,
        lineno,
        file,
        line,
    )

    if file is None:
        file = sys.stderr
        if file is None:
            # sys.stderr is None when run with pythonw.exe:
            # warnings get lost
            return
    text = warnings._formatwarnmsg(msg)  # type: ignore
    if file.isatty():
        Console(file=file, stderr=True).print(
            Panel(
                text,
                title=f"[bold dim yellow]{category.__name__}",
                subtitle=f"[dim italic cyan]\n{filename}, line {lineno}",
                highlight=True,
                style="bold dim yellow",
            )
        )
    else:
        try:
            file.write(f"{category.__name__}: {text}")
        except OSError:
            # the file (probably stderr) is invalid - this warning gets lost.
            pass


warnings.showwarning = _showwarning


def _warning_no_src_line(
    message: Union[Warning, str],
    category: Type[Warning],
    filename: str,
    lineno: int,
    file: Optional[TextIO] = None,
    line: Optional[str] = None,
) -> str:
    if (file is None and sys.stderr is not None) or file is sys.stderr:
        return str(message) + "\n"
    else:
        return f"{filename}:{lineno} {category.__name__}: {message}\n"


warnings.formatwarning = _warning_no_src_line  # type: ignore


def warn(message: str, *, category: Optional[Type[Warning]] = None) -> None:
    """Display a warning."""
    warnings.warn(message, category=category or RuntimeWarning)
