import api from './api'

const Resource = {
  // Get info for announcement
  getSchoolAnnouncement: (schoolID) => api.get(`/resource/school/${schoolID}/announcement/`),
  // Get info for homepage
  getUser: (userID) => api.get(`/resource/user/${userID}`),
  // Get info for setting
  getUserSetting: (userID) => api.get(`/resource/user/${userID}/setting`),
  // Change language or theme for user
  postUserLangTheme: (userID, body) => api.post(`/resource/user/${userID}/setting/edit-language-theme`, body),
  // Change image
  postUserImage: (userID, body) => api.post(`/resource/user/${userID}/setting/edit-image`, body),
  // Upload the user CSV file
  postUploadUser: (body) => api.post(`/resource/setting/upload-user`, body),
  // Add user
  postNewUser: (body) => api.post(`/resource/setting/add-user`, body),
  // Fetch teacher list
  getTeacherList: (schoolID) => api.get(`/resource/school/${schoolID}/teacherlist`),
  // Fetch class list
  getClassList: (schoolID) => api.get(`/resource/school/${schoolID}/classlist`),
  // Fetch school list
  getSchoolList: () => api.get(`/resource/schoollist`),
  // Get school ID
  getSchoolId: (userID) => api.get(`/resource/user/${userID}/getschoolid`),
}

export default Resource
