<template>
  <div>
    <label class="block mb-2 text-gray-700" :class="labelVisible ? '' : 'hidden'">{{ label }}</label>
    <textarea
      ref="textarea"
      v-model="inputValue"
      :class="[
        'block w-full py-3 ps-4 border text-sm max-h-24 p-2 focus:ring-2 focus:ring-blue-500 focus:caret-blue-500 focus:outline-none',
        hasInnerButton ? 'pe-16' : 'pe-4',
        sizeClasses[size],
        isChatText ? 'resize-none' : '',
      ]"
      type="text"
      :placeholder="placeholder"
      @input="handleInput"
    />
  </div>
</template>

<script setup>
  import { defineProps, ref, watch, onMounted } from 'vue'

  const props = defineProps({
    label: {
      type: String,
      required: true,
    },
    placeholder: {
      type: String,
      default: '',
    },
    modelValue: {
      type: String,
      default: '',
    },
    labelVisible: {
      type: Boolean,
      default: true,
    },
    hasInnerButton: {
      type: Boolean,
      default: false,
    },
    size: {
      type: String,
      default: 'base',
      validator: (value) => ['sm', 'md', 'base', 'lg'].includes(value),
    },
    isChatText: {
      type: Boolean,
      default: false,
    },
    reset: {
      type: Boolean,
      default: false,
    },
  })
  const emit = defineEmits(['update:modelValue'])

  const inputValue = ref(props.modelValue)

  const sizeClasses = {
    base: 'min-h-20 rounded-lg',
    lg: 'min-h-12 h-12 rounded-md',
    md: 'min-h-10 h-10 rounded-lg',
    sm: 'min-h-8 h-8 rounded-full',
  }

  // Function to resize the textarea based on content up to a max height
  const textarea = ref(null)
  const resizeTextarea = () => {
    const el = textarea.value
    el.style.height = '' // reset to auto to recalculate height
    el.style.height = `${Math.min(el.scrollHeight, 96)}px` // set height with a max of 96px (h-24 in Tailwind)
  }

  // Function to reset height to h-10 after sending
  const resetTextareaHeight = () => {
    const el = textarea.value
    el.style.height = '2.5rem' // equivalent to h-10 in Tailwind
  }

  // Handle input, resize, and reset after sending
  const handleInput = () => {
    emit('update:modelValue', inputValue.value)
    resizeTextarea()
    resetTextareaHeight()
  }

  // Watch for external changes in modelValue and resize textarea accordingly
  watch(
    () => props.modelValue,
    (newValue) => {
      inputValue.value = newValue
      resizeTextarea()
    }
  )
  watch(
    () => props.reset,
    (newValue) => {
      if (newValue) {
        resetTextareaHeight()
      }
    }
  )

  // Initial resize when the component mounts
  onMounted(() => {
    resizeTextarea()
  })
</script>
