<template>
  <div class="relative w-full items-center block">
    <label class="block mb-2 text-gray-700" :class="[labelVisible ? '' : 'hidden']">{{ label }}</label>
    <input
      v-model="inputValue"
      class="w-full py-3 ps-4 border text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:caret-blue-500"
      :type="type"
      :class="[sizeClasses[size], hasInnerButton ? 'pe-16' : 'pe-4']"
      :placeholder="placeholder"
      :disabled="isDisabled"
      @input="$emit('update:modelValue', inputValue)"
    />
    <slot></slot>
  </div>
</template>

<script setup>
  import { defineProps, ref, watch, defineEmits } from 'vue'

  const props = defineProps({
    modelValue: {
      type: String,
      default: '',
    },
    label: {
      type: String,
      default: '',
    },
    placeholder: {
      type: String,
      default: 'example@example.com',
    },
    type: {
      type: String,
      default: 'text',
    },
    isDisabled: {
      type: Boolean,
      default: false,
    },
    labelVisible: {
      type: Boolean,
      default: true,
    },
    size: {
      type: String,
      default: 'base',
      validator: (value) => ['sm', 'md', 'base', 'lg'].includes(value),
    },
    hasInnerButton: {
      type: Boolean,
      default: false,
    },
  })

  const emit = defineEmits(['update:modelValue'])

  const inputValue = ref(props.modelValue)

  const sizeClasses = {
    base: 'rounded-lg',
    lg: 'h-12 rounded-md',
    md: 'h-10 rounded-lg',
    sm: 'h-8 rounded-full',
  }

  watch(
    () => props.modelValue,
    (newValue) => {
      inputValue.value = newValue
    }
  )

  watch(inputValue, (newValue) => {
    emit('update:modelValue', newValue)
  })
</script>
