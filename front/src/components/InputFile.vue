<template>
  <div
    :class="{ 'bg-green-200 bg-opacity-20 border-green-300': active }"
    class="border-gray-300 bg-gray-50 hover:bg-gray-100 w-full h-64 flex flex-col justify-center items-center border-2 border-dashed rounded-lg transition-all duration-300 ease-in-out"
    @dragenter.prevent="toggleActive"
    @dragleave.prevent="toggleActive"
    @dragover.prevent
    @drop.prevent="toggleActive"
  >
    <label
      class="w-full h-full flex flex-col cursor-pointer text-center justify-center items-center"
      for="dropzoneFile"
    >
      <CloudArrowUpIcon :class="{ 'text-green-500': active }" class="w-12 h-12 text-gray-400 mb-2" />
      <p>
        <span
          :class="{ 'text-green-700': active }"
          class="font-semibold text-gray-500 transition-all duration-300 ease-in-out"
          >將檔案拖曳至此</span
        >
        <span
          :class="{ 'text-green-700': active }"
          class="text-gray-500 transition-all duration-300 ease-in-out"
          >或</span
        >
        <span
          :class="{ 'text-green-700': active }"
          class="text-gray-500 transition-all duration-300 ease-in-out"
          >點擊以選擇檔案</span
        >
      </p>
      <p
        :class="{ 'text-green-500': active }"
        class="text-xs text-gray-500 transition-all duration-300 ease-in-out"
      >
        {{ fileTypes }}
      </p>
    </label>
    <input id="dropzoneFile" type="file" class="hidden" />
  </div>
</template>

<script setup>
  import { CloudArrowUpIcon } from '@heroicons/vue/24/outline'
  import { defineProps } from 'vue'
  import { ref } from 'vue'
  const props = defineProps({
    fileTypes: {
      type: String,
      default: 'SVG, PNG, JPG or GIF (MAX. 800x400px)',
    },
  })
  console.log(props.fileTypes)
  const active = ref(false)

  const toggleActive = () => {
    active.value = !active.value
  }
</script>
