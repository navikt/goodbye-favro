class FavroConfig:
    def __init__(self, user_id, user_token, organization_id, widget_id):
        self.user_id = user_id
        self.user_token = user_token
        self.organization_id = organization_id
        self.widget_id = widget_id


class TrelloConfig:
    def __init__(self, api_key, api_token, board_id):
        self.api_key = api_key
        self.api_token = api_token
        self.board_id = board_id


class Config:
    def __init__(self, parsed_config):
        self.favro = FavroConfig(
            user_id=parsed_config["favro"]["user_id"],
            user_token=parsed_config["favro"]["user_token"],
            organization_id=parsed_config["favro"]["organization_id"],
            widget_id=parsed_config["favro"]["widget_id"],
        )
        self.trello = TrelloConfig(
            api_key=parsed_config["trello"]["api_key"],
            api_token=parsed_config["trello"]["api_token"],
            board_id=parsed_config["trello"]["board_id"],
        )
