from ... import ParagraphExtension


class AbstractParagraphExtension(ParagraphExtension):
    def __init__(self):
        super().__init__("abstract", extra_tags=["summary"])
