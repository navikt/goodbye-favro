class FavroLane:
    def __init__(self, lane_data):
        self.id = lane_data["laneId"]
        self.name = lane_data["name"]

    def __repr__(self):
        return f"FavroLane(id={self.id}, name={self.name})"
