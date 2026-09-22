import axios from 'axios';

const API = axios.create({
  baseURL: '/api/quizz/preguntas/',
});

export const getPreguntas = async () => {
  try {
    const response = await API.get('');
    return response.data;
  } catch (error) {
    console.error('Error al obtener las preguntas del servidor:', error);
    return [];
  }
};