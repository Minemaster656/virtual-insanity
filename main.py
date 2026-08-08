from typing import Callable, Dict
from ollama import Client, ChatResponse
from rich import print
from rich.markdown import Markdown
import asyncio

client = Client()
MODEL = "gemma4:e4b-it-qat"


def echo(value: str) -> str:
    """Debug function that echoes back the input. Also prints it. Feel free to put anything"""
    print("Echo: ", value)
    return value


async def main():
    history = []
    available_functions: Dict[str, Callable] = {
        "echo": echo,
    }

    while True:
        inp = input("> ")
        print("Model is thinking...")
        history.append({"role": "user", "content": inp})

        resp: ChatResponse = client.chat(
            MODEL, messages=history, tools=list(available_functions.values())
        )
        print(resp.model_dump())
        print(
            "[bright_black]" + str(resp.message.thinking),
            Markdown(str(resp.message.content)),
            sep="\n" * 3,
        )
        prompt_eval_duration = (resp.prompt_eval_duration or 0) / 1e9
        eval_duration = (resp.eval_duration or 0) / 1e9

        print(
            f"Prompt: {resp.prompt_eval_count} tokens in {prompt_eval_duration} sec. ({int(resp.prompt_eval_count or 0) / prompt_eval_duration} TPS)\n"
            f"Response: {resp.eval_count} tokens in {eval_duration} sec. ({int(resp.eval_count or 0) / eval_duration} TPS)\n"
        )
        history.append(resp.message.model_dump())
        if resp.message.tool_calls:
            for tool_call in resp.message.tool_calls:
                print(
                    tool_call.function.name,
                    " ",
                    tool_call.function.arguments,
                    ": ",
                    end="",
                )
                if tool_call.function.name in available_functions.keys():
                    print("[green] exists")
                    try:
                        result = available_functions[tool_call.function.name](
                            **tool_call.function.arguments
                        )
                    except Exception as e:
                        print("[red]", e)
                        result = str(e)
                    history.append(
                        {
                            "role": "tool",
                            "tool_name": tool_call.function.name,
                            "content": str(result),
                        }
                    )
                else:
                    print("[red] does not exists")
                    history.append(
                        {
                            "role": "tool",
                            "tool_name": tool_call.function.name,
                            "content": "Unknown function",
                        }
                    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")
