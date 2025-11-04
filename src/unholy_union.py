from src.goodbye_favro import Favro
from src.hello_trello import Trello
from src.datatypes import Column, Tag, get_column_from_favro_id, choose_color


class UnholyUnion:
    def __init__(self, trello: Trello, favro: Favro, verbose=False, lanes_to_ignore=None):
        self.trello = trello
        self.favro = favro
        self.verbose = verbose
        self.lanes_to_ignore = lanes_to_ignore if lanes_to_ignore else []
        self.tags = self.__tags()
        self.columns = self.__columns()
        self.cards = self.__cards()

    def __tags(self):
        trello_labels = self.trello.labels
        favro_tags = self.favro.tags
        print(
            f"Found {len(favro_tags)} Favro tags and {len(trello_labels)} Trello labels"
        )
        ret_tags = []
        for favro_tag in favro_tags:
            color = choose_color(favro_tag)
            trello_label = next(
                (
                    label
                    for label in trello_labels
                    if label.name == favro_tag.name and label.color == color
                ),
                None,
            )
            if not trello_label:
                trello_label = self.trello.create_label(favro_tag.name, color)
                if not trello_label:
                    continue
            ret_tags.append(Tag(favro_tag, trello_label))
        return ret_tags

    def __columns(self):
        trello_lists = self.trello.lists
        favro_columns = self.favro.columns
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
        trello_cards = self.trello.cards
        favro_cards = self.favro.cards
        print(
            f"Found {len(favro_cards)} Favro cards and {len(trello_cards)} Trello cards"
        )

        unified_cards = []
        position_adjustment = abs(min(x.position for x in favro_cards))
        for favro_card in reversed(favro_cards):
            tags = [x for x in self.tags if x.favro.id in favro_card.tags]
            trello_card = next(
                (
                    trello_card
                    for trello_card in trello_cards
                    if trello_card.name == favro_card.name
                ),
                None,
            )
            if favro_card.lane_id in self.lanes_to_ignore:
                if self.verbose:
                    print(f"Ignoring card {favro_card.name} in lane {favro_card.lane_id}")
                continue
            if not trello_card:
                column = get_column_from_favro_id(self.columns, favro_card.column_id)
                if not column:
                    print(
                        f"Column with ID {favro_card.column_id} not found in Trello.... weird"
                    )
                    exit(1)
                trello_card = self.trello.create_card(
                    position_adjustment, favro_card, column.trello.id, tags
                )
                if not trello_card:
                    continue
            unified_cards.append(trello_card)

        return sorted(unified_cards, key=lambda x: x.pos)
