import { defineStore } from 'pinia'

// import { useResourceStore } from '@/stores/resourceStore'
// const resourceStore = useResourceStore()
// const userId = resourceStore.userInfo.userId
export const useResourceStore = defineStore('resourceStore', {
  state: () => ({
    userSettings: {
      language: 'en-us',
      theme: 'auto',
      profileImage: '/src/assets/profile-placeholder.jpg',
    },
    userInfo: {
      name: 'John Doe',
      role: 'student',
    },
    schoolId: null,
  }),
  getters: {},
  actions: {
    updateUserInfo(userInfo) {
      this.userInfo = userInfo
      sessionStorage.setItem('userInfo', JSON.stringify(userInfo))
    },
    updateSchoolId(schoolId) {
      this.schoolId = schoolId
      sessionStorage.setItem('schoolId', schoolId)
    },
  },
})
