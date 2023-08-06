import sys
from pathlib import Path

from tukaan._tcl import Tcl


class Serif:
    """
    A Python interface to the Serif C extension.

    Attributes:
        loaded_fonts: A dictionary that contains the path of the
            loaded files along with the font families contained in them.
    """

    loaded_fonts: list[Path] = []

    @staticmethod
    def init() -> None:
        platform = {"darwin": "mac", "win32": "win"}.get(sys.platform, "unix")

        Tcl.load_dll(
            Path(__file__).parent
            / platform
            / f"libserif_{'x64' if sys.maxsize > 2**32 else 'x32'}{Tcl.dll_ext}",
            "Serif",
        )

    @classmethod
    def load(cls, file_path: Path) -> list[str]:
        """
        Load a font file specified by `file_path`.
        The file may contain multiple font families.
        If the font file is already loaded, does nothing.
        """

        if file_path not in cls.loaded_fonts:
            Tcl.call(None, "Serif::load_fontfile", file_path)
            cls.loaded_fonts.append(file_path)

    @classmethod
    def unload(cls, file_path: Path) -> None:
        """
        Unload a previously loaded font file specified by `file_path`.
        If the file wasn't loaded, does nothing.
        """

        if file_path in cls.loaded_fonts:
            Tcl.call(None, "Serif::unload_fontfile", file_path)
            cls.loaded_fonts.remove(file_path)

    @classmethod
    def cleanup(cls) -> None:
        """Unloads all loaded fonts."""
        for font in cls.loaded_fonts:
            cls.unload(font)
