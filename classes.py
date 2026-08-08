from dataclasses import dataclass
from typing import List


@dataclass
class GameMessage:
    def __init__(self, author: str, content: str):
        self.author = author
        self.content = content


def get_suffix_after_last_author(
    messages: List[GameMessage], target_author: str
) -> List[GameMessage]:
    last_index = -1
    for i in range(len(messages) - 1, -1, -1):
        if messages[i].author == target_author:
            last_index = i
            break

    if last_index == -1:
        return messages[:]
    return messages[last_index + 1 :]
