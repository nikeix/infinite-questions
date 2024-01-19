from flask import Flask

from infinite_questions.trivia_ai import generate_trivia_question
from infinite_questions.wikipedia_api import get_random_article_summary

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/api/question')
async def get_question_api():
    page_url, summary = await get_random_article_summary()
    question, answer = await generate_trivia_question(summary)

    return dict(source_url=str(page_url), question=question, answer=answer)


def main():
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()


if __name__ == '__main__':
    main()
