# goodbye-favro

Copy `example.config.toml` to `config.toml` and fill out the required changes!

## Running

- `uv sync`
  - To fetch dependencies, and set up venv, etc.
- `uv run python main.py`

## Features

Currently we can

- [x] Create lists in Trello from Favro columns
- [x] Create labels in Trello from Favro tags
- [x] Create cards in Trello from Favro cards
  - (using appropriate labels created in the previous step)
- [x] Create checklists in Trello from Favro card descriptions containing `r#- \[[x\s]\].\*#
  - (and attach the checklists to a corresponding card in Trello)
