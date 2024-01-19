// import React from 'react';
import './FinalScreen.css';

function FinalScreen({ correctAnswers, totalQuestions }) {
    return (
        <div className="finalScreen">
            <p className="resultText">ענית נכון על</p>
            <div className="circle">
                <div className="scores">
                    <span className="number">{correctAnswers}</span>
                    <span className="total">מתוך {totalQuestions}</span>
                </div>
            </div>
            <p className="geniusText">גאונות לשמה!</p>
        </div>
    );
}


export default FinalScreen;
