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
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--ignore-lanes")

    args = parser.parse_args()
    config = parse_config()

    lanes_to_ignore = []
    if args.ignore_lanes:
        lanes_to_ignore = [x.strip() for x in args.ignore_lanes.split(",")]
        print(f"Ignoring lanes: {lanes_to_ignore}")

    trello: Trello = Trello(
        config=config.trello,
        verbose=args.verbose,
    )
    if args.delete_stuff:
        trello.delete_all_tags()
        exit()
    favro: Favro = Favro(config=config.favro, verbose=args.verbose)
    unholy_union = UnholyUnion(trello, favro, verbose=args.verbose, lanes_to_ignore=lanes_to_ignore)
    # print(unholy_union.columns)
