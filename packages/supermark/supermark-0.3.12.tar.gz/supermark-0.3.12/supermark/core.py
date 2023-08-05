import inspect
import requests
from importlib import import_module
from pathlib import Path
from collections import defaultdict
from rich.progress import Progress, BarColumn
from concurrent.futures import ThreadPoolExecutor

from typing import Any, DefaultDict, Dict, List, Optional, Sequence, Set, Tuple

import rich
from rich.tree import Tree
import yaml
from yaml.scanner import ScannerError

from .chunks import (
    Chunk,
    HTMLChunk,
    MarkdownChunk,
    YAMLDataChunk,
    RawChunk,
    RawChunkType,
)
from .code import Code
from .extend import (
    Extension,
    ExtensionPoint,
    ParagraphExtension,
    ParagraphExtensionPoint,
    TableClassExtension,
    TableClassExtensionPoint,
    YamlExtension,
    YamlExtensionPoint,
)
from .parse import parse
from .report import Report
from .utils import remove_empty_lines_begin_and_end, write_file


class URLChecker:
    def __init__(self) -> None:
        self.urls: DefaultDict[str, Set[Chunk]] = defaultdict(set)

    def look_at_chunk(self, chunk: Chunk):
        chunk_urls = chunk.get_urls()
        if chunk_urls is not None:
            for url in chunk_urls:
                self.urls[url] |= {chunk}

    def _check_url(self, url: str, chunks: Set[Chunk]) -> None:
        try:
            response = requests.get(url)
            if response.status_code != 200:
                for chunk in chunks:
                    chunk.warning(
                        f"{url} is not reachable, status_code: {response.status_code}"
                    )
        except requests.exceptions.MissingSchema:
            ...  # a relative link
        except requests.exceptions.RequestException as e:
            for chunk in chunks:
                chunk.warning(f"{url} is not reachable. {type(e)}")

    def check_all_urls(self) -> None:
        for url, chunks in self.urls.items():
            self._check_url(url, chunks)

    def check(self) -> None:
        with ThreadPoolExecutor() as e:
            with Progress(
                "[progress.description]{task.description}",
                BarColumn(),
                "[progress.percentage]{task.percentage:>3.0f}%",
                transient=True,
            ) as progress:
                task = progress.add_task(
                    f"[orange]Checking {len(self.urls)} URLs",
                    total=len(self.urls),
                )
                futures = []
                for url, chunks in self.urls.items():
                    future = e.submit(
                        self._check_url,
                        url,
                        chunks,
                    )
                    future.add_done_callback(
                        lambda p: progress.update(task, advance=1.0)
                    )
                    futures.append(future)
                for future in futures:
                    future.result()


class Core:
    def __init__(self, report: Report, collect_urls: bool = False) -> None:
        self.report = report
        self.extension_points: Dict[str, ExtensionPoint] = {}
        self.yaml_extension_point: YamlExtensionPoint = self._register(
            YamlExtensionPoint()
        )
        self.paragraph_extension_point: ParagraphExtensionPoint = self._register(
            ParagraphExtensionPoint()
        )
        self.tableclass_extension_point: TableClassExtensionPoint = self._register(
            TableClassExtensionPoint()
        )
        self._load_extensions()
        self.collect_urls = collect_urls
        if collect_urls:
            self.url_checker = URLChecker()

    def _load_extensions(self):
        for file in (Path(__file__).parent / "extensions").glob("*"):
            if file.is_dir():
                self._register_module(f"supermark.extensions.{file.name}")

    def _register_module(self, name: str):
        try:
            module = import_module(name, package=None)
            clsmembers = inspect.getmembers(module, inspect.isclass)
            for name, clazz in clsmembers:
                if issubclass(clazz, Extension) and clazz.__module__ == module.__name__:
                    extension = clazz()
                    extension.set_folder(Path(module.__file__).parent)
                    self.register(extension)
                    self.report.info(f"Found extension {name}")
        except ModuleNotFoundError as error:
            self.report.error(f"Error when registering {name}")
            print(error)

    def _register(self, extension_point: ExtensionPoint) -> ExtensionPoint:
        self.extension_points[extension_point.name] = extension_point
        return extension_point

    def register(self, extension: Extension) -> None:
        if isinstance(extension, YamlExtension):
            self.yaml_extension_point.register(extension)
        elif isinstance(extension, ParagraphExtension):
            self.paragraph_extension_point.register(extension)
        elif isinstance(extension, TableClassExtension):
            self.tableclass_extension_point.register(extension)
        else:
            ValueError("Not sure what to do with this extension.")

    def cast(
        self,
        rawchunks: Sequence[RawChunk],
        report: Report,
        used_extensions: Optional[Set[Extension]] = None,
    ) -> Sequence[Chunk]:
        chunks: Sequence[Chunk] = []
        page_variables: Dict[str, Any] = {}
        for raw in rawchunks:
            chunk = self._cast_chunk(
                raw, page_variables, report, used_extensions=used_extensions
            )
            if chunk is None:
                report.tell(
                    "No idea what to do with {} chunk starting with '{}...'".format(
                        raw.type, raw.get_first_line()[:10]
                    ).replace("\n", ""),
                    Report.ERROR,
                    raw.path,
                    raw.start_line_number,
                )
            else:
                chunks.append(chunk)
                if used_extensions is not None:
                    chunk.add_used_extension(used_extensions, self)
                if self.collect_urls:
                    self.url_checker.look_at_chunk(chunk)
        return chunks

    def _cast_chunk(
        self,
        raw: RawChunk,
        page_variables: Dict[str, Any],
        report: Report,
        used_extensions: Optional[Set[Extension]] = None,
    ) -> Optional[Chunk]:
        chunk_type = raw.get_type()
        if chunk_type == RawChunkType.MARKDOWN:
            tag = raw.get_tag()
            if tag is None or tag == "aside":
                return MarkdownChunk(raw, page_variables)
            else:
                return self.paragraph_extension_point.cast_paragraph_class(
                    raw, tag, page_variables, report, used_extensions=used_extensions
                )
        elif chunk_type == RawChunkType.YAML:
            try:
                temp: Any = yaml.safe_load("".join(raw.lines))
                if isinstance(temp, dict):
                    dictionary: Dict[str, Any] = temp
                    if "type" in dictionary:
                        return self.yaml_extension_point.cast_yaml(
                            raw,
                            dictionary["type"],
                            dictionary,
                            page_variables,
                            used_extensions=used_extensions,
                        )
                    else:
                        data_chunk = YAMLDataChunk(raw, dictionary, page_variables)
                        try:
                            page_variables.update(data_chunk.dictionary)
                        except ValueError as e:
                            print(e)
                        return data_chunk
            except ScannerError as se:
                raw.report.error(f"Something is wrong with YAML section {se}")
            else:
                raw.report.error("Something is wrong with the YAML section.")
        elif chunk_type == RawChunkType.HTML:
            return HTMLChunk(raw, page_variables)
        elif chunk_type == RawChunkType.CODE:
            # TODO handle code chunks as extensions
            return Code(raw, page_variables)
        else:
            print(
                "unknown chunk type: {} with type {}".format(
                    chunk_type, type(chunk_type)
                )
            )

    def arrange_assides(self, chunks: Sequence[Chunk]) -> Sequence[Chunk]:
        main_chunks: Sequence[Chunk] = []
        current_main_chunk = None
        for chunk in chunks:
            if chunk.is_aside():
                if current_main_chunk is not None:
                    current_main_chunk.add_aside(chunk)
                else:
                    chunk.raw_chunk.report.tell(
                        "Aside chunk cannot be defined as first element.",
                        level=Report.WARNING,
                    )
                    main_chunks.append(chunk)
            else:
                main_chunks.append(chunk)
                current_main_chunk = chunk
        return main_chunks

    def parse_lines(
        self,
        lines: List[str],
        source_file_path: Path,
        report: Report,
        used_extensions: Optional[Set[Extension]] = None,
    ):
        chunks = parse(lines, source_file_path, report)
        chunks = self.cast(chunks, report, used_extensions=used_extensions)
        return self.arrange_assides(chunks)

    def parse_file(
        self,
        source_file_path: Path,
        abort_draft: bool = False,
        reformat: bool = False,
        used_extensions: Optional[Set[Extension]] = None,
    ) -> Optional[Sequence[Chunk]]:
        with open(source_file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            # report.tell("{}".format(source_file_path), Report.INFO)
            chunks = self.parse_lines(
                lines, source_file_path, self.report, used_extensions
            )
            # TODO do this in async
            if reformat:
                source_code: str = ""
                for chunk in chunks:
                    code = chunk.recode()
                    if code is not None:
                        source_code = source_code + remove_empty_lines_begin_and_end(
                            code
                        )
                        source_code = source_code + "\n\n\n"
                write_file(source_code, source_file_path, self.report)

            return chunks

    def get_css(self, used_extensions: Set[Extension]) -> str:
        all_css: str = ""
        for extension in sorted(list(used_extensions), key=lambda e: e.folder):
            all_css += extension.get_css() + "\n"
        return all_css

    def get_js(self, used_extensions: Set[Extension]) -> str:
        all_js: str = ""
        for extension in sorted(list(used_extensions), key=lambda e: e.folder):
            all_js += extension.get_js() + "\n"
        return all_js

    def info(self):
        tree = Tree("Supermark Extensions")
        for extension_point in self.extension_points.values():
            ep_tree = tree.add(extension_point.name)
            for extension in extension_point.extensions.values():
                ep_tree.add(str(extension))
        rich.print(tree)

    def get_all_extensions(self) -> Sequence[Extension]:
        extensions: List[Extension] = []
        for extension_point in self.extension_points.values():
            for extension in extension_point.extensions.values():
                extensions.append(extension)
        return extensions


"""
   Chunk  |- HTML
          |- Code
          |- YamlChunk --- YamlDataChunk
          |             |- Table
          |             |- Video
          |             |- Figure
          |             |- Lines
          |             |- Button
          |             |- Lines
          |- Markdown
                |- Hint     
"""
