from ... import TableClassExtension


class WeekplanTableClassExtension(TableClassExtension):
    def __init__(self):
        super().__init__("coursetable", empty_cell="")
