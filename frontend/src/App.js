import React, { useState } from 'react';
import './App.css';
import QuestionAnswer from './QuestionAnswer'; // Import the component
import FinalScreen from './FinalScreen'; // Import the FinalScreen component


const mockQuestions = [
  {
    question: "מי הוא הדר אשוח?",
    answer: "בדיקה בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה  בדיקה ",
    url: "https://en.wikipedia.org/wiki/Paris"
  },
  {
    question: "מי הוא מיז אשוח?",
    answer: "The Eiffel Tower (/ˈaɪfəl/ EYE-fəl; French: tour Eiffel [tuʁ‿ɛfɛl] (About this soundlisten)) is a wrought-iron lattice tower on the Champ de Mars in Paris, France. It is named after the engineer Gustave Eiffel, whose company designed and built the tower.",
    url: "https://en.wikipedia.org/wiki/Paris"
  },
  // Add more questions as needed
];

// async function fetchQuestion() {
//   const response = await fetch('/api/questions?count=1'); // Fetches one question
//   const questions = await response.json();
//   return questions[0]; // Assuming the API returns an array of questions
// }
async function fetchQuestions() {
  let q = mockQuestions;
  // add userAnswer to each question with null
  q.forEach(question => question.userAnswer = null);
  return q;
}


function App() {
  const [quizStarted, setQuizStarted] = useState(false);
  const [questions, setQuestions] = useState([]); // [question1, question2, ...
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [isFinished, setIsFinished] = useState(false);
  // Question index to answer: True, False, Null



  const startQuiz = async () => {
    const questions = await fetchQuestions();
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
