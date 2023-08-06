from abc import ABC, abstractmethod
from pathlib import Path

AXE_FILE_NAME = "axe.min.js"
AXE_FILE_PATH = Path(__file__).parent / AXE_FILE_NAME

AXE_SCRIPT = AXE_FILE_PATH.read_text()


class AxeBase(ABC):
    """Abstract base class."""

    def __init__(self, axe_script: str = AXE_SCRIPT) -> None:
        """
        Args:
            axe_script (str, optional): `axe.js` or `axe.min.js` javascript.
                Defaults to AXE_SCRIPT.
        """
        self.axe_script = axe_script

    @staticmethod
    def _format_script_args(
        context: str | list | dict | None = None, options: dict | None = None
    ) -> str:
        args_list = []
        # If context is passed, add to args
        if context:
            args_list.append(repr(context))
        # If options is passed, add to args
        if options:
            args_list.append(str(options))
        # Add comma delimiter only if both parameters are passed
        args = ",".join(args_list)

        return args

    @abstractmethod
    def run(self):
        pass

    @classmethod
    def from_file(cls, axe_min_js_path: str | Path) -> "AxeBase":
        """Load axe script from file and create Axe instance.

        Args:
            axe_min_js_path (str | Path): path to `axe.js` or `axe.min.js`

        Returns:
            AxeBase: Axe instance
        """
        axe_script = Path(axe_min_js_path).read_text(encoding="UTF-8")
        return cls(axe_script=axe_script)
