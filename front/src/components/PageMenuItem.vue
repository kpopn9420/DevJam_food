<template>
  <button
    class="self-stretch rounded-md h-10 px-2 py-3 justify-start text-left inline-flex hover:bg-gray-100 transition-all duration-100"
    :class="isActive ? 'bg-gray-100 hover:bg-gray-200' : ''"
    @click="isClicked"
  >
    <div
      class="grow shrink basis-0 text-base font-medium leading-none"
      :class="isActive ? 'text-gray-900' : 'text-gray-700'"
    >
      {{ headline }}
    </div>
  </button>
</template>

<script setup>
  defineProps({
    headline: {
      type: String,
      required: true,
      default: '標題',
    },
    isActive: {
      type: Function,
      required: true,
    },
    isClicked: {
      type: Function,
      required: true,
    },
  })
</script>
