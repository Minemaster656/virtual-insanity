from typing import Callable, Dict, List, Optional

from core.classes import GameMessage
from config import MODEL, client
import config
from ollama import ChatResponse
from rich import print
from core.location import Location


class CharacterBase:
    def __init__(self, name: str, description: str, prompt: str):
        self.name = name
        self.description = description
        self.prompt = prompt
        self.inventory = []
        self.location: Optional[Location] = None

    def act(self, new_messages: List[GameMessage]) -> str:
        raise NotImplementedError


class Character(CharacterBase):
    def __init__(
        self, name: str, description: str, prompt: str, tools: Dict[str, Callable]
    ):
        super().__init__(name, description, prompt)
        self.messages: List[Dict[str, str]] = [{"role": "system", "content": prompt}]
        self.tools = tools

    def act(self, new_messages: List[GameMessage]) -> str:
        def compress_messages(messages: List[Dict[str, str]]):
            # print(messages)
            if len(messages) < 12:
                return messages
            else:
                return [messages[0], *messages[-10:]]

        new_message = "# NEW MESSAGES SINCE LAST TURN:\n"
        for message in new_messages:
            new_message += f"\n# GAME MESSAGE BY {message.author}:\n{message.content}"
        self.messages.append({"role": "user", "content": new_message})
        self.messages.append(
            {
                "role": "user",
                "content": "# Environment:\nCharacters on location: Player, Tom, Hank\n\n"
                "# Info: HP: 100/100, Mana: 100/100, Inventory: []",
            }
        )
        i = 0
        while True:
            i += 1
            if i == 10:
                self.messages.append(
                    {
                        "role": "user",
                        "content": "# SYSTEM:\nToo many messages. Will you even use ``send``?",
                    }
                )
            if i >= config.CHARACTER_MAX_ITERATIONS:
                return ""

            # print("Model is thinking...")
            resp: ChatResponse = client.chat(
                MODEL,
                messages=compress_messages(self.messages),
                tools=list(self.tools.values()),
            )
            # print(resp.model_dump())
            print(
                "[bright_black]" + str(resp.message.thinking),
                "[bright_black]" + str(resp.message.content),
                sep="\n" * 3,
            )
            self.messages.append(resp.message.model_dump())
            if resp.message.tool_calls:
                is_return = False
                for tool_call in resp.message.tool_calls:
                    # print(
                    #     tool_call.function.name,
                    #     " ",
                    #     tool_call.function.arguments,
                    #     ": ",
                    #     end="",
                    # )
                    if tool_call.function.name in self.tools.keys():
                        # print("[green] exists")
                        try:
                            result = self.tools[tool_call.function.name](
                                **tool_call.function.arguments
                            )
                            if tool_call.function.name == "send":
                                is_return = result
                        except Exception as e:
                            print("[red]", e)
                            result = str(e)
                        self.messages.append(
                            {
                                "role": "tool",
                                "tool_name": tool_call.function.name,
                                "content": str(result),
                            }
                        )
                    else:
                        print("[red] does not exists")
                        self.messages.append(
                            {
                                "role": "tool",
                                "tool_name": tool_call.function.name,
                                "content": "Unknown function",
                            }
                        )
                if is_return:
                    return is_return
            else:
                print("[red] No tool call")
                extras: List[str] = []
                if "<send>" in self.messages[-1]["content"]:
                    extras.append(
                        "You are trying to use xml text instead of the send tool"
                    )
                self.messages.append(
                    {
                        "role": "user",
                        "content": f"# SYSTEM:\nYou forgot about the tool call. If you want to send your answer - use the send tool\n{'\n -'.join(extras)}",
                    }
                )


class Player(CharacterBase):
    def __init__(self, name: str, description: str, prompt: str):
        super().__init__(name, description, prompt)
