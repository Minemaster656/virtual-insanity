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
    Use the ``send`` tool to send message to the chat and finish your turn or use ``pass`` as message to skip your turn.
    You are in the group roleplay chat with others. Everybody makes turns by queue.
    ---

    """
    queue: List[CharacterBase] = [
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
