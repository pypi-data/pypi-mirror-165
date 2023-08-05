from pathlib import Path
from typing import Optional, Sequence


class ExtensionPoint:
    """Base class for any extension point."""

    def __init__(self, name: str):
        self.name = name


class Extension:
    def __init__(self):
        ...

    def set_folder(self, folder: Path):
        self.folder = folder

    def _find_files(self, pattern: str):
        return list(self.folder.glob(pattern))

    def files_to_string(self, files: Sequence[Path]) -> str:
        string: str = ""
        for file in files:
            with open(
                file, "r", encoding="utf-8", errors="surrogateescape"
            ) as open_file:
                string += open_file.read()
        return string

    def get_css(self) -> str:
        return self.files_to_string(self._find_files("*.css"))

    def get_js(self) -> str:
        return self.files_to_string(self._find_files("*.js"))

    def get_examples(self):
        return self._find_files("examples/*.md")

    def get_doc(self) -> Optional[Path]:
        files = self._find_files("doc.md")
        if len(files) > 0:
            return files[0]
        return None

    def __str__(self) -> str:
        return "Extension at " + str(self.folder)
