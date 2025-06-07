import api from './api'

const Course = {
  // Get info for course
  getUserCourse: (userID) => api.get(`/course/user/${userID}`),
  // Get info (time) for specific course
  getCourse: (courseID) => api.get(`/course/${courseID}`),
  // Update course
  patchCourse: (courseID, body) => api.patch(`/course/${courseID}`, body),
  // Delete course
  deleteCourse: (courseID) => api.delete(`/course/${courseID}`),
  // Get info for announcement
  getCourseAnnouncement: (courseID) => api.get(`/course/${courseID}/announcement`),
  // Get info for topic
  getCourseTopic: (courseID) => api.get(`/course/${courseID}/topic`),
  // Add announcement
  postCourseAnnouncement: (courseID, body) => api.post(`/course/${courseID}/announcement/add`, body),
  // Update announcement
  patchCourseAnnouncement: (courseID, announcementID, body) =>
    api.patch(`/course/${courseID}/announcement/${announcementID}`, body),
  // Delete announcement
  deleteCourseAnnouncement: (courseID, announcementID) =>
    api.delete(`/course/${courseID}/announcement/${announcementID}`),
  // Return grouplist for adding topic
  getGroupList: (courseID) => api.get(`/course/${courseID}/grouplist`),
  // Add topic
  postCourseTopic: (courseID, body) => api.post(`/course/${courseID}/topic/add`, body),
  // Get data for response
  getTopicUpdateResponse: (courseID, topicID) =>
    api.get(`/course/${courseID}/topic/${topicID}/responseforupdatetopic`),
  // Update topic
  patchCourseTopic: (courseID, topicID, body) => api.patch(`/course/${courseID}/topic/${topicID}`, body),
  // Delete topic
  deleteCourseTopic: (courseID, topicID) => api.delete(`/course/${courseID}/topic/${topicID}`),
  // Show participants in specific course
  getCourseParticipants: (courseID) => api.get(`/course/${courseID}/show-participants`),
  // Get data for response for updating course
  getCourseUpdateResponse: (courseID) => api.get(`/course/${courseID}/responseforupdatecourse`),
  // Add course
  postNewCourse: (body) => api.post(`/course/add-course`, body),
  // Fetch group list
  getCourseGroupList: (courseID) => api.get(`/course/${courseID}/groupslist`),
  // Fetch group data
  getGroupData: (courseID, grouplistID) => api.get(`/course/${courseID}/group/${grouplistID}`),
  // Delete group version
  deleteGroupList: (courseID, grouplistID) => api.delete(`/course/${courseID}/group/${grouplistID}`),
  // Add group version
  postGroupList: (courseID, body) => api.post(`/course/${courseID}/group/add-grouplist`, body),
  // Upload course .csv file
  postUploadCourse: (body) => api.post(`/course/setting/upload-course`, body),
  // Check user group
  checkUserGroup: (topicID, userID) => api.get(`/course/topic/${topicID}/user/${userID}/checkusergroup`),
  // Get group version info
  getGroupVersionInfo: (topicID) => api.get(`/course/topic/${topicID}/getgroupversioninfo`),
}

export default Course
