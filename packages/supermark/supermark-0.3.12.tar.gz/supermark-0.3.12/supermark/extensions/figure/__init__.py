import os
from typing import Any, Dict, Optional, Sequence

from ... import YAMLChunk, YamlExtension, RawChunk, Builder


class FigureExtension(YamlExtension):
    def __init__(self):
        super().__init__(type="figure", chunk_class=Figure)


class Figure(YAMLChunk):
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
            required=["source"],
            optional=["caption", "link"],
        )
        if dictionary["source"].startswith("http://") or dictionary[
            "source"
        ].startswith("https://"):
            self.tell(
                "Refer to remote figure: {}".format(dictionary["source"]),
                level=self.WARNING,
            )
        else:
            self.file_path = os.path.join(
                os.path.dirname(os.path.dirname(raw_chunk.path)), dictionary["source"]
            )
            if not os.path.exists(self.file_path):
                self.tell(
                    "Figure file {} does not exist.".format(self.file_path),
                    level=self.WARNING,
                )

    def to_html(self, builder: Builder):
        html: Sequence[str] = []
        html.append('<div class="figure">')
        if "caption" in self.dictionary:
            if "link" in self.dictionary:
                html.append(
                    '<a href="{}"><img src="{}" alt="{}" width="100%"/></a>'.format(
                        self.dictionary["link"],
                        self.dictionary["source"],
                        self.dictionary["caption"],
                    )
                )
            else:
                html.append(
                    '<img src="{}" alt="{}" width="100%"/>'.format(
                        self.dictionary["source"], self.dictionary["caption"]
                    )
                )
            html.append(
                '<span name="{}">&nbsp;</span>'.format(self.dictionary["source"])
            )
            html_caption: str = builder.convert(
                self.dictionary["caption"], target_format="html", source_format="md"
            )
            html.append(
                '<aside name="{}"><p>{}</p></aside>'.format(
                    self.dictionary["source"], html_caption
                )
            )
        else:
            if "link" in self.dictionary:
                html.append(
                    '<a href="{}"><img src="{}" width="100%"/></a>'.format(
                        self.dictionary["link"], self.dictionary["source"]
                    )
                )
            else:
                html.append(
                    '<img src="{}" width="100%"/>'.format(self.dictionary["source"])
                )
        html.append("</div>")
        return "\n".join(html)

    def to_latex(self, builder: Builder) -> Optional[str]:
        s: Sequence[str] = []
        s.append("\\begin{figure}[htbp]")
        # s.append('\\begin{center}')
        # file = '../' + self.dictionary['source']
        figure_file = self.raw_chunk.parent_path / self.dictionary["source"]
        # print(figure_file.suffix)
        if figure_file.suffix == ".gif":
            self.tell(
                "Figure file {} in gif format is not compatible with LaTeX.".format(
                    self.file_path
                ),
                level=self.WARNING,
            )
            return None
        if figure_file.suffix == ".svg":
            # file = Path(file)
            target_path = self.get_dir_cached() / "{}.pdf".format(figure_file.stem)
            if not target_path.exists():
                import cairosvg
                # file = self.raw_chunk.parent_path / self.dictionary['source']
                cairosvg.svg2pdf(url=str(figure_file), write_to=str(target_path))
            # s.append('\\includegraphics[width=\\linewidth]{{{}}}%'.format(target_path))
            figure_file = target_path
        figure_file = figure_file.relative_to(builder.output_file.parent)
        # print('figure_file: {}'.format(figure_file))
        s.append("\\includegraphics[width=\\linewidth]{{{}}}%".format(figure_file))
        if "caption" in self.dictionary:
            s.append(
                "\\caption{{{}}}".format(
                    builder.convert(
                        self.dictionary["caption"],
                        target_format="latex",
                        source_format="md",
                    )
                )
            )
        s.append("\\label{default}")
        # s.append('\\end{center}')
        s.append("\\end{figure}")
        return "\n".join(s)
