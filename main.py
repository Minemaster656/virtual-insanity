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
    """Sends a message to the chat and ends your turn.
    Args:
        value (str): The message to send. Use "pass" or empty to skip your turn.

    Returns:
        str: Echoes the input and sends it to the chat.
    """
    if value == "pass":
        return ""
    return value


async def main():
    history: List[GameMessage] = []
    GENERIC_PROMPT = """
    You are a roleplay character, not an AI assistant.
    Make sure that you respond as YOU, not as the other character.
    Respond in russian. 
    Use the ``send`` tool to send message to the chat and finish your turn or use ``pass`` as message to skip your turn.
    You are in the group roleplay chat with others. Everybody makes turns by queue.
    ---

    """
    queue: List[Union[Character, Player]] = [
        Player("Player", "Player", "Player"),
        Character(
            "Tom",
            "Character",
            GENERIC_PROMPT + "Your are Tom.",
            {"send": send},
        ),
        Character(
            "Hank",
            "Character",
            GENERIC_PROMPT + "Your are Hank.",
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
                if resp != "":
                    print(f"[magenta]{character.name}:\n", Markdown(resp))
                    history.append(GameMessage(character.name, resp))
                else:
                    print(
                        f"[magenta]{character.name}:\n",
                        "[bright_black][italic]Skipped his turn...",
                    )
                    history.append(GameMessage(character.name, "Skipped his turn..."))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")
