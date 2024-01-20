import asyncio
from dataclasses import dataclass

from fastapi import FastAPI
from yarl import URL

from trivia_ai import generate_trivia_question
from wikipedia_api import get_articles, TriviaType

app = FastAPI()

ARTICLES_LIMIT = 10

@dataclass
class Trivia:
    question: str
    answer: str
    source_url: str


async def generate_one_trivia(page_url: URL, summary: str) -> Trivia:
    question, answer = await generate_trivia_question(summary)
    return Trivia(question, answer, str(page_url))


@app.get('/trivia')
async def get_trivia_api(
    max_articles: int = 1,
    trivia_type: TriviaType = TriviaType.RANDOM,
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
