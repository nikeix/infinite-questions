import asyncio
import os
from dataclasses import dataclass

from fastapi import FastAPI, Security, HTTPException
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_401_UNAUTHORIZED
from yarl import URL

from trivia_ai import generate_trivia_question
from wikipedia_api import get_articles, TriviaType

app = FastAPI()
API_KEY_HEADER = APIKeyHeader(name="X-API-Key")

ARTICLES_LIMIT = 20


@dataclass
class Trivia:
    question: str
    answer: str
    source_url: str


def get_api_key(api_key_header: str = Security(API_KEY_HEADER)) -> str:
    if api_key_header == os.environ.get("SERVER_SECRET"):
        return api_key_header
    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )


async def generate_one_trivia(page_url: URL, summary: str) -> Trivia:
    question, answer = await generate_trivia_question(summary)
    return Trivia(question, answer, str(page_url))


@app.get('/trivia')
async def get_trivia_api(
        max_articles: int = 1,
        trivia_type: TriviaType = TriviaType.RANDOM,
        api_key: str = Security(get_api_key),
) -> list[Trivia]:
    if max_articles > ARTICLES_LIMIT:
        return {'error': f'Maximum {ARTICLES_LIMIT} articles allowed'}

    articles = await get_articles(trivia_type, max_articles)

    results = list(await asyncio.gather(*[generate_one_trivia(*r) for r in articles]))

    return results


def main():
    import uvicorn
    uvicorn.run("app:app", host='0.0.0.0', port=8000, reload=True)


if __name__ == '__main__':
    main()
