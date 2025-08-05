from src.datatypes import FavroTag, TrelloLabel
import random


class Tag:
    def __init__(self, favro_tag: FavroTag, trello_label: TrelloLabel):
        self.favro = favro_tag
        self.trello = trello_label


ALLOWED_COLORS = [
    "green",
    "yellow",
    "orange",
    "red",
    "purple",
    "blue",
    "sky",
    "lime",
    "pink",
    "black",
    "green_dark",
    "yellow_dark",
    "orange_dark",
    "red_dark",
    "purple_dark",
    "blue_dark",
    "sky_dark",
    "lime_dark",
    "pink_dark",
    "black_dark",
    "green_light",
    "yellow_light",
    "orange_light",
    "red_light",
    "purple_light",
    "blue_light",
    "sky_light",
    "lime_light",
    "pink_light",
    "black_light",
]

def get_tag_from_favro_id(tags, favro_id):
    return next((tag for tag in tags if tag.favro.id == favro_id), None)

def choose_color(favro_tag: FavroTag) -> str:
    """
    Choose a color for the Trello label based on the Favro tag.
    If the Favro tag has a color, use it; otherwise, default to 'blue'.
    """
    if favro_tag.color and favro_tag.color in ALLOWED_COLORS:
        return favro_tag.color

    random.seed(favro_tag.name)
    return random.choice(ALLOWED_COLORS)
