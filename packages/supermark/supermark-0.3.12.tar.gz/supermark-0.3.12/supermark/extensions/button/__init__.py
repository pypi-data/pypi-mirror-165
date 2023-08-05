from typing import Any, Dict, Sequence
from ... import YamlExtension, YAMLChunk, RawChunk, Builder


class ButtonExtension(YamlExtension):
    def __init__(self):
        super().__init__(type="button", chunk_class=Button)


class Button(YAMLChunk):
    def __init__(
        self,
        raw_chunk: RawChunk,
        dictionary: Dict[str, Any],
        page_variables: Dict[str, Any],
    ):
        super().__init__(
            raw_chunk, dictionary, page_variables, required=["url", "text"]
        )

    def to_html(self, builder: Builder):
        clazz = "ntnu-button"
        html: Sequence[str] = []
        html.append(
            '<a class="{}" href="{}">{}</a>'.format(
                clazz, self.dictionary["url"], self.dictionary["text"]
            )
        )
        return "\n".join(html)
