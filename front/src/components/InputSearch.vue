<template>
  <form class="max-w-full">
    <div class="relative items-center">
      <div class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
        <IconSearch class="w-5 h-5 text-gray-400" />
      </div>
      <input
        type="search"
        :placeholder="placeholder"
        class="w-full py-2 px-2 ps-10 pe-4 border text-sm focus:outline-none"
        :class="sizeClasses[size]"
        required
      />
    </div>
  </form>
</template>

<script setup>
import { IconSearch } from '@iconify-prerendered/vue-jam'

defineProps({
  size: {
    type: String,
    default: 'base',
    validator: (value) => ['sm', 'md', 'base', 'lg'].includes(value),
  },
  placeholder: {
    type: String,
    default: 'Search...',
  }
})

const sizeClasses = {
  base: 'rounded-lg',
  lg: 'h-12 rounded-md',
  md: 'h-10 rounded-lg',
  sm: 'h-8 rounded-full',
}
</script>
