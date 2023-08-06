from typing import Any, Dict, Sequence
from ... import YamlExtension, YAMLChunk, RawChunk, Builder

TEMPLATE = """<p>
<div class="accordion" id="{element_id}">
  <div class="accordion-item">
    <p class="accordion-header" id="{element_id}A">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#{element_id}C" aria-expanded="false" aria-controls="{element_id}C">{question}</button>
    </p>
    <div id="{element_id}C" class="accordion-collapse collapse" aria-labelledby="{element_id}A" data-bs-parent="#{element_id}">
      <div class="accordion-body">{answer}</div>
    </div>
  </div>
</div>
</p>"""


class ButtonExtension(YamlExtension):
    def __init__(self):
        super().__init__(type="qna", chunk_class=QnA)


class QnA(YAMLChunk):
    def __init__(
        self,
        raw_chunk: RawChunk,
        dictionary: Dict[str, Any],
        page_variables: Dict[str, Any],
    ):
        super().__init__(raw_chunk, dictionary, page_variables, required=["q"])
        self.question: str = dictionary["q"]
        if self.has_post_yaml():
            self.answer: str = self.get_post_yaml()
        else:
            self.ok = False
            self.error("A QnA requires ans answer as post-yaml section.")

    def to_html(self, builder: Builder):
        element_id = "id" + self.raw_chunk.get_hash()
        return TEMPLATE.format_map(
            {
                "element_id": element_id,
                "question": self.question,
                "answer": builder.convert(self.answer, "html"),
            }
        )
