from src.goodbye_favro import Favro
from src.hello_trello import Trello
from src.datatypes import Column, get_column_from_favro_id


class UnholyUnion:
    def __init__(self, trello: Trello, favro: Favro):
        self.trello = trello
        self.favro = favro
        self.columns = self.__columns()
        self.cards = self.__cards()

    def __columns(self):
        trello_lists = self.trello.get_lists()
        favro_columns = self.favro.get_columns()
        unified_columns = []
        for column in favro_columns:
            trello_list = next(
                (
                    trello_list
                    for trello_list in trello_lists
                    if trello_list.name == column.name
                    and trello_list.pos == column.position + 1
                ),
                None,
            )
            if not trello_list:
                trello_list = self.trello.create_list(column.name, column.position + 1)
                if not trello_list:
                    continue
            unified_columns.append(Column(column, trello_list))

        return sorted(unified_columns, key=lambda x: x.trello.pos)

    def __cards(self):
        trello_cards = self.trello.get_cards()
        favro_cards = self.favro.get_cards(self.columns)
        print(
            f"Found {len(favro_cards)} Favro cards and {len(trello_cards)} Trello cards"
        )
        exit() # TODO: remove this
        unified_cards = []
        for card in favro_cards:
            trello_card = next(
                (
                    trello_card
                    for trello_card in trello_cards
                    if trello_card.name == card.name
                ),
                None,
            )
            if not trello_card:
                trello_list_id = get_column_from_favro_id(self.columns, card.column_id)
                if not trello_list_id:
                    print(
                        f"Column with ID {card.column_id} not found in Trello.... weird"
                    )
                    exit() # TODO: remove this line
                trello_card = self.trello.create_card(
                    card.name, trello_list_id.trello.id
                )
                if not trello_card:
                    continue
            unified_cards.append(trello_card)

        return sorted(unified_cards, key=lambda x: x.pos)
