from ... import ParagraphExtension


class FactBoxParagraphExtension(ParagraphExtension):
    def __init__(self):
        super().__init__("factbox", extra_tags=["note-box"])
