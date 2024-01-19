import os
from typing import Tuple

from openai import AsyncOpenAI

from infinite_questions.config import GPT_TRIVIA_PROMPT


async def generate_trivia_question(trivia_info: str) -> Tuple[str, str]:
    client = AsyncOpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": GPT_TRIVIA_PROMPT + '\n\n' + trivia_info,
            }
        ],
        model="gpt-3.5-turbo",
    )

    response = chat_completion.choices[0].message.content
    question, answer = response.split('\n', 1)
    return question, answer
