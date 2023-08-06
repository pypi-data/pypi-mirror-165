from enum import Enum
from pathlib import Path
from typing import List, Sequence, TYPE_CHECKING
from .chunks import RawChunk, RawChunkType
from .utils import has_class_tag

if TYPE_CHECKING:
    from .report import Report


class ParserState(Enum):
    MARKDOWN = 0
    YAML = 1
    CODE = 2
    HTML = 3
    AFTER_YAML = 4
    AFTER_YAML_CONTENT = 5


def is_empty(s_line: str) -> bool:
    return not s_line


def yaml_start(s_line: str) -> bool:
    return s_line == "---"


def yaml_stop(s_line: str) -> bool:
    return s_line == "---" or s_line == "..."


def markdown_start(s_line: str, empty_lines: int) -> bool:
    return (
        has_class_tag(s_line)
        or s_line.startswith("# ")
        or empty_lines >= 2
        or s_line.startswith("Aside:")
    )


def html_start(s_line: str, empty_lines: int) -> bool:
    return s_line.startswith("<") and empty_lines >= 2


def html_stop(empty_lines: int) -> bool:
    return empty_lines >= 2


def code_start(s_line: str) -> bool:
    return s_line.startswith("```")


def code_stop(s_line: str) -> bool:
    return s_line.startswith("```")


def parse(lines: List[str], path: Path, report: "Report") -> Sequence[RawChunk]:
    chunks: Sequence[RawChunk] = []
    current_lines: Sequence[str] = []
    empty_lines = 0
    state = ParserState.MARKDOWN
    start_line_number = 0
    previous_yaml_chunk = None

    for line_number, line in enumerate(lines, start=1):
        s_line: str = line.strip()
        if state == ParserState.MARKDOWN:
            if is_empty(s_line):
                empty_lines = empty_lines + 1
                current_lines.append(line)
            elif yaml_start(s_line):
                chunks.append(
                    RawChunk(
                        current_lines,
                        RawChunkType.MARKDOWN,
                        start_line_number,
                        path,
                        report,
                    )
                )
                state = ParserState.YAML
                current_lines = []
                start_line_number = line_number
                empty_lines = 0
            elif code_start(s_line):
                chunks.append(
                    RawChunk(
                        current_lines,
                        RawChunkType.MARKDOWN,
                        start_line_number,
                        path,
                        report,
                    )
                )
                state = ParserState.CODE
                current_lines = [line]
                start_line_number = line_number
                empty_lines = 0
            elif html_start(s_line, empty_lines):
                chunks.append(
                    RawChunk(
                        current_lines,
                        RawChunkType.MARKDOWN,
                        start_line_number,
                        path,
                        report,
                    )
                )
                state = ParserState.HTML
                current_lines = []
                current_lines.append(line)
                start_line_number = line_number
                empty_lines = 0
            elif markdown_start(s_line, empty_lines):
                chunks.append(
                    RawChunk(
                        current_lines,
                        RawChunkType.MARKDOWN,
                        start_line_number,
                        path,
                        report,
                    )
                )
                state = ParserState.MARKDOWN
                current_lines = []
                current_lines.append(line)
                start_line_number = line_number
                empty_lines = 0
            else:
                current_lines.append(line)
                empty_lines = 0
        elif state == ParserState.YAML:
            if is_empty(s_line):
                empty_lines = empty_lines + 1
                current_lines.append(line)
            if (empty_lines > 1) or yaml_stop(s_line):
                previous_yaml_chunk = RawChunk(
                    current_lines,
                    RawChunkType.YAML,
                    start_line_number,
                    path,
                    report,
                )
                empty_lines = 0
                chunks.append(previous_yaml_chunk)
                state = ParserState.AFTER_YAML
                current_lines = []
                start_line_number = line_number + 1
            else:
                current_lines.append(line)
        elif state == ParserState.AFTER_YAML:
            if is_empty(s_line):
                empty_lines = empty_lines + 1
                current_lines.append(line)
                state = ParserState.MARKDOWN
                previous_yaml_chunk = None
            else:
                current_lines.append(line)
                state = ParserState.AFTER_YAML_CONTENT
                empty_lines = 0
        elif state == ParserState.AFTER_YAML_CONTENT:
            if is_empty(s_line):
                empty_lines = empty_lines + 1
                if empty_lines > 1:
                    previous_yaml_chunk.post_yaml = current_lines
                    state = ParserState.MARKDOWN
                    current_lines = []
                else:
                    current_lines.append(line)
                start_line_number = line_number + 1
            else:
                empty_lines = 0
                current_lines.append(line)
        elif state == ParserState.CODE:
            if code_stop(s_line):
                current_lines.append(line)
                chunks.append(
                    RawChunk(
                        current_lines,
                        RawChunkType.CODE,
                        start_line_number,
                        path,
                        report,
                    )
                )
                state = ParserState.MARKDOWN
                current_lines = []
                start_line_number = line_number + 1
            else:
                current_lines.append(line)
        elif state == ParserState.HTML:
            if is_empty(s_line):
                empty_lines = empty_lines + 1
                current_lines.append(line)
            elif html_stop(empty_lines):
                chunks.append(
                    RawChunk(
                        current_lines,
                        RawChunkType.HTML,
                        start_line_number,
                        path,
                        report,
                    )
                )
                state = ParserState.MARKDOWN
                current_lines = []
                current_lines.append(line)
                start_line_number = line_number
                empty_lines = 0
            else:
                current_lines.append(line)
                empty_lines = 0
    # create last chunk
    if state == ParserState.AFTER_YAML_CONTENT:
        previous_yaml_chunk.post_yaml = current_lines
    else:
        def parser_state_to_chunk_type(state: ParserState) -> RawChunkType:
            if state == ParserState.MARKDOWN:
                return RawChunkType.MARKDOWN
            elif (
                (state == ParserState.YAML)
                or (state == ParserState.AFTER_YAML)
            ):
                return RawChunkType.YAML
            elif state == ParserState.HTML:
                return RawChunkType.HTML
            elif state == ParserState.CODE:
                return RawChunkType.CODE
            else:
                assert False

        chunks.append(
            RawChunk(
                current_lines,
                parser_state_to_chunk_type(state),
                start_line_number,
                path,
                report,
            )
        )

    # TODO remove chunks that turn out to be empty
    chunks = [item for item in chunks if not item.is_empty()]
    chunks = expand_reference_chunks(chunks, path, report)
    return chunks


def expand_reference_chunks(
    source_chunks: Sequence[RawChunk], path: Path, report: "Report"
) -> Sequence[RawChunk]:
    # TODO prevent cycles
    target_chunks: Sequence[RawChunk] = []
    for source_chunk in source_chunks:
        path = source_chunk._get_reference()
        if path is not None:
            with open(path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                target_chunks.append(parse(lines, path, report))
        else:
            target_chunks.append(source_chunk)
    return target_chunks
