import React from 'react';

function StartScreen({ onStart }) {
  return (
    <div className="flex flex-col items-center justify-center text-center p-8 bg-gray-800 rounded-xl shadow-2xl max-w-md w-full border border-gray-700">
      <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600 mb-4">
        Quizz Arena
      </h1>
      <p className="text-gray-300 mb-8">
        Pon a prueba tus conocimientos con este desafío de preguntas.
      </p>
      <button
        onClick={onStart}
        className="w-full py-3 px-6 bg-purple-600 hover:bg-purple-700 text-white font-semibold rounded-lg shadow-lg transition duration-200 transform hover:scale-105"
      >
        Comenzar Cuestionario
      </button>
    </div>
  );
}

export default StartScreen;