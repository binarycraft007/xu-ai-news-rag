import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000'; // The backend URL

const apiClient = axios.create({
  baseURL: API_URL,
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const register = (username, password) => {
  return apiClient.post('/auth/register', { username, password });
};

export const login = async (username, password) => {
  const response = await apiClient.post('/auth/login', { username, password });
  if (response.data.access_token) {
    localStorage.setItem('token', response.data.access_token);
  }
  return response;
};

export const logout = () => {
  localStorage.removeItem('token');
};

export const getDocuments = (params) => {
  return apiClient.get('/documents', { params });
};

export const uploadDocument = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return apiClient.post('/documents', formData);
};

export const deleteDocument = (docId) => {
  return apiClient.delete(`/documents/${docId}`);
};

export const batchDeleteDocuments = (docIds) => {
  return apiClient.post('/documents/batch_delete', { doc_ids: docIds });
};

export const search = (query) => {
  return apiClient.post('/search', { query });
};

export const getKeywordReport = () => {
  return apiClient.get('/report/keywords');
};

export const getClusteringReport = () => {
  return apiClient.get('/report/clustering');
};

export const getFeeds = () => {
  return apiClient.get('/feeds');
};

export const addFeed = (url) => {
  return apiClient.post('/feeds', { url });
};

export const deleteFeed = (feedId) => {
  return apiClient.delete(`/feeds/${feedId}`);
};

export const editDocumentMetadata = (docId, { tags, source }) => {
  return apiClient.put(`/documents/${docId}`, { tags, source });
};