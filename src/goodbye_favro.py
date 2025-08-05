from requests_ratelimiter import LimiterSession

from src.datatypes import FavroColumn, FavroCard, Column, FavroLane


class ResourceType:
    CARDS = "cards"
    TAGS = "tags"
    COLUMNS = "columns"
    WIDGETS = "widgets"


class Favro:
    def __init__(self, config):
        self.user_id = config.user_id
        self.user_token = config.user_token
        self.organization_id = config.organization_id
        self.widget_id = config.widget_id

        # https://favro.com/developer/#rate-limiting-and-throttling
        # States no more than 10000 requests per hour for the enterprise plan,
        # and 1000 requests per hour for the standard plan.
        # You may look at your plan in your organization settings.
        # Administratoin -> Billing
        # and adjust the limit if you need to fire 10000 requests per hour.
        self.session = LimiterSession(per_hour=1000)
        self.session.auth = (self.user_id, self.user_token)
        self.session.headers.update(
            {
                "organizationId": self.organization_id,
            }
        )

        self.__widget = self.get_widget()
        if not self.__widget:
            print("Favro widget not found, exiting...")
            exit(1)
        self.lanes = [FavroLane(lane) for lane in self.__widget["lanes"]]
        self.columns = self.get_columns()
        self.cards = self.get_cards(self.columns)

    def __get_resource(self, api_endpoint, params=None):
        resource = []
        should_stop = False
        page = 0
        while not should_stop:
            response = self.session.get(
                f"https://favro.com/api/v1/{api_endpoint}",
                params={**params, "page": page} if params else {"page": page},
            )
            if response.status_code == 200:
                data = response.json()
                resource.extend(data["entities"])
                page += 1
                if data["pages"] == page:
                    should_stop = True
            else:
                print(
                    f"Error fetching {api_endpoint}: {response.status_code} - {response.text}"
                )
                should_stop = True
        return resource

    def __to_type(self, datatype, json_data):
        return [datatype(x) for x in json_data]

    @staticmethod
    def lookup_card_id(card_id, cards):
        if card_id is None:
            return None
        for card in cards:
            if card.id == card_id:
                return card
        return None

    def get_cards(self, columns: list[FavroColumn]):
        cards = []
        lane_ids = [lane.id for lane in self.lanes]
        for column in columns:
            column_cards = self.__to_type(
                FavroCard,
                self.__get_resource(
                    ResourceType.CARDS,
                    {
                        "widgetCommonId": self.widget_id,
                        "columnId": column.id,
                        "descriptionFormat": "markdown",
                    },
                ),
            )
            cards.extend(column_cards)

        ret_cards = [
            card
            for card in cards
            if (
                (card.lane_id is not None and card.lane_id in lane_ids)
                and (
                    (
                        card.parent_card_id is None
                        and card.archived is False
                        and card.column_id is not None
                    )
                    or (
                        (a := self.lookup_card_id(card.parent_card_id, cards))
                        is not None
                        and a.archived is False
                    )
                )
            )
        ]
        return ret_cards

    def get_widget(self):
        response = self.session.get(
            f"https://favro.com/api/v1/{ResourceType.WIDGETS}/{self.widget_id}"
        )
        if response.status_code == 200:
            data = response.json()
            return data
        print(
            f"Error fetching {ResourceType.WIDGETS}/{self.widget_id}: {response.status_code} - {response.text}"
        )
        return None

    def get_tags(self):
        return self.__get_resource(ResourceType.TAGS)

    def get_columns(self):
        return self.__to_type(
            FavroColumn,
            self.__get_resource(
                ResourceType.COLUMNS,
                {
                    "widgetCommonId": self.widget_id,
                },
            ),
        )
