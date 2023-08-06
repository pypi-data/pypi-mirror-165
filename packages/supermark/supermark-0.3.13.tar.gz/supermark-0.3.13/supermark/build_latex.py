# from pathlib import Path
# from typing import Sequence
# from yaml import SafeLoader, load_all

# from .chunks import HTMLChunk, MarkdownChunk, YAMLDataChunk
# from .code import Code
# from .core import arrange_assides
# from .figure import Figure
# from .parse import ParserState, parse
# from .report import Report, print_reports
# from .table import Table
# from .video import Video

# from typing import TYPE_CHECKING

# if TYPE_CHECKING:
#     from . import extensions


# def write_file(html: str, target_file_path: Path, report: Report):
#     encoding = "utf-8"
#     try:
#         with open(target_file_path, "w", encoding=encoding) as html_file:
#             html_file.write(html)
#     except UnicodeEncodeError as error:
#         report.tell("Encoding error when writing file {}.".format(target_file_path))
#         text = error.object
#         character = text[error.start : error.end]
#         line = html.count("\n", 0, error.start) + 1
#         report.tell(
#             "Character {} in line {} cannot be saved with encoding {}.".format(
#                 character, line, encoding
#             )
#         )
#         with open(
#             target_file_path, "w", encoding=encoding, errors="ignore"
#         ) as html_file:
#             html_file.write(html)


# def default_html_template() -> str:
#     html: Sequence[str] = []
#     html.append("{content}")
#     return "\n".join(html)


# def load_html_template(template_path: Path, report: Report):
#     try:
#         with open(
#             template_path, "r", encoding="utf-8", errors="surrogateescape"
#         ) as templatefile:
#             template = templatefile.read()
#             report.tell("Loading template {}.".format(template_path), Report.INFO)
#             return template
#     except FileNotFoundError:
#         report.tell(
#             "Template file missing. Expected at {}. Using default template.".format(
#                 template_path
#             ),
#             Report.WARNING,
#         )
#     return default_html_template()


# class Builder:
#     def __init__(self, yaml, base_path: Path):
#         self.yaml = yaml
#         self.base_path = base_path
#         self.output_file = self.base_path / yaml["output"]
#         self.template_file = Path(
#             "/Users/kraemer/Dropbox/Education/SUPERMARK/latex-fr1.tex"
#         )

#     def to_latex(self) -> None:
#         reports = []
#         report = Report(None)
#         latex = []
#         latex.append(load_html_template(self.template_file, report))
#         for element in self.yaml["content"]:
#             if element["type"] == "chapter":
#                 latex.append(r"\chapter{{{}}}".format(element["name"]))
#                 for doc in element["content"]:
#                     source_file_path = self.base_path / "pages" / doc
#                     if source_file_path.is_file() and source_file_path.exists():
#                         with open(source_file_path, "r", encoding="utf-8") as file:
#                             file_report = Report(source_file_path)
#                             reports.append(file_report)
#                             lines = file.readlines()
#                             file_report.tell("{}".format(source_file_path), Report.INFO)
#                             latex.append(
#                                 self.transform_page_to_latex(
#                                     lines, source_file_path, False, file_report
#                                 )
#                             )
#                 latex.append("\\clearpage\\newpage")
#         latex.append(r"\end{document}")
#         latex = "\n".join(latex)
#         target_file_path = self.output_file
#         write_file(latex, target_file_path, report)

#     def transform_page_to_latex(
#         self, lines: Sequence[str], filepath: Path, abort_draft: bool, report: Report
#     ) -> str:
#         chunks = parse(lines, filepath, report)
#         chunks = extensions.cast(chunks)
#         chunks = arrange_assides(chunks)

#         content = []
#         # content.append('<div class="page">')
#         if len(chunks) == 0:
#             pass
#         else:
#             first_chunk = chunks[0]
#             if isinstance(first_chunk, MarkdownChunk) and not first_chunk.is_section:
#                 # content.append('    <section class="content">')
#                 pass

#         for chunk in chunks:
#             latex = chunk.to_latex(self)
#             if latex is not None:
#                 content.append(latex)
#             for aside in chunk.asides:
#                 latex = aside.to_latex(self)
#                 if latex is not None:
#                     content.append(latex)
#         latex = "\n".join(content)
#         return latex


# def build_latex(build_file: Path, base_path: Path):
#     with open(build_file) as file:
#         for doc in load_all(file, Loader=SafeLoader):
#             b = Builder(doc, base_path)
#             b.to_latex()
