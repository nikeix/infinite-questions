import React, { useState } from 'react';

function AnswerPopup({ answer, onCorrect }) {
  const [backgroundColor, setBackgroundColor] = useState('rgb(30, 184, 255)'); // Default background color

  const handleCorrect = (correct) => {
    // Change the background color based on correctness
    if (correct) {
      setBackgroundColor('green'); // Change to green for correct
    } else {
      setBackgroundColor('red'); // Change to red for incorrect
    }

    onCorrect(correct);
  };

  return (
    <div className="answerPopup" style={{ backgroundColor }}>
      <div className="answer">{answer}</div>
      <div className="divider"></div>
      <div className="correctButtonsText">האם צדקת?</div>
      <div className="correctButtons">
        <button className="correctButton" onClick={() => handleCorrect(false)}>X</button>
        <button className="correctButton" onClick={() => handleCorrect(true)}>V</button>
      </div>
    </div>
  );
}

export default AnswerPopup;
