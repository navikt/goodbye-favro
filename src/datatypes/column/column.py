from src.datatypes.column.favro.column import FavroColumn
from src.datatypes.column.trello.list import TrelloList


class Column:
    def __init__(self, favro_column: FavroColumn, trello_list: TrelloList):
        self.favro = favro_column
        self.trello = trello_list

    def __repr__(self):
        return f"Column(favro={self.favro.id}, trello={self.trello.id})"


def get_column_from_trello_id(columns, trello_id):
    return next((column for column in columns if column.trello.id == trello_id), None)


def get_column_from_favro_id(columns, favro_id) -> Column | None:
    return next((column for column in columns if column.favro.id == favro_id), None)
