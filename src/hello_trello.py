import re
from requests_ratelimiter import LimiterSession

from src.datatypes import (
    TrelloCard,
    TrelloList,
    TrelloLabel,
    FavroCard,
    TrelloChecklist,
    Tag,
)


class ResourceType:
    BOARDS = "boards"
    LISTS = "lists"
    CARDS = "cards"
    LABELS = "labels"
    CHECKLISTS = "checklists"


class Trello:
    def __init__(self, config):
        self.api_key = config.api_key
        self.api_token = config.api_token
        self.board_id = config.board_id

        # https://support.atlassian.com/trello/docs/api-rate-limits/
        # States no more than 100 requests per 10 seconds,
        # so a limit of 400 per minute (66 per 10 seconds) should be safe :)
        self.session = LimiterSession(per_minute=400)

        self.cards = self.get_cards()
        self.lists = self.get_lists()
        self.labels = self.get_labels()

    def __get_resource(self, api_endpoint: str, params: dict | None = None) -> list:
        response = self.session.get(
            f"https://api.trello.com/1/{api_endpoint}",
            params={**params, "key": self.api_key, "token": self.api_token}
            if params
            else {"key": self.api_key, "token": self.api_token},
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(
                f"Error fetching {api_endpoint}: {response.status_code} - {response.text}"
            )
            return []

    def __post_resource(
        self, api_endpoint: str, params: dict[str, str] | None = None, ret_type=None
    ):
        response = self.session.post(
            f"https://api.trello.com/1/{api_endpoint}",
            params={**params, "key": self.api_key, "token": self.api_token}
            if params
            else {"key": self.api_key, "token": self.api_token},
        )
        if response.status_code == 200:
            if ret_type:
                return ret_type(response.json())
            return response.json()
        else:
            print(
                f"Error fetching {api_endpoint}: {response.status_code} - {response.text}"
            )
            return None

    def __delete_resource(
        self, api_endpoint: str, params: dict[str, str] | None = None, ret_type=None
    ):
        response = self.session.delete(
            f"https://api.trello.com/1/{api_endpoint}",
            params={**params, "key": self.api_key, "token": self.api_token}
            if params
            else {"key": self.api_key, "token": self.api_token},
        )
        if response.status_code == 200:
            if ret_type:
                return ret_type(response.json())
            return response.json()
        else:
            print(
                f"Error fetching {api_endpoint}: {response.status_code} - {response.text}"
            )
            return None

    def __to_type(
        self,
        datatype,
        json_data: list[dict[str, object]],
    ) -> list[object]:
        return [datatype(x) for x in json_data]  # TODO: fix the type hinting

    def get_board(self):
        return self.__get_resource(f"{ResourceType.BOARDS}/{self.board_id}")

    def get_lists(self) -> list:
        return self.__to_type(
            TrelloList,
            self.__get_resource(
                f"{ResourceType.BOARDS}/{self.board_id}/{ResourceType.LISTS}",
            ),
        )

    def get_cards(self) -> list:
        return self.__to_type(
            TrelloCard,
            self.__get_resource(
                f"{ResourceType.BOARDS}/{self.board_id}/{ResourceType.CARDS}",
            ),
        )

    def get_labels(self) -> list:
        return self.__to_type(
            TrelloLabel,
            self.__get_resource(
                f"{ResourceType.BOARDS}/{self.board_id}/{ResourceType.LABELS}"
            ),
        )

    def create_list(self, name: str, pos: float | None = None) -> TrelloList | None:
        print(f"Creating Trello list for Favro column: {name} at position {pos}")
        params = {
            "name": name,
            "pos": pos,
            "idBoard": self.board_id,
            "key": self.api_key,
            "token": self.api_token,
        }
        trello_list = self.__post_resource(ResourceType.LISTS, params)
        if trello_list:
            return TrelloList(trello_list)
        else:
            print(f"Failed to create Trello list for {name}")
            return None

    def checklist_items(self, favro_card: FavroCard):
        description_lines = favro_card.description.split("\n")
        description = ""
        checklist_items = []
        for line in description_lines:
            matched = re.match(r"\s?+-\s?+\[[x\s]]\s?+(.*)", line)
            if matched:
                item = matched.group(1)
                checklist_items.append(("[x]" in item, item))
            else:
                description += f"{line}\n"
        return description, checklist_items

    def create_checklist(
        self, trello_card: TrelloCard, checklist_items: list[tuple[bool, str]]
    ):
        checklist = self.__post_resource(
            f"{ResourceType.CHECKLISTS}",
            params={"idCard": trello_card.id, "name": "To do"},
        )
        if checklist:
            checklist = TrelloChecklist(
                self.session, self.api_key, self.api_token, checklist
            )
            for checked, name in checklist_items:
                checklist.create_item(checked, name)

    def delete_all_tags(self):
        tags = [
            TrelloLabel(x)
            for x in self.__get_resource(
                f"{ResourceType.BOARDS}/{self.board_id}/{ResourceType.LABELS}",
                params={"limit": 1000},
            )
        ]
        for tag in tags:
            self.__delete_resource(f"{ResourceType.LABELS}/{tag.id}")
        print("Deleted all tags :)")

    def create_card(
        self,
        position_adjustment: float,
        favro_card: FavroCard,
        trello_list_id: str,
        tags: list[Tag],
    ) -> TrelloCard | None:
        description, checklist_items = self.checklist_items(favro_card)
        print(f"Creating Trello card: {favro_card.name} in list {trello_list_id}")
        params = {
            "name": favro_card.name,
            "desc": description,
            "idList": trello_list_id,
            "key": self.api_key,
            "pos": int((position_adjustment + favro_card.position + 1) * 10),
            "idLabels": [x.trello.id for x in tags],
            "token": self.api_token,
        }
        trello_card = self.__post_resource(ResourceType.CARDS, params)
        if trello_card:
            ret = TrelloCard(trello_card)
            if len(checklist_items) > 0:
                self.create_checklist(ret, checklist_items)
            return ret
        else:
            print(f"Failed to create Trello card for {favro_card.name}")
            return None

    def create_label(self, name: str, color: str) -> TrelloLabel | None:
        print(f"Creating Trello label: {name} with color {color}")
        params = {
            "name": name,
            "color": color,
            "key": self.api_key,
            "token": self.api_token,
        }
        trello_label = self.__post_resource(
            f"{ResourceType.BOARDS}/{self.board_id}/{ResourceType.LABELS}", params
        )
        if trello_label:
            return TrelloLabel(trello_label)
        else:
            print(f"Failed to create Trello label for {name}")
            return None
