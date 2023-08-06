from ... import ParagraphExtension


class WarningParagraphExtension(ParagraphExtension):
    def __init__(self):
        super().__init__("warning", extra_tags=["warn"])
