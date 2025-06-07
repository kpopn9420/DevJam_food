<template>
  <div :class="['p-4 flex', props.sidebarExpanded ? 'justify-between' : 'justify-center']">
    <router-link
      v-if="props.sidebarExpanded"
      to="/"
      class="text-base text-gray-700 hover:text-gray-900 p-2 font-semibold flex items-center"
      ><img src="/src/assets/logo.png" alt="logo" class="w-6 h-6 mr-2" />
      ClassBud
    </router-link>
    <button
      class="text-black rounded-lg p-1 hover:bg-gray-100 transition-all duration-100 ease-in-out transform"
      @click="props.expandSidebar"
    >
      <ChevronLeftIcon v-if="props.sidebarExpanded" class="w-6 h-6" />
      <Bars2Icon v-else class="w-6 h-6" />
    </button>
  </div>
</template>

<script setup>
  import { defineProps } from 'vue'
  import { Bars2Icon, ChevronLeftIcon } from '@heroicons/vue/24/outline'

  const props = defineProps({
    sidebarExpanded: Boolean,
    expandSidebar: {
      type: Function,
      default: () => {},
    },
  })
</script>
