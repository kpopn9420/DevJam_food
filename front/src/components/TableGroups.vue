<!-- eslint-disable vue/no-unused-vars -->
<template>
  <div class="overflow-x-auto rounded-md border">
    <table class="min-w-full bg-white shadow-md rounded-lg">
      <thead class="bg-gray-100">
        <tr>
          <th
            class="px-3 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider w-6/12 md:w-2/5"
          >
            {{ columnOne }}
          </th>
          <th
            class="px-3 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider w-4/12 md:w-2/5"
          >
            {{ columnTwo[mode] }}
          </th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200 align-middle flex-col items-center">
        <tr v-for="item in items" :key="item.title">
          <td class="px-6 py-4 whitespace-nowrap text-center">
            <div class="flex items-center text-center max-md:space-y-2 max-md:flex-col">
              <img :src="item.picture" alt="" class="w-10 h-10 rounded-full md:mr-3" />
              <div>
                <div class="text-sm font-medium text-gray-900">{{ item.title }}</div>
              </div>
            </div>
          </td>
          <td class="px-6 py-4 items-center text-center">
            <div v-if="mode === 'view'">
              <div v-if="item.isLeader" class="text-sm font-medium text-gray-900">組長</div>
              <div v-else class="text-sm font-medium text-gray-900">組員</div>
            </div>
            <div v-if="mode === 'edit'">
              <div class="flex justify-center">
                <TrashIcon
                  class="w-10 h-10 cursor-pointer rounded-md hover:text-gray-700 hover:bg-gray-100 text-gray-500 p-2"
                  @click="deleteMember(item.title)"
                />
              </div>
            </div>
            <div v-if="mode === 'new'">
              <div class="flex justify-center">
                <InputCheck v-model="clicked[item.title]" @change="handleInputClick(item.title)" />
              </div>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
  import { ref, reactive } from 'vue'
  import { TrashIcon } from '@heroicons/vue/24/outline'
  import InputCheck from '@/components/InputCheck.vue'

  defineProps({
    items: {
      type: Array,
      required: true,
    },
    mode: {
      type: String,
      required: true,
    },
    studentName: {
      type: String,
      required: true,
    },
  })

  const columnOne = '學生姓名'
  const columnTwo = {
    view: '身份',
    edit: '刪除',
    new: '新增',
  }

  const selectedStudent = ref('')
  const clicked = reactive({})
  const handleInputClick = (studentName) => {
    if (clicked[studentName]) {
      selectedStudent.value = studentName
      emit('add', studentName)
    } else {
      selectedStudent.value = ''
    }
    console.log('Student Selected', studentName)
  }

  const emit = defineEmits(['delete', 'add'])
  const deleteMember = (studentName) => {
    confirm('確認要刪除此學生嗎？')
    console.log('Member Deleted', studentName)
    emit('delete', studentName)
  }
</script>
