<!-- eslint-disable vue/no-template-shadow -->
<template>
  <PageLayout headline="分組系統">
    <div class="w-full align-top flex max-lg:flex-col justify-between">
      <div class="justify-start">
        <span class="text-gray-700 font-bold leading-none">現在時間：</span
        ><span class="text-gray-700 font-normal leading-none">{{ time }}</span>
      </div>
      <div class="w-auto lg:-mt-4 justify-end flex space-x-2">
        <BaseButtonFilled
          v-if="isEditing"
          size="md"
          width="w-40"
          button-text="+ 新增組別"
          @click="openNewGroup"
        ></BaseButtonFilled>
        <BaseSelector
          v-model="selectedGroupList"
          class="-mt-2 z-20 w-full max-w-44"
          headline=""
          :options="groupList"
          :selection="groupList.findIndex((option) => option.id === selectedGroupList.id)"
          :headline-visible="true"
          size="md"
        />
        <Menu v-if="userGroup === 'teacher'">
          <BaseButtonFilled size="md" width="w-48" button-text="返回課程" @click="ReturnCoursePage">
          </BaseButtonFilled>
          <MenuButton
            class="px-3 py-2 text-sm items-center font-medium rounded-md hover:bg-gray-100 transition-all duration-100"
          >
            <IconMoreVertical class="w-4 h-4 text-gray-500" />
          </MenuButton>
          <MenuItems
            class="absolute z-20 mt-2 w-56 p-2 divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black/5 focus:outline-none origin-top-right"
          >
            <MenuItem>
              <button
                :class="['group flex w-full items-center rounded-md px-2 py-2 text-sm hover:bg-gray-100']"
                @click="openAddGroupList"
              >
                <IconPen class="w-4 h-4 text-gray-500 mr-2" />
                新增分組版本
              </button>
            </MenuItem>
            <MenuItem>
              <button
                :class="[
                  'group flex w-full items-center rounded-md px-2 py-2 text-sm text-red-500 hover:bg-gray-100',
                ]"
                @click="openDeleteGroupList"
              >
                <IconTrashAlt class="w-4 h-4 text-red-500 mr-2" />
                刪除分組版本
              </button>
            </MenuItem>
          </MenuItems>
        </Menu>
      </div>
    </div>
    <div
      v-if="!dataProcessed"
      class="flex left-1/2 text-gray-500 items-center inset-0 justify-center top-1/2"
    >
      <IconBarsRotateFade class="h-8 w-8" />
    </div>
    <div v-else>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <GroupCard
          v-for="(members, group) in groupedMembers"
          :key="group"
          :group-name="group"
          :members="members"
          :user-group="userGroup"
          :student-name="studentName"
          :is-editable="isEditing"
          :ungrouped-members="ungroupedStudents"
          @delete="deleteGroup"
          @change="changeGroupName"
          @delete-student="deleteStudent"
          @add-student="addStudent"
        />
      </div>
    </div>
    <BaseButtonFilled
      v-if="isEditing"
      class="absolute bottom-4 right-4"
      width="w-fit"
      button-text="儲存分組"
      @click="submitNewGroupList"
    />
  </PageLayout>
  <!-- Add Group Dialog -->
  <PageDialog dialog-title="新增分組" :is-open="addGroupListDialog" class="hidden" @close="closeAddGroupList">
    <div class="flex justify-between items-center mb-4">
      <BaseInputPlace v-model="newGroupListName" label="新版本名稱" placeholder="請輸入名稱" />
    </div>
    <div class="mb-4">
      <InputCheck v-model="newGroupBasis.enabled">
        <span class="text-gray-700">是否使用現有分組版本調整？</span></InputCheck
      >
    </div>
    <div class="mb-4">
      <BaseSelector
        v-if="newGroupBasis.enabled"
        v-model="selectedGroupList"
        :disabled="!newGroupBasis.enabled"
        class="-mt-2 z-20 w-full"
        headline="選擇現有分組版本"
        :options="groupList"
        :selection="groupList.findIndex((option) => option.id === selectedGroupList.id)"
        size="base"
        :headline-visible="true"
      />
    </div>
    <div class="flex justify-between items-center mt-4">
      <h2 class="text-lg font-bold"></h2>
      <BaseButtonFilled width="w-full" button-text="新增" @click="editGroups"></BaseButtonFilled>
    </div>
  </PageDialog>
  <!-- Delete Group Dialog -->
  <PageDialog
    dialog-title="刪除分組"
    class="hidden"
    :is-open="deleteGroupListDialog"
    @close="closeDeleteGroupList"
  >
    <div class="mb-4 text-center text-base text-gray-700">確定要刪除此分組版本嗎？</div>
    <div class="mt-4 flex space-x-2">
      <BaseButtonFilled button-text="取消" />
      <BaseButtonFilled button-text="確定" bg-color="bg-red-500 hover:bg-red-700" @click="deleteGroupList" />
    </div>
  </PageDialog>
  <PageDialog dialog-title="重設組別" :is-open="deleteAllGroup" @close="closeDeleteAllGroup">
    <div class="mb-4 text-center w-full">
      <p class="text-gray-700 text-sm">您確定要重設所有組別嗎？這將清空所有現有的組別資料。</p>
    </div>
    <div class="flex justify-end space-x-4">
      <BaseButtonFilled
        size="md"
        width="w-fit"
        bg-color="bg-red-500"
        hover-color="hover:bg-red-700"
        button-text="確認重設"
        @click="resetGroups"
      />
      <BaseButtonFilled size="md" width="w-fit" button-text="取消" @click="closeDeleteAllGroup" />
    </div>
  </PageDialog>
  <PageDialog dialog-title="新增組別" class="hidden" :is-open="isNewGroupDialogOpen" @close="closeNewGroup">
    <div class="mb-4">
      <BaseInputPlace v-model="newGroupName" label="組別名稱" placeholder="請填寫組別名稱" />
    </div>
    <BaseButtonGhost
      button-text="新增組員"
      size="sm"
      class="my-1 rounded-lg"
      text-color="text-gray-500 text-sm"
      hover-color="hover:bg-white/50"
      @click="openNewMembers"
    ></BaseButtonGhost>
    <BaseButtonFilled width="w-full" button-text="新增" class="mt-4" @click="addGroup"></BaseButtonFilled>
    <!-- 重要 -->
    <PageDialog
      :dialog-title="'請選擇組員'"
      class="hidden"
      :is-open="isNewMembersDialogOpen"
      @close="cancelNewMembers"
    >
      <TableGroups mode="new" :items="ungroupedStudents" @add="handleNewMembers"></TableGroups>
      <div class="mt-4 space-x-2 flex">
        <BaseButtonFilled
          button-text="取消"
          width="w-full"
          bg-color="bg-red-500 hover:bg-red-700"
          @click="cancelNewMembers"
        />
        <BaseButtonFilled width="w-full" button-text="選擇" @click="closeNewMembers" />
      </div>
    </PageDialog>
  </PageDialog>
</template>

<script setup>
  import { computed, onMounted, ref, watch } from 'vue'
  import { useRouter, useRoute } from 'vue-router'
  import Course from '@/api/course'
  import GroupCard from '@/components/GroupCard.vue'
  import PageLayout from '@/components/PageLayout.vue'
  import BaseButtonFilled from '@/components/BaseButtonFilled.vue'
  import PageDialog from '@/components/PageDialog.vue'
  import BaseInputPlace from '@/components/BaseInputPlace.vue'
  import BaseSelector from '@/components/BaseSelector.vue'
  import BaseButtonGhost from '@/components/BaseButtonGhost.vue'
  import TableGroups from '@/components/TableGroups.vue'
  import InputCheck from '@/components/InputCheck.vue'
  import { IconMoreVertical, IconTrashAlt, IconPen } from '@iconify-prerendered/vue-jam'
  import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/vue'
  import { IconBarsRotateFade } from '@iconify-prerendered/vue-svg-spinners'
  import { useResourceStore } from '@/stores/resource.js'
  const resourceStore = useResourceStore()

  const time = new Date().toDateString()
  // To show the loading spinner
  const dataProcessed = ref(false)

  // Fetch grouplist and set it to the first option
  const groupList = ref([])
  // Controls which group list is selected with the selector
  const selectedGroupList = ref([])
  const fetchGroupList = async () => {
    try {
      const courseId = 1
      const response = await Course.getGroupList(courseId)

      groupList.value = response.data.map((item) => ({
        id: item.groupListId,
        title: item.groupName,
      }))
    } catch (error) {
      console.error(error)
      // Fallback data
      groupList.value = [
        { id: 1, title: '分組版本 1' },
        { id: 2, title: '分組版本 2' },
      ]
      selectedGroupList.value = groupList.value[0]
      console.log('groupList:', groupList.value)
      console.log('selectedGroupList:', selectedGroupList.value)
      console.log(
        'test',
        groupList.value.findIndex((option) => option.id === selectedGroupList.value.id)
      )
    }
  }

  // Show group data when selectedGroupList changes
  watch(selectedGroupList, (newValue) => {
    console.log('new selectedGroupList:', newValue)
    fetchGroupData()
  })

  // Fetch group data in a grouplist
  const groupData = ref([])
  const fetchGroupData = async () => {
    try {
      const courseId = 1
      const response = await Course.getGroupData(courseId, selectedGroupList.value.id)
      groupData.value = response.data.groups
    } catch (error) {
      console.error(error)
      groupData.value = [
        {
          groupId: '1',
          groupName: 'Group A',
          students: [
            {
              studentId: '01BJQE4QTHMFP0S5J153XCFSP9',
              studentName: 'andy',
              studentImage: '',
              imageType: 'png',
            },
          ],
        },
      ]
    }
  }

  // Get all participants of the course to filter out ungrouped students
  const students = ref([])
  const fetchStudents = async () => {
    try {
      const courseId = 1
      const response = await Course.getCourseParticipants(courseId)
      students.value = response.data.filter((participant) => participant.participantsRole === 'student')
    } catch (error) {
      console.error(error)
      students.value = [
        {
          participantsID: '12312',
          participantsName: 'Neokent',
          participantsSerialNumber: '12312',
          participantsRole: 'student',
          profileImage: '',
          imageType: 'png',
        },
        {
          participantsID: '01BJQE4QTHMFP0S5J153XCFSP9',
          participantsName: 'andy',
          participantsSerialNumber: '01BJQE4QTHMFP0S5J153XCFSP9',
          participantsRole: 'student',
          profileImage: '',
          imageType: 'png',
        },
      ]
    }
  }

  // Whatever happened here was between me and god
  const members = ref([])
  const processGroupAndStudentData = () => {
    const groupedStudentsMap = new Map()
    // Map all grouped students for quick lookup
    groupData.value.forEach((group) => {
      group.students.forEach((student) => {
        groupedStudentsMap.set(student.studentId, group.groupName)
      })
    })

    members.value = students.value.map((student) => {
      const groupName = groupedStudentsMap.get(student.participantsID) || ''
      return {
        title: student.participantsName || 'Unnamed',
        picture: student.profileImage || '/src/assets/profile-placeholder.jpg',
        group: groupName,
      }
    })
    console.log('Final members:', members.value)
    dataProcessed.value = true
  }

  const groupedMembers = computed(() => {
    return members.value.reduce((acc, member) => {
      if (!acc[member.group]) acc[member.group] = []
      acc[member.group].push(member)
      return acc
    }, {})
  })

  const ungroupedStudents = computed(() => {
    return members.value.filter((member) => !member.group)
  })

  // To display which group the student is in
  const studentName = ref('andy')

  const fetchDataAndProcess = async () => {
    await Promise.all([fetchGroupData(), fetchStudents()])
    processGroupAndStudentData()
  }

  // Add group list
  const addGroupListDialog = ref(false)
  const openAddGroupList = () => {
    addGroupListDialog.value = true
  }
  const closeAddGroupList = () => {
    addGroupListDialog.value = false
  }

  const isEditing = ref(false)
  const editGroups = () => {
    if (!newGroupListName.value || newGroupListName.value.trim() === '') {
      alert('請填寫群組名稱！')
      return
    }
    isEditing.value = true
    if (newGroupBasis.value.enabled) {
      // fetch selected group data to create a new group list based on that list
      fetchGroupData()
      processGroupAndStudentData()
    } else {
      // just use students data to create a new group list
      fetchStudents()
      clearGroups()
      processGroupAndStudentData()
    }
    closeAddGroupList()
  }

  // Clear the group data if the user decides to start fresh
  const clearGroups = () => {
    groupData.value = []
  }

  const newGroupListName = ref('')
  const newGroupBasis = ref({
    basedOn: groupList.value[0],
    enabled: false,
  })

  const newGroupList = ref({
    grouplist: {
      grouplistName: '',
      'group-data': [],
    },
  })

  // TODO: 在新增groupList後新增組別按鈕邏輯、編輯組別、刪除組別

  const newGroupName = ref('')

  // Control "new group" dialog
  const isNewGroupDialogOpen = ref(false)
  const openNewGroup = () => {
    isNewGroupDialogOpen.value = true
  }
  const closeNewGroup = () => {
    isNewGroupDialogOpen.value = false
    console.log('closeNewGroup')
  }

  // Control "add new members" dialog
  const isNewMembersDialogOpen = ref(false)
  const closeNewMembers = () => {
    isNewMembersDialogOpen.value = false
  }
  const openNewMembers = () => {
    isNewMembersDialogOpen.value = true
  }

  const membersToAdd = ref([])
  const handleNewMembers = (studentName) => {
    membersToAdd.value.push(studentName)
    console.log('handleNewMembers', studentName)
  }

  const cancelNewMembers = () => {
    closeNewMembers()
    membersToAdd.value = []
    console.log('saveNewMembers')
  }

  const addGroup = () => {
    members.value = members.value.map((member) => {
      if (membersToAdd.value.includes(member.title)) {
        return { ...member, group: newGroupName.value } // Update group name
      }
      return member // Keep unchanged members
    })
    console.log('add group')
    closeNewGroup()
  }

  const deleteGroup = (groupName) => {
    members.value = members.value.map((member) => {
      if (member.group === groupName) {
        return {
          ...member,
          group: '',
        }
      }
      return member
    })
  }

  // Edit group related code
  const changeGroupName = (newGroupName, oldGroupName) => {
    members.value = members.value.map((member) => {
      if (member.group === oldGroupName) {
        return {
          ...member,
          group: newGroupName,
        }
      }
      return member
    })
  }

  const addStudent = (studentName, groupName) => {
    members.value = members.value.map((member) => {
      if (member.title === studentName) {
        return {
          ...member,
          group: groupName,
        }
      }
      return member
    })
  }

  const deleteStudent = (studentName) => {
    members.value = members.value.map((member) => {
      if (member.title === studentName) {
        return {
          ...member,
          group: '',
        }
      }
      return member
    })
  }

  const convertDataToBackendFormat = () => {
    const groupData = Object.entries(groupedMembers.value).map(([groupName, members]) => ({
      groupName,
      students: members.map((member) => {
        const student = students.value.find((student) => student.participantsName === member.title) // Match member.title with participantsName
        return {
          studentId: student ? student.participantsSerialNumber : '', // Use participantsSerialNumber
        }
      }),
    }))
    newGroupList.value = {
      grouplistName: newGroupListName.value,
      'group-data': groupData,
    }
  }

  const submitNewGroupList = async () => {
    try {
      const courseId = 1
      convertDataToBackendFormat()
      console.log('newGroupList', newGroupList.value)
      await Course.postGroupList(courseId, newGroupList.value)
      fetchGroupList()
    } catch (error) {
      console.error(error)
      alert('新增分組版本失敗')
    }
    closeAddGroupList()
  }

  // Delete group list
  const deleteGroupListDialog = ref(false)
  const openDeleteGroupList = () => {
    deleteGroupListDialog.value = true
  }
  const closeDeleteGroupList = () => {
    deleteGroupListDialog.value = false
  }

  const deleteGroupList = async () => {
    try {
      const courseId = 1
      await Course.deleteGroupList(courseId, selectedGroupList.value.id)
      fetchGroupList()
    } catch (error) {
      console.error(error)
      alert('刪除分組版本失敗')
    }
    closeDeleteGroupList()
  }

  // User group logic (to be removed)
  const userGroup = resourceStore.userInfo.userRole

  const route = useRoute()
  const router = useRouter()
  function ReturnCoursePage() {
    const courseId = route.params.id
    router.push({ name: 'Course', params: { id: courseId } })
  }

  onMounted(() => {
    fetchGroupList()
    fetchDataAndProcess()
  })
</script>
