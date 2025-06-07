<template>
  <div class="flex flex-col space-y-1">
    <label :for="inputId" class="text-sm font-medium text-gray-700">{{ label }}</label>
    <input
      :id="inputId"
      v-model="proxyValue"
      type="date"
      class="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      :min="min"
      :max="max"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { nanoid } from 'nanoid'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  label: {
    type: String,
    default: '選擇日期'
  }
})

const emit = defineEmits(['update:modelValue'])

const proxyValue = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const inputId = `datepicker-${nanoid(6)}`
</script>
