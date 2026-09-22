import React, { useState } from 'react';
import { getPreguntas } from './services/api';
import StartScreen from './components/StartScreen';
import QuizCard from './components/QuizzCard';
import ResultScreen from './components/ResultScreen';

function App() {
  const [step, setStep] = useState('start');
  const [preguntas, setPreguntas] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [score, setScore] = useState(0);

  const iniciarJuego = async () => {
    const data = await getPreguntas();
    if (data.length > 0) {
      setPreguntas(data);
      setCurrentIndex(0);
      setScore(0);
      setStep('quiz');
    } else {
      alert("No se pudieron cargar las preguntas desde el servidor.");
    }
  };

  const handleAnswer = (esCorrecta, puntuacionOpcion) => {
    if (esCorrecta) {
      setScore(prev => prev + (puntuacionOpcion || 10));
    }

    const siguiente = currentIndex + 1;
    if (siguiente < preguntas.length) {
      setCurrentIndex(siguiente);
    } else {
      setStep('result');
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center p-4">
      {step === 'start' && <StartScreen onStart={iniciarJuego} />}
      {step === 'quiz' && preguntas.length > 0 && (
        <QuizCard 
          pregunta={preguntas[currentIndex]} 
          current={currentIndex + 1} 
          total={preguntas.length} 
          onAnswer={handleAnswer} 
        />
      )}
      {step === 'result' && (
        <ResultScreen score={score} totalPossible={preguntas.length * 10} onRestart={() => setStep('start')} />
      )}
    </div>
  );
}

export default App;