class FavroCard:
    def __init__(
        self,
        data,
    ):
        self.name = data.get("name")
        self.id = data.get("cardId")
        self.common_id = data.get("cardCommonId")
        self.organization_id = data.get("organizationId")
        self.position = data.get("position")
        self.list_position = data.get("listPosition")
        self.description = data.get("detailedDescription", "")
        self.parent_card_id = data.get("parentCardId", None)
        self.archived = data.get("archived")
        self.widget_common_id = data.get("widgetCommonId")
        self.column_id = data.get("columnId", None)
        self.lane_id = data.get("laneId", None)
        self.is_lane = data.get("isLane")
        self.sheet_position = data.get("sheetPosition", None)
        self.dependencies = data.get("dependencies")
        self.tags = data.get("tags")
        self.sequential_id = data.get("sequentialId")
        self.created_by_user_id = data.get("createdByUserId")
        self.created_at = data.get("createdAt")
        self.assignments = data.get("assignments")
        self.tasks_total = data.get("tasksTotal")
        self.tasks_done = data.get("tasksDone")
        self.attachments = data.get("attachments")
        self.custom_fields = data.get("customFields")
        self.time_on_board = data.get("timeOnBoard")
        self.time_on_columns = data.get("timeOnColumns")
        self.favro_attachments = data.get("favroAttachments")
        self.num_comments = data.get("numComments", 0)
        self.due_date = data.get("dueDate")

    def __repr__(self):
        return f"FavroCard(id='{self.id}', name='{self.name}', position={self.position}, archived={self.archived}, list_position={self.list_position}, sheet_position={self.sheet_position}, lane_id='{self.lane_id}', column_id='{self.column_id}')"