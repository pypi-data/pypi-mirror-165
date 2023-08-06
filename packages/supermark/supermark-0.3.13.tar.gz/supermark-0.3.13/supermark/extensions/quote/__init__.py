import os
from typing import Any, Dict, Optional, Sequence

from ... import YAMLChunk, YamlExtension, RawChunk, Builder


class QuoteExtension(YamlExtension):
    def __init__(self):
        super().__init__(type="quote", chunk_class=Quote)


class Quote(YAMLChunk):
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
            required=None,
            optional=["link", "title"],
        )

    def to_html(self, builder: Builder):
        html: Sequence[str] = []

        link = self.dictionary["link"] if "link" in self.dictionary else None
        title = self.dictionary["title"] if "title" in self.dictionary else None

        html.append('<div class="quotedoc shadow-sm mt-5 mb-5 bg-light rounded">')
        if link is not None:
            html.append(
                f'<div class="quotetitle"><a href="{link}"><i class="bi bi-arrow-right-circle-fill"></i>&nbsp;{title}</a></div>'
            )
        html.append('<div class="quotecontent">')
        if self.has_post_yaml():
            html.append(
                builder.convert(
                    self.get_post_yaml(), target_format="html", source_format="md"
                )
            )
        html.append("</div>")
        html.append("</div>")
        return "\n".join(html)
