from typing import List, Union
from classes import GameMessage, get_suffix_after_last_author
from ollama import Client
from rich import print
import asyncio

from character import Character, Player
from rich.markdown import Markdown

client = Client()
MODEL = "gemma4:e4b-it-qat"


def echo(value: str) -> str:
    """Debug function that echoes back the input. Also prints it. Feel free to put anything"""
    print("Echo: ", value)
    return value


def send(value: str) -> str:
    """Sends a message to the chat and breaks the thinking loop until the your next message"""
    return value


async def main():
    history: List[GameMessage] = []
    queue: List[Union[Character, Player]] = [
        Player("Player", "Player", "Player"),
        Character(
            "Character 1",
            "Character",
            "You are a roleplay character. Do not respond as other characters. Respond in russian. Use send to send message to the chat",
            {"send": send},
        ),
        Character(
            "Character 2",
            "Character",
            "You are a roleplay character. Do not respond as other characters. Respond in russian. Use send to send message to the chat",
            {"send": send},
        ),
    ]

    while True:
        for character in queue:
            if isinstance(character, Player):
                inp = input(f"You as {character.name}: ")
                history.append(GameMessage(character.name, inp))
            else:
                resp = character.act(
                    get_suffix_after_last_author(history, character.name)
                )
                print(f"[magenta]{character.name}:\n", Markdown(resp))
                history.append(GameMessage(character.name, resp))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")
