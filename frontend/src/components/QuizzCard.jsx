import React from 'react';

function QuizzCard({ pregunta, current, total, onAnswer }) {
  return (
    <div className="bg-gray-800 border border-gray-700 rounded-xl shadow-2xl p-8 max-w-xl w-full">
      <div className="flex justify-between items-center mb-6 text-sm text-gray-400 font-medium">
        <span>Pregunta {current} de {total}</span>
        <span className="bg-purple-900/50 text-purple-300 px-3 py-1 rounded-full border border-purple-700/50">
          {pregunta.puntuacion || 10} pts
        </span>
      </div>

      <h2 className="text-xl font-bold text-white mb-6 leading-snug">
        {pregunta.texto}
      </h2>

      <div className="space-y-3">
        {pregunta.opciones.map((opcion, index) => (
          <button
            key={index}
            onClick={() => onAnswer(opcion.es_correcta, pregunta.puntuacion || 10)}
            className="w-full text-left p-4 rounded-lg bg-gray-700/50 hover:bg-purple-600/30 border border-gray-600 hover:border-purple-500 text-gray-200 transition duration-150 flex items-center justify-between group"
          >
            <span className="font-medium">{opcion.texto}</span>
          </button>
        ))}
      </div>
    </div>
  );
}

export default QuizzCard;