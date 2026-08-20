from typing import List
from core.classes import GameMessage
from core.location import Location
from ollama import Client
from rich import print
from core.world import World
import networkx as nx
import asyncio

from core.character import Character, CharacterBase, Player

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
    You are in the group roleplay chat with others. Everybody makes turns by queue.
    Do not maintain others' roles!
    Do not use emoji
    Do not respond questions or actions if they are not adressed to you, BUT you can REACT on them
    Empty text to skip your turn.
    Use *text* to mark actions, you can express yourself, move, interact etc.
    ---

    """
    queue: List[CharacterBase] = [
        Player("Player", "Player", "Player"),
        Character(
            "Tom",
            "Generic character",
            GENERIC_PROMPT + "Your are Tom.",
            {},
        ),
        Character(
            "Hank",
            "Generic character",
            GENERIC_PROMPT + "Your are Hank.",
            {},
        ),
    ]
    location1 = Location("Test room", "Test room", "Test room", queue)
    location2 = Location("Empty room", "Empty room", "Empty room", [])
    locations = nx.Graph()
    locations.add_nodes_from([location1, location2])
    locations.add_edges_from([(location1, location2)])
    world = World(locations)

    while True:
        world.tick()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")
