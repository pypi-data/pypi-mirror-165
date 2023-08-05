from ... import YAMLChunk, YamlExtension, Builder, RawChunk
from typing import Dict, Any, List


class LinesExtension(YamlExtension):
    def __init__(self):
        super().__init__(type="lines", chunk_class=Lines)
        # print("-------- foudn lines extension")


class Lines(YAMLChunk):
    def __init__(
        self,
        raw_chunk: RawChunk,
        dictionary: Dict[str, Any],
        page_variables: Dict[str, Any],
    ):
        # print("--------     init lines extension")
        super().__init__(raw_chunk, dictionary, page_variables, required=["lines"])

    def to_html(self, builder: Builder):
        html: List[str] = []
        for _ in range(self.dictionary["lines"]):
            html.append('<hr class="lines"/>')
        return "\n".join(html)
