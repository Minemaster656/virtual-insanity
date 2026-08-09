from typing import List
from core.character import CharacterBase, Player
from core.classes import GameMessage, get_suffix_after_last_author
from rich.markdown import Markdown
from rich import print


class Location:
    def __init__(
        self,
        name: str,
        description: str,
        prompt: str,
        characters: List[CharacterBase] = [],
    ):
        self.name = name
        self.description = description
        self.prompt = prompt
        self.characters: List[CharacterBase] = characters
        self.history: List[GameMessage] = []

    def do_turns(self):
        for character in self.characters:
            if isinstance(character, Player):
                inp = input(f"You as {character.name}: ")
                self.history.append(GameMessage(character.name, inp))
            else:
                resp = character.act(
                    get_suffix_after_last_author(self.history, character.name)
                )
                if resp != "":
                    print(f"[magenta]{character.name}:\n", Markdown(resp))
                    self.history.append(GameMessage(character.name, resp))
                else:
                    print(
                        f"[magenta]{character.name}:\n",
                        "[bright_black][italic]Skipped his turn...",
                    )
                    self.history.append(
                        GameMessage(character.name, "Skipped his turn...")
                    )
