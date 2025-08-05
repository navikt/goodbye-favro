class TrelloChecklist:
    # {
    # 'id': '68920766fe48583f80833b24',
    # 'name': 'To do',
    # 'idBoard': '689195899923d28e7e321b91',
    # 'idCard': '68920765f9c83cc4d60c2668',
    # 'pos': 140737488355328,
    # 'checkItems': [],
    # 'limits': {}
    # }
    def __init__(self, session, api_key, api_token, json_data):
        self.session = session
        self.api_key = api_key
        self.api_token = api_token
        self.id = json_data["id"]
        self.name = json_data["name"]
        self.id_board = json_data["idBoard"]
        self.pos = json_data["pos"]
        self.check_items = json_data["checkItems"]
        self.limits = json_data["limits"]

    def __repr__(self):
        return f"TrelloChecklist(id={self.id}, name={self.name})"

    def create_item(self, checked, name):
        response = self.session.post(
            f"https://api.trello.com/1/checklists/{self.id}/checkItems",
            params={
                "name": name,
                "checked": str(checked).lower(),
                "key": self.api_key,
                "token": self.api_token,
            },
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(
                f"Error fetching checklists/{self.id}/checkItems: {response.status_code} - {response.text}"
            )
            return None
