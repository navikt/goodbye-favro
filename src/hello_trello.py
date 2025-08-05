from requests_ratelimiter import LimiterSession

from src.datatypes import TrelloCard
from src.datatypes import TrelloList


class ResourceType:
    BOARDS = "boards"
    LISTS = "lists"
    CARDS = "cards"


class Trello:
    def __init__(self, config):
        self.api_key = config.api_key
        self.api_token = config.api_token
        self.board_id = config.board_id

        # https://support.atlassian.com/trello/docs/api-rate-limits/
        # States no more than 100 requests per 10 seconds,
        # so a limit of 400 per minute (66 per 10 seconds) should be safe :)
        self.session = LimiterSession(per_minute=400)

    def __get_resource(self, api_endpoint, params=None):
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
            return None

    def __post_resource(self, api_endpoint, params=None):
        response = self.session.post(
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
            return None

    def __to_type(self, datatype, json_data):
        return [datatype(x) for x in json_data]

    def get_board(self):
        return self.__get_resource(f"{ResourceType.BOARDS}/{self.board_id}")

    def get_lists(self):
        return self.__to_type(
            TrelloList,
            self.__get_resource(
                f"{ResourceType.BOARDS}/{self.board_id}/{ResourceType.LISTS}",
            ),
        )

    def get_cards(self):
        return self.__to_type(
            TrelloCard,
            self.__get_resource(
                f"{ResourceType.BOARDS}/{self.board_id}/{ResourceType.CARDS}",
            ),
        )

    def create_list(self, name, pos=None):
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

    def create_card(self, name, trello_list_id):
        print(f"Creating Trello card: {name} in list {trello_list_id}")
        params = {
            "name": name,
            "idList": trello_list_id,
            "key": self.api_key,
            "token": self.api_token,
        }
        trello_card = self.__post_resource(ResourceType.CARDS, params)
        if trello_card:
            return TrelloCard(trello_card)
        else:
            print(f"Failed to create Trello card for {name}")
            return None
