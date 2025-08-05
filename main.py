import tomllib

from src.config import Config
from src import goodbye_favro, hello_trello, unholy_union


def parse_config():
    with open("config.toml", "rb") as f:
        return Config(tomllib.load(f))


if __name__ == "__main__":
    config = parse_config()
    favro = goodbye_favro.Favro(config=config.favro)
    trello = hello_trello.Trello(
        config=config.trello,
    )

    print(trello.labels)
    unholy_union = unholy_union.UnholyUnion(trello, favro)
    # print(unholy_union.columns)
