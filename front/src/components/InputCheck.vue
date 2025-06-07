<template>
  <div class="flex items-center">
    <label class="relative flex cursor-pointer items-center mr-2" for="icon">
      <input
        id="icon"
        type="checkbox"
        :checked="modelValue"
        class="peer relative h-5 w-5 cursor-pointer appearance-none rounded border border-gray-300 shadow hover:shadow-md transition-all before:absolute before:top-2/4 before:left-2/4 before:block before:h-8 before:w-8 before:-translate-y-2/4 before:-translate-x-2/4 before:rounded-full before:bg-gray-400 before:opacity-0 before:transition-opacity checked:bg-blue-500 checked:before:bg-blue-300 hover:before:opacity-10"
        @change="toggleChecked"
      />
      <IconCheck
        class="pointer-events-none absolute top-2/4 left-2/4 -translate-y-2/4 -translate-x-2/4 text-white opacity-0 transition-opacity peer-checked:opacity-100 w-5 h-5"
      />
    </label>
    <slot></slot>
  </div>
</template>

<script setup>
  import { defineProps, defineEmits } from 'vue'
  import { IconCheck } from '@iconify-prerendered/vue-jam'

  const props = defineProps({
    modelValue: Boolean,
  })

  const emit = defineEmits(['update:modelValue'])

  const toggleChecked = () => {
    emit('update:modelValue', !props.modelValue)
  }
</script>
