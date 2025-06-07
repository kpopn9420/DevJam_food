<template>
  <div ref="menuContainer" class="relative">
    <Icons.IconMoreHorizontal class="w-5 h-5 transform rotate-90 cursor-pointer" @click="toggleMenu" />

    <transition name="fade">
      <div
        v-if="isMenuOpen"
        class="absolute right-0 mt-2 w-40 bg-white shadow-lg rounded-md border opacity-100 transition-opacity duration-200 ease-in-out"
      >
        <button
          class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
          @click="openEditCourseDialog"
        >
          編輯課程
        </button>
        <button
          class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
          @click="openDeleteCourseDialog"
        >
          刪除課程
        </button>
      </div>
    </transition>

    <PageDialog :is-open="isEditCourseOpen" dialog-title="編輯課程" @close="closeEditCourseDialog">
      <BaseInputPlace
        label="課程名稱"
        placeholder="Please enter the new name..."
        class="mb-2"
      ></BaseInputPlace>
      <BaseInputPlace
        label="開課年份"
        placeholder="Please enter the course year..."
        class="mb-2"
      ></BaseInputPlace>
      <BaseSelector
        size="md"
        headline="開課學期"
        :options="semesterOptions"
        :selection="semesterOptions.findIndex((option) => option.value === selectedSemester)"
        class="mb-2 w-auto"
        @update:model="onSemesterChange"
      />
      <BaseSelectorAutofill headline="教師" class="mb-4"></BaseSelectorAutofill>
      <BaseButtonFilled size="md" button-text="儲存"></BaseButtonFilled>
    </PageDialog>

    <PageDialog
      :is-open="isDeleteCourseOpen"
      dialog-title="是否確定刪除課程"
      @close="closeDeleteCourseDialog"
    >
      <div class="flex justify-between">
        <BaseButtonFilled
          size="md"
          button-text="確定"
          bg-color="bg-red-500"
          hover-color="hover:bg-red-700"
          class="mr-2"
        ></BaseButtonFilled>
        <BaseButtonFilled size="md" button-text="取消"></BaseButtonFilled>
      </div>
    </PageDialog>
  </div>
</template>

<script setup>
  import { ref, defineEmits, onMounted, onUnmounted } from 'vue'
  import * as Icons from '@iconify-prerendered/vue-jam'
  import PageDialog from './PageDialog.vue'
  import BaseButtonFilled from './BaseButtonFilled.vue'
  import BaseInputPlace from './BaseInputPlace.vue'
  import BaseSelector from './BaseSelector.vue'
  import BaseSelectorAutofill from './BaseSelectorAutofill.vue'

  const emit = defineEmits(['update:modelValue'])

  const isMenuOpen = ref(false)
  const isEditCourseOpen = ref(false)
  const isDeleteCourseOpen = ref(false)

  const toggleMenu = () => {
    isMenuOpen.value = !isMenuOpen.value
    emit('update:modelValue', isMenuOpen.value)
  }

  function openEditCourseDialog() {
    isMenuOpen.value = false
    isEditCourseOpen.value = true
  }

  function openDeleteCourseDialog() {
    isMenuOpen.value = false
    isDeleteCourseOpen.value = true
  }

  function closeEditCourseDialog() {
    isEditCourseOpen.value = false
  }

  function closeDeleteCourseDialog() {
    isDeleteCourseOpen.value = false
  }

  //   function confirmDeleteCourse() {
  //     console.log('刪除課程')
  //     closeDeleteCourseDialog()
  //   }

  // 點擊菜單外部關閉菜單
  const menuContainer = ref(null)
  function handleClickOutside(event) {
    if (menuContainer.value && !menuContainer.value.contains(event.target)) {
      isMenuOpen.value = false
      emit('update:modelValue', isMenuOpen.value)
    }
  }
  const selectedSemester = ref('Spring')
  const semesterOptions = [
    { id: 1, title: 'Spring', value: 'Spring' },
    { id: 2, title: 'Fall', value: 'Fall' },
  ]
  const onSemesterChange = (option) => {
    selectedSemester.value = option.value
  }

  onMounted(() => {
    document.addEventListener('click', handleClickOutside)
  })

  onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside)
  })
</script>
