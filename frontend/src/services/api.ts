import axios from 'axios';
import type { ResearchRequest, ResearchResponse } from '../types/research';
import { SAMPLE_RESEARCH_RESPONSE } from '../mock/sampleData';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export const executeResearch = async (request: ResearchRequest): Promise<ResearchResponse> => {
  try {
    const response = await axios.post<ResearchResponse>(`${API_BASE_URL}/research`, request, {
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 60000,
    });
    return response.data;
  } catch (error) {
    console.warn('Backend API request failed or unreachable, returning response (or fallback if question matches):', error);
    // If backend is unreachable and question is about langchain, return sample mock data for seamless demo
    if (request.question.toLowerCase().includes('langchain')) {
      return {
        ...SAMPLE_RESEARCH_RESPONSE,
        question: request.question,
      };
    }
    throw error;
  }
};
