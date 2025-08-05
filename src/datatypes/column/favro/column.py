class FavroColumn:
    def __init__(self, json_data):
        self.id = json_data["columnId"]
        self.name = json_data["name"]
        self.organization_id = json_data["organizationId"]
        self.widget_id = json_data["widgetCommonId"]
        self.position = json_data["position"]
        self.card_count = json_data["cardCount"]
        self.time_sum = json_data["timeSum"]
        self.estimation_sum = json_data["estimationSum"]

    def __repr__(self):
        return f"Column(id='{self.id}', name='{self.name}', position={self.position}, card_count={self.card_count})"
