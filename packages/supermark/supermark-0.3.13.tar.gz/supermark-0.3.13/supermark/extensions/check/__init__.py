from ... import ParagraphExtension


class CheckParagraphExtension(ParagraphExtension):
    def __init__(self):
        super().__init__("check", extra_tags=["todo"])
