import React, { useState } from 'react';
import AnswerPopup from './AnswerPopup';

function QuestionAnswer({ question, questionNumber: questionIndex, totalQuestions, onNavigate, onAnswer }) {
  const [answerRevealed, setAnswerRevealed] = useState(false);
  const [isPopupVisible, setIsPopupVisible] = useState(false); // Add state for popup visibility

  const revealAnswer = () => {
    setIsPopupVisible(true); // Show the popup
    setAnswerRevealed(true);
  };

  const handleResponse = (correct) => {
    onAnswer(questionIndex, correct);
  };

  return (
    <div className="questionAnswer">
      <div className="progressIndicator">
        {questionIndex + 1}/{totalQuestions}
      </div>

      <button className="navButton navButtonLeft" onClick={() => { onNavigate(1); setAnswerRevealed(false); }}>
        <span className="arrow">&gt;</span>
      </button>

      <h2>{question.question}</h2>

      {!answerRevealed ? (
        <button className="startRevealButton" onClick={revealAnswer}>תשובה</button>
      ) : (
        <AnswerPopup answer={question.answer} onCorrect={handleResponse} isVisible={isPopupVisible} />
      )}

      <button className="navButton navButtonRight" onClick={() => { onNavigate(-1); setAnswerRevealed(false); }}>
        <span className="arrow">&lt;</span>
      </button>
    </div>
  );
}

export default QuestionAnswer;
