from pathlib import Path
from typing import Dict, List, Optional, Set

from rich import print as pprint
from rich.panel import Panel
from rich.tree import Tree
from rich.console import Console

from colorama import Fore, Back, Style
import indentation

COLOR_1 = Fore.LIGHTBLUE_EX
COLOR_2 = Fore.LIGHTGREEN_EX


class ReportEntry:
    def __init__(
        self,
        message: str,
        level: int,
        path: Optional[Path] = None,
        line: Optional[int] = None,
        conclusion: bool = False,
    ):
        self.message = message
        self.level = level
        self.path = path
        self.line = line
        self.conclusion = conclusion
        self.cwd = Path.cwd()

    def _path_to_string(self, path: Path) -> str:
        # if path.is_relative_to(self.cwd):
        #    return str(path.relative_to(self.cwd))
        return str(path)

    def get_hash(self) -> str:
        return self.message

    def get_styled_location(self) -> str:
        s = ""
        if self.path:
            s += f"[deep_sky_blue2][not bold]{str(self.path)}[/deep_sky_blue2][/not bold]"
            if self.line is not None:
                s += f" [dark_cyan]{self.line}[/dark_cyan]"
        return s

    def to_string(self) -> str:
        s = ""
        if self.path is not None:
            s = (
                COLOR_1
                + self._path_to_string(self.path)
                + " "
                + COLOR_2
                + str(self.line)
                + "\n"
            )
        if self.level == Report.WARNING:
            s = s + "    "
        elif self.level == Report.ERROR:
            s = s + "    "
        else:
            s = s + "    "
        s = s + Fore.WHITE + indentation.set(self.message, 1)
        return s


class Report:

    INFO = 1
    WARNING = 2
    ERROR = 3

    def __init__(self, source_path: Optional[Path] = None):
        self.source_path = source_path
        self.messages: List[ReportEntry] = []
        self.max_level = self.INFO
        self.files = []
        self.conclusions: List[ReportEntry] = []
        self.warnings: int = 0
        self.errors: int = 0

    def get_max_level(self):
        return self.max_level

    def has_error(self):
        return self.max_level == Report.ERROR

    def tell(
        self,
        message: str,
        level: int = 1,
        path: Optional[Path] = None,
        line: Optional[int] = None,
    ) -> None:
        self.max_level = max(self.max_level, level)
        entry = ReportEntry(message, level=level, path=path, line=line)
        self.messages.append(entry)
        if entry.path:
            self.files.append(entry.path)
        if level == Report.ERROR:
            self.errors += 1
        elif level == Report.WARNING:
            self.warnings += 1

    def info(
        self,
        message: str,
        path: Optional[Path] = None,
        line: Optional[int] = None,
    ):
        self.tell(message, level=Report.INFO, path=path, line=line)

    def warning(
        self,
        message: str,
        path: Optional[Path] = None,
        line: Optional[int] = None,
    ):
        self.tell(message, level=Report.WARNING, path=path, line=line)

    def error(
        self,
        message: str,
        path: Optional[Path] = None,
        line: Optional[int] = None,
    ):
        self.tell(message, level=Report.ERROR, path=path, line=line)

    def conclude(self, message: str):
        entry = ReportEntry(
            message, level=Report.INFO, path=None, line=None, conclusion=True
        )
        self.conclusions.append(entry)

    def print_(self):
        for m in self.messages:
            print(m.to_string())

    def _get_conclusion_panel(self):
        if len(self.conclusions) > 0:
            for entry in self.conclusions:
                return Panel(entry.message, expand=False)
        if self.errors > 0:
            if self.warnings > 0:
                plural_w = "" if self.warnings == 1 else "s"
                plural_e = "" if self.errors == 1 else "s"
                return Panel(
                    f":tomato: Finished with {self.errors} error{plural_e} and {self.warnings} warning{plural_w}.",
                    expand=False,
                    style="red3",
                )
            else:
                plural = "" if self.errors == 1 else "s"
                return Panel(
                    f":tomato: Finished with {self.errors} error{plural}.",
                    expand=False,
                    style="red3",
                )
        elif self.warnings > 0:
            plural = "" if self.warnings == 1 else "s"
            return Panel(
                f":banana: Finished with {self.warnings} warning{plural}.",
                expand=False,
                style="dark_orange",
            )
        else:
            return Panel(":shamrock: Finished.", expand=False, style="dark_sea_green")

    def _get_tree(self, verbose: bool) -> Tree:
        panel = self._get_conclusion_panel()
        tree = Tree(panel, guide_style="grey50")
        levels = (
            [Report.ERROR, Report.WARNING, Report.INFO]
            if verbose
            else [Report.ERROR, Report.WARNING]
        )
        hashes: Dict[str, Tree] = {}
        for level in levels:
            for entry in self.messages:
                if entry.level == level:
                    if entry.get_hash() in hashes:
                        if entry.path is not None:
                            hashes[entry.get_hash()].add(entry.get_styled_location())
                    else:
                        level_color = (
                            "orange3"
                            if level == Report.WARNING
                            else "red1"
                            if level == Report.ERROR
                            else "dark_sea_green4"
                        )
                        hashes[entry.get_hash()] = tree.add(
                            entry.message, style=f"bold {level_color}"
                        )
                        if entry.path is not None:
                            hashes[entry.get_hash()].add(entry.get_styled_location())
        return tree

    def print(self, verbose: bool = False):
        tree = self._get_tree(verbose=verbose)
        pprint(tree)

    def print_to_file(self, log: Path):
        with open(log, "w") as file:
            tree = self._get_tree(verbose=True)
            console = Console(record=True)
            with console.capture() as capture:
                console.print(tree)
            file.write(console.export_text())


    # @staticmethod
    # def print_reports(verbose: bool = False) -> int:
    #     levels = (
    #         [Report.ERROR, Report.WARNING, Report.INFO]
    #         if verbose
    #         else [Report.ERROR, Report.WARNING]
    #     )
    #     total_max_level = Report.INFO
    #     for level in levels:
    #         for report in Report.all_reports:
    #             if report.get_max_level() == level:
    #                 report.print_()
    #                 if level > total_max_level:
    #                     total_max_level = level

    #     concluded: bool = False
    #     for report in Report.all_reports:
    #         for entry in report.conclusions:
    #             pprint(Panel(entry.message, expand=False))
    #             concluded = True
    #     if not concluded:
    #         pprint(Panel("Finished with X warnings and X errors."))
    #     return total_max_level

    # @staticmethod
    # def reset_reports():
    #     Report.all_reports = set()
