from typing import Any, Dict, List

from pygments import highlight
from pygments.formatters import LatexFormatter
from pygments.lexers import get_lexer_by_name

from .chunks import Builder, Chunk, RawChunk


class Code(Chunk):
    def __init__(self, raw_chunk: RawChunk, page_variables: Dict[str, Any]):
        super().__init__(raw_chunk, page_variables)
        if self.get_first_line().startswith("```"):
            self.lang = self.get_first_line().replace("```", "").strip()
            self.code = "".join(self.raw_chunk.lines[1:-1])
        else:
            self.lang = None
            self.code = self.get_content()

    def get_chunk_type(self) -> str:
        return "code" if self.lang is None else f"code/{self.lang}"

    def to_html(self, builder: Builder) -> str:
        return builder.convert_code(self.get_content(), target_format="html")

    def to_latex(self, builder: Builder) -> str:
        lexer = None
        if self.lang is not None:
            try:
                lexer = get_lexer_by_name(self.lang, stripall=True)
            except Exception as e:
                print(e)
        output: List[str] = []
        if lexer is not None:
            formatter = LatexFormatter(linenos=False, verboptions="breaklines")
            output.append(highlight(self.code, lexer, formatter))
        else:
            output.append(r"\begin{Verbatim}[breaklines]")
            output.append(self.code)
            output.append(r"\end{Verbatim}")
        return "\n".join(output)

    def recode(self) -> str:
        # import was failing on Github actions, therefore here
        import black

        if self.get_first_line().startswith("```"):
            lang = self.get_first_line().replace("```", "").strip()
            code = "".join(self.raw_chunk.lines[1:-1])
            if lang == "python":
                try:
                    code = black.format_str(code, mode=black.Mode())
                except black.InvalidInput as e:
                    print(e)
            return "```" + lang + "\n" + code + "```"
        else:
            return self.get_content()
