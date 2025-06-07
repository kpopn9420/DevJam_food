import { defineStore } from 'pinia'

export const useGroupStore = defineStore('groupStore', {
  state: () => ({
    groupList: [],
    groupData: {},
  }),
  actions: {},
})
