class ListDataSource:
    def __init__(self, json_data):
        self.filter = json_data.get("filter", None)


class TrelloList:
    def __init__(self, json_data):
        self.id = json_data["id"]
        self.name = json_data["name"]
        self.closed = json_data["closed"]
        self.color = json_data["color"]
        self.id_board = json_data["idBoard"]
        self.pos = json_data["pos"]
        self.subscribed = json_data.get("subscribed", None)
        self.soft_limit = json_data.get("softLimit", None)
        self.type = json_data.get("type", None)
        self.datasource = ListDataSource(json_data.get("datasource", {}))

    def __repr__(self):
        return f"TrelloList(id='{self.id}', name='{self.name}', closed={self.closed}, color='{self.color}')"
