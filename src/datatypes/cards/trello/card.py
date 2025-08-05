class TrelloCard:
    def __init__(self, data):
        self.id = data.get("id")
        self.name = data.get("name")
        self.desc = data.get("desc")
        self.closed = data.get("closed", False)
        self.idList = data.get("idList")
        self.pos = data.get("pos", 0)
        self.labels = data.get("labels", [])
        self.due = data.get("due")
        self.url = data.get("url")

    def __repr__(self):
        return f"TrelloCard(id={self.id}, name={self.name}, list_id={self.idList})"
