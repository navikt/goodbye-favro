class FavroTag:
    def __init__(self, tag_data):
        self.id = tag_data["tagId"]
        self.name = tag_data["name"]
        self.color = tag_data.get("color", None)
        self.organization_id = tag_data["organizationId"]


    def __repr__(self):
        return f"FavroTag(id={self.id}, name={self.name}, color={self.color})"