from abc import abstractmethod
import regex as re
import hashlib
from optparse import Option

from yaml.scanner import ScannerError
from .base import Extension
from typing import Any, Dict, Optional, Sequence, List, Set
from pathlib import Path
from enum import Enum

from .pandoc import convert, convert_code
import yaml
from .utils import has_class_tag
from .report import Report


def is_empty(s_line: str) -> bool:
    return not s_line


class Builder:
    def __init__(
        self,
        input_path: Path,
        output_path: Path,
        template_file: Path,
        report: Report,
        rebuild_all_pages: bool = True,
        abort_draft: bool = True,
        verbose: bool = False,
        reformat: bool = False,
    ) -> None:
        self.input_path = input_path
        self.output_path = output_path
        self.template_file = template_file
        self.report = report
        self.rebuild_all_pages = rebuild_all_pages
        self.abort_draft = abort_draft
        self.verbose = verbose
        self.reformat = reformat
        self.chunk_counts: Dict[str, int] = {}
        self.extensions_used: Set[Extension] = set()

    @abstractmethod
    def build(self):
        ...

    def parse_file(
        self,
        source_file_path: Path,
        extensions_used: Set[Extension],
    ) -> Optional[Sequence["Chunk"]]:
        chunks = self.core.parse_file(
            source_file_path, self.abort_draft, self.reformat, extensions_used
        )
        self.extensions_used = self.extensions_used.union(extensions_used)
        if chunks is not None:
            self._count_chunks(chunks)
        return chunks

    def set_core(self, core: "Core") -> None:
        self.core = core

    def _count_chunks(self, chunks: Sequence["Chunk"]):
        for chunk in chunks:
            count = 0
            if chunk.get_chunk_type() in self.chunk_counts:
                count = self.chunk_counts[chunk.get_chunk_type()]
            self.chunk_counts[chunk.get_chunk_type()] = count + 1

    def get_chunk_counts(self) -> Dict[type, int]:
        return self.chunk_counts

    def get_extensions_used(self) -> Set[Extension]:
        return self.extensions_used

    def convert(
        self, source: str, target_format: str, source_format: str = "md"
    ) -> str:
        return convert(source, target_format, source_format=source_format)

    def convert_code(self, source: str, target_format: str) -> str:
        return convert_code(source, target_format)


class RawChunkType(Enum):
    MARKDOWN = 0
    YAML = 1
    CODE = 2
    HTML = 3


class RawChunk:
    def __init__(
        self,
        lines: Sequence[str],
        chunk_type: RawChunkType,
        start_line_number: int,
        path: Path,
        report: "Report",
    ):
        self.lines: List[str] = list(lines)
        self.type = chunk_type
        assert isinstance(self.type, RawChunkType)
        self.start_line_number = start_line_number
        self.path = Path(path)
        self.parent_path = Path(path).parent.parent
        self.report = report
        self.hash = None

        # check if we only got empty lines
        def all_empty(lines: Sequence[str]) -> bool:
            if len(lines) == 0:
                return True
            for line in lines:
                if line.strip():
                    return False
            return True

        self._is_empty = all_empty(self.lines)
        # remove blank lines from the beginning
        while len(self.lines) > 0 and is_empty(self.lines[0].strip()):
            self.lines.pop(0)
            self.start_line_number = self.start_line_number + 1
        self.tag = None
        if len(self.lines) > 0:
            if has_class_tag(self.lines[0]):
                self.tag = self.lines[0].strip().split(":")[1].lower()
        self.post_yaml = None

    def tell(self, message: str, level: int = 0):
        self.report.tell(
            message, level=level, line=self.start_line_number, path=self.path
        )

    def get_tag(self):
        return self.tag

    def is_empty(self):
        return self._is_empty

    def get_type(self) -> RawChunkType:
        return self.type

    def get_first_line(self):
        if len(self.lines) == 0:
            return "empty"
        return self.lines[0]

    def _get_reference(self):
        # TODO check if this is called too often
        if self.type == RawChunkType.YAML:
            try:
                self.dictionary = yaml.safe_load("".join(self.lines))
                if "ref" in self.dictionary:
                    return self.path / self.dictionary["ref"]
            except ScannerError as se:
                self.report.error(f"Error parsing YAML {se}")
        return None

    def get_hash(self) -> str:
        if self.hash is None:
            shake = hashlib.shake_128()
            shake.update("".join(self.lines).encode("utf-8"))
            self.hash = shake.hexdigest(3)
        return self.hash


class Chunk:
    """Base class for a chunk."""

    INFO = 1
    WARNING = 2
    ERROR = 3

    def __init__(self, raw_chunk: RawChunk, page_variables: Dict[str, Any]):
        self.raw_chunk = raw_chunk
        self.page_variables = page_variables
        self.aside: bool = False
        self.asides: List["Chunk"] = []
        self.ok: bool = True
        self.extension = None

    def is_ok(self) -> bool:
        return self.ok

    def get_extension(self) -> Optional[Extension]:
        return self.extension

    def is_aside(self) -> bool:
        return self.aside

    def add_aside(self, aside: "Chunk") -> None:
        self.asides.append(aside)

    def get_asides(self):
        return self.asides

    def get_first_line(self) -> str:
        return self.raw_chunk.lines[0]

    def get_last_line(self) -> str:
        return self.raw_chunk.lines[-1]

    def get_type(self) -> RawChunkType:
        return self.raw_chunk.type

    def get_start_line_number(self) -> int:
        return self.raw_chunk.start_line_number

    def get_content(self):
        return "".join(self.raw_chunk.lines)

    def tell(self, message: str, level: int = 0):
        self.raw_chunk.tell(message, level=level)

    def info(self, message: str):
        self.raw_chunk.tell(message, level=Chunk.INFO)

    def warning(self, message: str):
        self.raw_chunk.tell(message, level=Chunk.WARNING)

    def error(self, message: str):
        self.raw_chunk.tell(message, level=Chunk.ERROR)

    def to_latex(self, builder: Builder) -> Optional[str]:
        print("No conversion to latex: " + self.get_content())
        return None

    def to_html(self, builder: Builder) -> Optional[str]:
        print("No conversion to html: " + self.get_content())
        return None

    def recode(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def add_used_extension(self, used_extensions: Set[Extension], core: Any):
        ...

    @staticmethod
    def create_hash(content: str):
        shake = hashlib.shake_128()
        shake.update(content.encode("utf-8"))
        return shake.hexdigest(3)

    def get_dir_cached(self):
        cached = self.raw_chunk.parent_path / "cached"
        cached.mkdir(parents=True, exist_ok=True)
        return cached

    @abstractmethod
    def get_chunk_type(self) -> str:
        ...

    @abstractmethod
    def get_escaped_source(self) -> str:
        ...

    def get_urls(self) -> Optional[Sequence[str]]:
        return None


class YAMLChunk(Chunk):
    def __init__(
        self,
        raw_chunk: RawChunk,
        dictionary: Dict[str, Any],
        page_variables: Dict[str, Any],
        required: Optional[Sequence[str]] = None,
        optional: Optional[Sequence[str]] = None,
    ):
        super().__init__(raw_chunk, page_variables)
        self.dictionary = dictionary
        t = self.dictionary["type"] if "type" in self.dictionary else "-"
        required = required or []
        optional = optional or []
        for key in required:
            if key not in self.dictionary:
                self.tell(
                    "YAML section of type {} misses required parameter '{}' class {}.".format(
                        t, key, self.__class__
                    ),
                    level=self.ERROR,
                )
        for key in self.dictionary.keys():
            if (key not in required) and (key not in optional) and (key != "type"):
                self.tell(
                    "YAML section of type {} has unknown parameter '{}' class {}.".format(
                        t, key, self.__class__
                    ),
                    level=self.WARNING,
                )

    def get(self, attribute: str) -> Optional[Any]:
        if attribute in self.dictionary:
            return self.dictionary[attribute]
        return None

    def has_post_yaml(self):
        return self.raw_chunk.post_yaml is not None

    def get_post_yaml(self):
        return (
            None
            if self.raw_chunk.post_yaml is None
            else "".join(self.raw_chunk.post_yaml)
        )

    def _yaml_as_source(self) -> str:
        return (
            "---\n"
            + yaml.dump(
                self.dictionary,
                sort_keys=False,
            )
            + "---\n"
        )

    def recode(self) -> str:
        if self.has_post_yaml():
            return self._yaml_as_source() + "".join(self.raw_chunk.post_yaml)
        else:
            return self._yaml_as_source()

    def get_escaped_source(self) -> str:
        # TODO escape post yaml section
        return "```yaml\n" + self._yaml_as_source() + "\n```"

    def get_chunk_type(self) -> str:
        # if hasattr(self, "type"):
        return "yaml" + "/" + self.dictionary["type"]
        # return "yaml"


class YAMLDataChunk(YAMLChunk):
    def __init__(
        self,
        raw_chunk: RawChunk,
        dictionary: Dict[str, Any],
        page_variables: Dict[str, Any],
    ):
        super().__init__(raw_chunk, dictionary, page_variables, optional=["status"])

    def to_latex(self, builder: Builder) -> Optional[str]:
        return None

    def get_chunk_type(self) -> str:
        return "yaml/data"


class MarkdownChunk(Chunk):
    def __init__(self, raw_chunk: RawChunk, page_variables: Dict[str, Any]):
        super().__init__(raw_chunk, page_variables)
        self.content = "".join(self.raw_chunk.lines)
        self.is_section = super().get_first_line().startswith("# ")
        if raw_chunk.get_tag() is not None:
            self.class_tag = super().get_first_line().strip().split(":")[1].lower()
            self.content = self.content[len(self.class_tag) + 2 :].strip()
            if self.class_tag == "aside":
                self.aside = True
                self.class_tag = None
        else:
            self.class_tag = None
            self.aside = False

    def get_chunk_type(self) -> str:
        if self.class_tag:
            return "md" + "/" + str(self.class_tag)
        return "md"

    def get_content(self) -> str:
        return self.content

    def to_html(self, builder: Builder) -> str:
        if self.aside:
            aside_id = Chunk.create_hash(self.content)
            output: Sequence[str] = []
            output.append(
                '<span name="{}"></span><aside name="{}">'.format(aside_id, aside_id)
            )
            output.append(
                builder.convert(
                    self.get_content(), target_format="html", source_format="md"
                )
            )
            output.append("</aside>")
            return "".join(output)
        else:
            if self.class_tag:
                output = '<div class="{}">{}</div>'.format(
                    self.class_tag,
                    builder.convert(
                        self.get_content(), target_format="html", source_format="md"
                    ),
                )
            else:
                output = builder.convert(
                    self.get_content(), target_format="html", source_format="md"
                )
            return output

    def wrap(self, content: str) -> str:
        return (
            "\\begin{tcolorbox}[colback=red!5!white,colframe=red!75!black,arc=0pt,outer arc=0pt,leftrule=2pt,rightrule=0pt,toprule=0pt,bottomrule=0pt]"
            + content
            + r"\end{tcolorbox}"
        )

    def bold_prefix(self, prefix: str) -> str:
        return "\\textbf{{{}}} ".format(prefix + ":")

    def to_latex(self, builder: Builder) -> str:
        # TODO paragraph style in latex
        output = convert(self.get_content(), target_format="latex", source_format="md")
        if self.class_tag is None:
            return output
        elif self.class_tag == "aside":
            return self.wrap(output)
        elif self.class_tag == "goals":
            return self.wrap(output)
        elif self.class_tag == "warning":
            return self.wrap(self.bold_prefix("Warning") + output)
        elif self.class_tag == "tip":
            return self.wrap(self.bold_prefix("Tip") + output)
        return output

    def recode(self):
        if self.class_tag is not None:
            return ":" + self.class_tag + ": " + self.get_content()
        return self.get_content()

    def get_escaped_source(self) -> str:
        return "```markdown\n" + self.recode() + "\n```"

    def get_urls(self) -> Optional[Sequence[str]]:
        # TODO only create once
        pattern = re.compile(r"\[([^][]+)\](\(((?:[^()]+|(?2))+)\))")
        result: Optional[Sequence[str]] = None
        for match in pattern.finditer(self.get_content()):
            if result is None:
                result = []
                _, _, url = match.groups()
                result.append(url)
        return result


class HTMLChunk(Chunk):
    def __init__(self, raw_chunk: RawChunk, page_variables: Dict[str, Any]):
        super().__init__(raw_chunk, page_variables)

    def to_html(self, builder: Builder):
        return super().get_content()

    def to_latex(self, builder: Builder) -> Optional[str]:
        if super().get_content().startswith("<!--"):
            return None
        else:
            return convert(
                self.get_content(), target_format="latex", source_format="html"
            )

    def recode(self) -> str:
        return self.get_content()

    def get_escaped_source(self) -> str:
        return "```html\n" + self.recode() + "\n```"

    def get_chunk_type(self) -> str:
        return "html"
