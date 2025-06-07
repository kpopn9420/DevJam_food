<template>
  <div
    class="bg-white p-4 border rounded-lg hover:shadow-md flex flex-col space-y-2 relative transition-all duration-200"
  >
    <!-- Group Title -->
    <div class="text-lg font-semibold">{{ computedGroupName }}</div>

    <!-- Members Section -->
    <div class="flex -space-x-4 rtl:space-x-reverse hover:space-x-1">
      <div
        v-for="(member, index) in firstThreeMembers"
        :key="index"
        class="relative group transition-all duration-200"
      >
        <img
          :src="member.picture"
          :alt="member.title"
          class="w-14 h-14 lg:w-16 lg:h-16 rounded-full border hover:ring-2 ring-blue-500 transition-all duration-200"
        />
        <!-- Tooltip -->
        <div
          class="absolute bottom-12 left-1/2 transform -translate-x-1/2 px-2 py-1 bg-gray-100 text-gray-700 text-sm rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap"
        >
          {{ member.title }}
        </div>
      </div>
      <!-- Extra member count icon if there are more than 3 members -->
      <div
        v-if="extraMemberCount > 0"
        class="relative w-14 h-14 lg:w-16 lg:h-16 rounded-full z-10 bg-gray-300 flex items-center justify-center text-base font-medium text-gray-700 group"
      >
        +{{ extraMemberCount }}
        <!-- Tooltip for extra members -->
        <div
          class="absolute bottom-12 left-1/2 transform -translate-x-1/2 px-2 py-1 bg-gray-100 text-gray-700 text-sm rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap"
        >
          <span v-for="(member, index) in regularMembers.slice(3)" :key="index">
            {{ member.title }}<span v-if="index < regularMembers.length - 4">, </span>
          </span>
        </div>
      </div>
    </div>

    <div
      v-if="isStudentInGroup"
      class="absolute bottom-3 right-3 w-fit mt-2 px-2 py-1 bg-amber-100 text-amber-600 text-xs rounded-full"
    >
      你的組別
    </div>

    <!-- Menu Button and Items -->
    <Menu>
      <MenuButton
        class="absolute top-1 right-3 px-2 py-2 text-xs font-medium rounded-md hover:bg-gray-100 transition-all duration-100"
      >
        <IconMoreVertical class="w-4 h-4 text-gray-500" />
      </MenuButton>
      <MenuItems
        class="absolute top-0 z-10 mt-2 w-56 p-2 divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black/5 focus:outline-none origin-top-right"
      >
        <MenuItem>
          <button
            :class="['group flex w-full items-center rounded-md px-2 py-2 text-sm hover:bg-gray-100']"
            @click="openGroup"
          >
            <IconEye class="w-4 h-4 text-gray-500 mr-2" />
            檢視
          </button>
        </MenuItem>
        <MenuItem>
          <button
            v-show="userGroup === 'teacher' && isEditable"
            :class="['group flex w-full items-center rounded-md px-2 py-2 text-sm hover:bg-gray-100']"
            @click="openEditGroup"
          >
            <IconPen class="w-4 h-4 text-gray-500 mr-2" />
            編輯
          </button>
        </MenuItem>
        <MenuItem>
          <button
            v-show="userGroup === 'teacher' && isEditable"
            :class="['group flex w-full items-center rounded-md px-2 py-2 text-sm hover:bg-gray-100']"
            @click="deleteGroup"
          >
            <IconTrashAlt class="w-4 h-4 text-red-500 mr-2" />
            刪除
          </button>
        </MenuItem>
      </MenuItems>
    </Menu>
  </div>
  <PageDialog :dialog-title="computedGroupName" class="hidden" :is-open="showGroup" @close="closeGroup">
    <TableGroups mode="view" :student-name="studentName" :items="members"></TableGroups>
    <div class="mt-4">
      <BaseButtonFilled
        width="w-full"
        button-text="關閉"
        bg-color="bg-gray-300 hover:bg-gray-500"
        @click="closeGroup"
      ></BaseButtonFilled>
    </div>
  </PageDialog>
  <PageDialog :dialog-title="computedGroupName" class="hidden" :is-open="editGroup" @close="closeEditGroup">
    <div v-if="editGroupMember">
      <div class="bg-gray-100 rounded-md border items-center">
        <TableGroups
          mode="edit"
          class="border-0 border-b rounded-b-none"
          :items="members"
          @delete="deleteStudent"
        ></TableGroups>
        <BaseButtonGhost
          button-text="新增組員"
          size="sm"
          class="my-1 rounded-lg"
          text-color="text-gray-500 text-sm"
          hover-color="hover:bg-white/50"
          @click="openNewMember()"
        ></BaseButtonGhost>
      </div>
      <div class="mt-4 space-x-2 flex">
        <BaseButtonFilled
          button-text="取消"
          width="w-full"
          bg-color="bg-red-500 hover:bg-red-700"
          @click="editGroupMember = false"
        />
        <BaseButtonFilled width="w-full" button-text="儲存" @click="editGroupMember = false" />
      </div>
    </div>
    <div v-else-if="addGroupMember">
      <TableGroups mode="new" :items="ungroupedMembers" @add="addStudent"></TableGroups>
      <div class="mt-4 space-x-2 flex">
        <BaseButtonFilled
          button-text="取消"
          width="w-full"
          bg-color="bg-red-500 hover:bg-red-700"
          @click="closeNewMember()"
        />
        <BaseButtonFilled width="w-full" button-text="儲存" @click="closeNewMember()" />
      </div>
    </div>
    <div v-else>
      <div>
        <div class="flex items-center space-x-2 mb-4">
          <BaseInputPlace
            v-model="newGroupName"
            size="lg"
            label="組別名稱"
            placeholder="請填寫需更改的組別名稱"
          />
          <BaseButtonFilled button-text="" size="lg" width="w-14" class="mt-8" @click="changeGroupName"
            ><IconCheck class="w-6 h-6"
          /></BaseButtonFilled>
        </div>
        <BaseButtonFilled
          button-text="點擊以編輯組員"
          width="w-full"
          class="mb-4"
          @click="editGroupMember = true"
        ></BaseButtonFilled>
      </div>
      <div>
        <BaseButtonFilled
          width="w-full"
          button-text="關閉"
          bg-color="bg-gray-300 hover:bg-gray-500"
          @click="closeEditGroup"
        ></BaseButtonFilled>
      </div>
    </div>
  </PageDialog>
</template>

<script setup>
  import { computed, ref } from 'vue'
  import { IconMoreVertical, IconTrashAlt, IconEye, IconPen, IconCheck } from '@iconify-prerendered/vue-jam'
  import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/vue'
  import PageDialog from './PageDialog.vue'
  import TableGroups from './TableGroups.vue'
  import BaseButtonFilled from './BaseButtonFilled.vue'
  import BaseInputPlace from './BaseInputPlace.vue'
  import BaseButtonGhost from './BaseButtonGhost.vue'
  import { defineEmits } from 'vue'

  // Define props for GroupCard component
  const props = defineProps({
    groupName: {
      type: String,
      default: '',
    },
    studentName: {
      type: String,
      default: '',
    },
    members: {
      type: Array,
      required: true,
    },
    userGroup: {
      type: String,
      required: true,
    },
    isEditable: {
      type: Boolean,
      default: false,
    },
    ungroupedMembers: {
      type: Array,
      required: true,
    },
  })

  // Storing group name for adding a new member to the group
  const addToGroup = ref('')

  // Computed property to handle group naming logic
  const computedGroupName = computed(() => {
    if (props.groupName === '' || props.groupName === null || props.groupName === undefined) {
      return 'Ungrouped'
    }
    return typeof props.groupName === 'number' ? `Group ${props.groupName}` : props.groupName
  })

  const regularMembers = computed(() => props.members)

  // Computed properties for member display when there is no leader
  const firstThreeMembers = computed(() => regularMembers.value.slice(0, 3))
  const extraMemberCount = computed(() => regularMembers.value.length - 3)

  // Show group modal dialog
  const showGroup = ref(false)
  const closeGroup = () => {
    showGroup.value = false
  }
  const openGroup = () => {
    console.log(props.members)
    showGroup.value = true
  }

  // Edit group modal dialog
  const editGroup = ref(false)
  const closeEditGroup = () => {
    editGroup.value = false
  }
  const openEditGroup = () => {
    editGroup.value = true
  }

  const openNewMember = () => {
    addToGroup.value = props.groupName
    addGroupMember.value = true
    editGroupMember.value = false
  }

  const closeNewMember = () => {
    addGroupMember.value = false
    editGroupMember.value = true
  }

  const addGroupMember = ref(false)
  const editGroupMember = ref(false)

  const emit = defineEmits(['delete', 'deleteStudent', 'addStudent', 'change'])
  // Delete Group
  const deleteGroup = () => {
    confirm('確認要刪除此群組嗎？')
    console.log('Group Deleted')
    emit('delete', props.groupName)
  }

  // Change group name
  const newGroupName = ref(props.groupName)
  const changeGroupName = () => {
    console.log('change group name')
    emit('change', newGroupName.value, props.groupName)
  }

  // Computed property to check if the user is a student and in the group
  const isStudentInGroup = computed(() => {
    return props.userGroup === 'student' && props.members.some((member) => member.title === props.studentName)
  })

  const addStudent = (studentName) => {
    emit('addStudent', studentName, addToGroup.value)
    console.log('add student', studentName, addToGroup.value)
  }

  const deleteStudent = (studentName) => {
    emit('deleteStudent', studentName)
    console.log('delete student', studentName)
  }
</script>
