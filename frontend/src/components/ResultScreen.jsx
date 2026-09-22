import React from 'react';

function ResultScreen({ score, totalPossible, onRestart }) {
  const porcentaje = Math.round((score / totalPossible) * 100);

  return (
    <div className="bg-gray-800 border border-gray-700 rounded-xl shadow-2xl p-8 max-w-md w-full text-center">
      <h1 className="text-3xl font-extrabold text-white mb-2">¡Cuestionario Completado!</h1>
      <p className="text-gray-400 mb-6">Has completado el desafío con éxito.</p>

      <div className="bg-gray-900/80 border border-gray-700 rounded-xl p-6 mb-8">
        <span className="text-sm text-gray-400 uppercase tracking-wider block mb-1">Puntuación Final</span>
        <span className="text-5xl font-black text-purple-400">{score}</span>
        <span className="text-gray-500 text-sm block mt-1">de {totalPossible} puntos posibles ({porcentaje}%)</span>
      </div>

      <button
        onClick={onRestart}
        className="w-full py-3 px-6 bg-purple-600 hover:bg-purple-700 text-white font-semibold rounded-lg shadow-lg transition duration-200"
      >
        Volver a Jugar
      </button>
    </div>
  );
}

export default ResultScreen;