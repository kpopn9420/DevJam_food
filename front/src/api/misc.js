import api from './api'

const Misc = {
  // Join AI chat
  joinChat: () => api.get('/chat/join'),
  // Check API gateway health
  checkHealth: () => api.get('/health'),
  // Get file
  getFile: (fileId) => api.get(`/file/${fileId}`),
}

export default Misc
