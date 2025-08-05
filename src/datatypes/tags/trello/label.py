class TrelloLabel:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.color = data.get("color")
        self.id_board = data["idBoard"]
        self.uses = data.get("uses", 0)

    def __repr__(self):
        return f"TrelloLabel(id='{self.id}', name='{self.name}', color='{self.color}', uses={self.uses})"