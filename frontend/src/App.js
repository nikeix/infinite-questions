import React, { useState } from 'react';
import './App.css';
import QuestionAnswer from './QuestionAnswer'; // Import the component
import FinalScreen from './FinalScreen'; // Import the FinalScreen component


async function fetchQuestions() {
  const response = await fetch('/api/trivia?max_articles=3&trivia_type=RANDOM');
  const trivia = await response.json();
  return trivia;
  // return [{"question":"שאלה: מי הוא איש העסקים שבשליטתו של חברת דלק נדל\"ן?","answer":"תשובה: יצחק תשובה.","source_url":"https://he.wikipedia.org/wiki/%D7%93%D7%9C%D7%A7_%D7%A0%D7%93%D7%9C%22%D7%9F"},{"question":"שאלה: איזה תפקיד כיהן אודי שני בצה\"ל?","answer":"תשובה: ראש אגף התקשוב, מפקד הגיס הצפוני, ומנכ\"ל משרד הביטחון.","source_url":"https://he.wikipedia.org/wiki/%D7%90%D7%95%D7%93%D7%99_%D7%A9%D7%A0%D7%99"},{"question":"שאלה: מתי הוקמה שכונת זיכרון יוסף?","answer":"תשובה: בשנת 1927.","source_url":"https://he.wikipedia.org/wiki/%D7%96%D7%99%D7%9B%D7%A8%D7%95%D7%9F_%D7%99%D7%95%D7%A1%D7%A3"}];
}


function App() {
  const [quizStarted, setQuizStarted] = useState(false);
  const [questions, setQuestions] = useState([]); // [question1, question2, ...
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [isFinished, setIsFinished] = useState(false);
  // Question index to answer: True, False, Null



  const startQuiz = async () => {
    const questions = await fetchQuestions();
    // add userAnswer property to each question
    questions.forEach(question => question.userAnswer = null);
    setQuestions(questions);
    setQuizStarted(true);
  };

  const onNavigate = (direction) => {
    // protect against out of bounds and negative values
    if (currentQuestionIndex + direction < 0) {
      return;
    }
    if (currentQuestionIndex + direction >= questions.length) {
      return;
    }
    setCurrentQuestionIndex(currentQuestionIndex + direction);
  };

  const allQuestionsAnswered = () => {
    return questions.every(question => question.userAnswer !== null);
  }

  const handleAnswer = (index, answer) => {
    console.log('Answered question', index, 'with', answer);
    questions[index].userAnswer = answer;
    if (allQuestionsAnswered()) {
      setIsFinished(true);
    }
  };


  let content;
  if (quizStarted) {
    console.log("Rendering question");
    if (isFinished) {
      content = (
        <FinalScreen
          correctAnswers={questions.filter(question => question.userAnswer === true).length}
          totalQuestions={questions.length}
        />
      );
    }
    else {
      content = (
        <QuestionAnswer
          question={questions[currentQuestionIndex]}
          questionNumber={currentQuestionIndex}
          totalQuestions={questions.length}
          onNavigate={onNavigate}
          onAnswer={handleAnswer}
        />
      );
    }
  } else {
    content = (
      <>
        <h1 className="startTitle">20 שאלות</h1>
        <button className="startButton" onClick={startQuiz}>התחילו!</button>
      </>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        {content}
      </header>
    </div>
  );
}

export default App;
