<template>
  <div
    class="w-full max-w-sm rounded-lg border border-dashed border-indigo-200 shadow-md overflow-hidden bg-white hover:shadow-lg transition"
  >
    <!-- Header: Title + Image -->
    <div class="p-4 pb-0">
      <!-- Title -->
      <h2 class="text-sm font-medium text-gray-900 mb-2">
        {{ title }}
      </h2>

      <!-- Image -->
      <div class="relative aspect-video w-full overflow-hidden rounded-md bg-gray-200">
        <img
          v-if="imageUrl"
          :src="imageUrl"
          :alt="imageAlt || title"
          class="h-full w-full object-cover"
        />
        <div v-else class="flex h-full w-full items-center justify-center">
          <div class="rounded-md border-2 border-gray-300 p-4">
            <X class="h-12 w-12 text-gray-400" />
          </div>
        </div>
      </div>
    </div>

    <!-- Footer: Icons + More -->
    <div class="flex justify-between items-center px-4 py-2">
        <!-- 左側：頭像區塊 + 更多按鈕 -->
        <div class="flex items-center space-x-1">
        <!-- 使用者頭像 -->
        <div
            v-for="n in 4"
            :key="n"
            class="w-6 h-6 rounded-full bg-gray-200 border border-gray-300 flex items-center justify-center text-xs text-gray-500"
        >
            <UserIcon class="w-3 h-3" />
        </div>

        <!-- 插入你的 Popover component 在最右邊 -->
        <Popover />
        </div>
    </div>

    <!-- Description -->
    <div class="px-4 pb-4 text-sm text-gray-600">
      {{ description }}
    </div>
  </div>
</template>

<script setup>
import Popover from './Popover.vue'
import { EllipsisHorizontalIcon } from '@heroicons/vue/20/solid'


defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  }
})

</script>
