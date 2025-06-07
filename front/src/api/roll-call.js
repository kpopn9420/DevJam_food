import api from './api'

const RollCall = {
  // Get student's attendance record for current week
  getAttendance: (date) => api.get(`/rollcall/student/${date}`),
  // Get latest attendance  for a course
  getCourseAttendance: (courseId, date, period) => api.get(`/rollcall/teacher/${courseId}/${date}/${period}`),
  // Start auto roll call session
  autoRollCallStart: () => api.post('/rollcall/auto/start'),
  // Generate new roll call code
  autoRollCallGenerate: () => api.post('/rollcall/auto/generate'),
  // End auto roll call session
  autoRollCallEnd: () => api.post('/rollcall/auto/end'),
  // Punch in code
  autoRollCallPunch: (code) => api.post(`/rollcall/auto/punch-in/${code}`),
  // Manual roll call
  manualRollCall: () => api.post('/rollcall/manual'),
}

export default RollCall
