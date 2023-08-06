from ... import TableClassExtension

# add table class="weekplan table table-sm table-bordered"


class WeekplanTableClassExtension(TableClassExtension):
    def __init__(self):
        super().__init__("weekplan", empty_cell="")
