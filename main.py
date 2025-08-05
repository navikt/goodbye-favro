import tomllib
import argparse

from src.config import Config
from src.goodbye_favro import Favro
from src.hello_trello import Trello
from src.unholy_union import UnholyUnion


def parse_config():
    with open("config.toml", "rb") as f:
        return Config(tomllib.load(f))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("goodbye-favro")
    parser.add_argument("--delete-stuff", action="store_true")

    args = parser.parse_args()
    config = parse_config()

    trello: Trello = Trello(
        config=config.trello,
    )
    if args.delete_stuff:
        trello.delete_all_tags()
        exit()
    favro: Favro = Favro(config=config.favro)
    unholy_union = UnholyUnion(trello, favro)
    # print(unholy_union.columns)
