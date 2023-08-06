from ... import TableClassExtension


class RubricTableClassExtension(TableClassExtension):
    def __init__(self):
        super().__init__("rubric", empty_cell="&nbsp;")
