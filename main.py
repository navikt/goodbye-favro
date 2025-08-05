import tomllib

from src.config import Config
from src.goodbye_favro import Favro
from src.hello_trello import Trello
from src.unholy_union import UnholyUnion


def parse_config():
    with open("config.toml", "rb") as f:
        return Config(tomllib.load(f))


if __name__ == "__main__":
    config = parse_config()
    favro: Favro = Favro(config=config.favro)
    trello: Trello = Trello(
        config=config.trello,
    )

    print(trello.labels)
    unholy_union = UnholyUnion(trello, favro)
    # print(unholy_union.columns)
