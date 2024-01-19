import asyncio
from dataclasses import dataclass

from flask import Flask, request
from yarl import URL

from infinite_questions.trivia_ai import generate_trivia_question
from infinite_questions.wikipedia_api import get_articles, TriviaType

app = Flask(__name__)


@dataclass
class Trivia:
    question: str
    answer: str
    source_url: str


@app.route('/')
def hello():
    return 'Hello, World!'


async def generate_one_trivia(page_url: URL, summary: str) -> Trivia:
    question, answer = await generate_trivia_question(summary)
    return Trivia(question, answer, str(page_url))


@app.route('/api/trivia')
async def get_trivia_api() -> list[Trivia]:
    max_articles = int(request.args.get('max_articles', 1))
    trivia_type = TriviaType[request.args.get('trivia_type', TriviaType.RANDOM)]

    articles = await get_articles(trivia_type, max_articles)

    results = list(await asyncio.gather(*[generate_one_trivia(*r) for r in articles]))

    return results


def main():
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()


if __name__ == '__main__':
    main()
