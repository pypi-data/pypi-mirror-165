import os
import re
from ...extend import TableClassExtension, Extension
from typing import Any, Dict, List, Optional, Sequence, Set

import wikitextparser as wtp
from wikitextparser._table import Cell

from ... import Chunk, YAMLChunk, YamlExtension, RawChunk, Builder


class TableExtension(YamlExtension):
    def __init__(self):
        super().__init__(type="table", chunk_class=Table)


IGNORED_CLASSES = ["table", "table-sm", "table-bordered"]


def extract_main_table_class(attribute: str) -> Optional[str]:
    for token in attribute.split():
        if token not in IGNORED_CLASSES:
            return token
    return None


class Table(YAMLChunk):
    def __init__(
        self,
        raw_chunk: RawChunk,
        dictionary: Dict[str, Any],
        page_variables: Dict[str, Any],
    ):
        super().__init__(
            raw_chunk,
            dictionary,
            page_variables,
            required=[],
            optional=["file", "class", "caption", "format"],
        )
        if "class" in dictionary:
            self.div_class = extract_main_table_class(dictionary["class"])
        else:
            self.div_class = None

        if self.has_post_yaml():
            self.table_raw = self.get_post_yaml()
        elif "file" in dictionary:
            file_path = os.path.join(
                os.path.dirname(os.path.dirname(raw_chunk.path)), dictionary["file"]
            )
            if not os.path.exists(file_path):
                self.error("Table file {} does not exist.".format(file_path))
                self.ok = False
            else:
                with open(file_path, "r") as myfile:
                    self.table_raw = myfile.read()
        else:
            self.error("Table must either refer to a file or have a post-yaml section.")
            self.ok = False

    def add_used_extension(self, used_extensions: Set[Extension], core: Any):
        if self.div_class is not None:
            self.table_extension: Optional[
                TableClassExtension
            ] = core.tableclass_extension_point.get_table_class(self.div_class)
            if self.table_extension is None:
                self.warning(f"No extension found for table class '{self.div_class}'.")
            else:
                used_extensions.add(self.table_extension)
        else:
            self.table_extension = None

    def _cell_to_html(
        self, cell: str, source_format: str, empty_cell: str, builder: Builder
    ) -> str:
        if len(cell) == 0:
            return empty_cell
        elif source_format == "html":
            return cell
        else:
            return builder.convert(
                cell, target_format="html", source_format=source_format
            )

    def _cellwise_to_html(
        self, source_format: str, empty_cell: str, builder: Builder
    ) -> str:
        def get_colspan(cell: Cell):
            if "colspan" in cell.attrs:
                return ' colspan="{}"'.format(cell.attrs["colspan"])
            return ""

        def get_rowspan(cell: Cell):
            if "rowspan" in cell.attrs:
                return ' rowspan="{}"'.format(cell.attrs["rowspan"])
            return ""

        def get_class(cell: Cell):
            if "class" in cell.attrs:
                return ' class="{}"'.format(cell.attrs["class"])
            return ""

        output: Sequence[str] = []
        parsed = wtp.parse(self.table_raw)
        rows = parsed.tables[0].cells(span=False)
        if self.div_class:
            output.append('<table class="{} table table-sm">'.format(self.div_class))
        else:
            output.append('<table class="table table-sm">')
        for row in rows:
            output.append("<tr>")
            for cell in row:
                c = self._cell_to_html(
                    cell.value.strip(), source_format, empty_cell, builder
                )
                if cell.is_header:
                    output.append(
                        "<th"
                        + get_rowspan(cell)
                        + get_colspan(cell)
                        + get_class(cell)
                        + ">"
                        + c
                        + "</th>"
                    )
                else:
                    output.append(
                        "<td"
                        + get_rowspan(cell)
                        + get_colspan(cell)
                        + get_class(cell)
                        + ">"
                        + c
                        + "</td>"
                    )
            output.append("</tr>")

        output.append("</table>")
        return "\n".join(output)

    def to_html(self, builder: Builder) -> str:
        empty_cell = (
            ""
            if self.table_extension is None
            else self.table_extension.get_empty_cell()
        )
        html: Sequence[str] = []

        if "format" in self.dictionary:
            source_format = self.dictionary["format"]
        else:
            source_format = "md"
        output = self._cellwise_to_html(source_format, empty_cell, builder)
        html.append(output)
        if "caption" in self.dictionary:
            if "file" in self.dictionary:
                table_id = self.dictionary["file"]
            else:
                table_id = Chunk.create_hash(self.table_raw)
            html.append('<span name="{}">&nbsp;</span>'.format(table_id))
            html.append(
                '<aside name="{}"><p>{}</p></aside>'.format(
                    table_id,
                    builder.convert(self.dictionary["caption"], target_format="html"),
                )
            )
        return "\n".join(html)

    def get_scss(self):
        return """section {
                    border:1px solid #e5e5e5;
                    border-width:1px 0;
                    padding:20px 0;
                    margin:0 0 20px;
                  }"""

    def to_latex(self, builder: Builder) -> str:
        parsed = wtp.parse(self.table_raw)
        rows = parsed.tables[0].data()
        rowspec = ""
        for _ in rows[0]:
            rowspec = rowspec + "L"
        latex: Sequence[str] = []
        latex.append("\\begin{table*}[t]")
        latex.append("\\begin{tabulary}{\\textwidth}" + "{{{}}}".format(rowspec))
        latex.append("\\toprule")

        source_format = (
            self.dictionary["format"] if "format" in self.dictionary else "mediawiki"
        )

        for row in rows:
            resolved_row: List[str] = []
            for x in row:
                resolved_row.append(
                    builder.convert(
                        x, target_format="latex", source_format=source_format
                    )
                )
            latex.append("&".join(resolved_row) + "\\\\")
        latex.append("\\bottomrule")
        latex.append("\\end{tabulary}")
        if "caption" in self.dictionary:
            latex.append(
                "\\caption{{{}}}".format(
                    builder.convert(
                        self.dictionary["caption"],
                        target_format="latex",
                        source_format="md",
                    )
                )
            )
        if "label" in self.dictionary:
            latex.append("\\label{{{}}}".format(self.dictionary["label"]))
        latex.append("\\end{table*}")
        # extra_args = ['--from', 'mediawiki', '--to', 'latex']
        # output = pypandoc.convert_text(self.table_raw, 'latex', format='md', extra_args=extra_args)
        return "\n".join(latex)
