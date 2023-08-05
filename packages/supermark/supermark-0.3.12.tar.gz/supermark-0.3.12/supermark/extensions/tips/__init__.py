from ... import ParagraphExtension


class TipsParagraphExtension(ParagraphExtension):
    def __init__(self):
        super().__init__("tips", extra_tags=["tip"])
