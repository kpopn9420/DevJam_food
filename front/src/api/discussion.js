import api from './api'

const Discussion = {
  // Get discussions list
  getDiscussion: (courseId) => api.get('/discussion/', { params: { courseId } }),
  // Join a discussion or get discussion content
  joinDiscussion: (groupId, topicId) =>
    api.get('/discussion/join', { params: { groupId, topicId } }),
  // Start a discussion
  startDiscussion: (body) => api.post('/discussion/start', body),
  // End a discussion
  endDiscussion: (body) => api.post('/discussion/end', body),
}

export default Discussion
