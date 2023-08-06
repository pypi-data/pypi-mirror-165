from typing import Any, Dict, List
from ... import YAMLChunk, YamlExtension, RawChunk, Builder, ParagraphExtension


class HintParagraphExtension(ParagraphExtension):
    def __init__(self):
        super().__init__("hints", extra_tags=["hint"])


class HintExtension(YamlExtension):
    def __init__(self):
        super().__init__(type=["hints", "hint"], chunk_class=Hint)


class Hint(YAMLChunk):
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
            optional=["title"],
        )
        self.title = dictionary["title"] if "title" in dictionary else ""
        if self.has_post_yaml():
            self.hint = self.get_post_yaml()
        else:
            self.tell(
                "Hint should have a post-yaml section with the content.", self.WARNING
            )
            self.hint = ""

    def to_html(self, builder: Builder):
        html: List[str] = []
        html.append('<button class="w3collapsible">{}</button>'.format(self.title))
        html.append('<div class="w3content">')
        html.append(
            builder.convert(self.hint, target_format="html", source_format="md")
        )
        html.append("</div>")
        return "\n".join(html)

    def to_latex(self, builder: Builder):
        latex: List[str] = []
        # TODO
        return "\n".join(latex)

    def example_1(self):
        """An example to show students a hint."""
        return (
            "---"
            "title: Hint about Something"
            "---"
            "Within the content you can have lists:"
            ""
            "* 10.0.0.0/8"
            "* 172.16.0.0/12"
            "* 192.168.0.0/16"
            ""
            "And you can continue."
            ""
            "**Remember:** Hints should be helpful."
        )
