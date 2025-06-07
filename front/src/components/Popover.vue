<template>
  <div class="relative">
    <Popover v-slot="{ open, close }" class="relative z-20">
      <!-- ⋮ 按鈕 -->
      <PopoverButton
        class="p-2 rounded-full hover:bg-gray-100 transition focus:outline-none focus-visible:ring-2 focus-visible:ring-gray-500"
        aria-label="More options"
      >
        <span class="text-xl text-gray-700">⋮</span>
      </PopoverButton>

      <!-- 下拉選單 -->
      <transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="translate-y-2 opacity-0"
        enter-to-class="translate-y-0 opacity-100"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="translate-y-0 opacity-100"
        leave-to-class="translate-y-2 opacity-0"
      >
        <PopoverPanel
          class="absolute right-0 bottom-12 z-30 mt-2 w-64 transform px-4 sm:px-0"
        >
          <div class="overflow-hidden rounded-lg shadow-lg ring-1 ring-black/5 bg-white">
            <div class="flex flex-col gap-2 p-4">
              <button
                v-for="item in options"
                :key="item.name"
                type="button"
                @click="() => handleClick(item, close)"
                class="flex items-center w-full text-left rounded-lg p-2 transition hover:bg-gray-100 focus:outline-none focus-visible:ring focus-visible:ring-blue-500/50"
              >
                <div class="flex h-10 w-10 items-center justify-center">
                  <component :is="item.icon" class="h-5 w-5 text-blue-500" />
                </div>
                <div class="ml-4 text-left">
                  <p class="text-sm font-medium text-gray-900">
                    {{ item.name }}
                  </p>
                  <p class="text-sm text-gray-500">
                    {{ item.description }}
                  </p>
                </div>
              </button>
            </div>
          </div>
        </PopoverPanel>
      </transition>
    </Popover>
  </div>
</template>

<script setup>
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/vue'


defineProps({
  options: {
    type: Array,
    required: true,
  },
})

function handleClick(item) {
  item.onClick?.()
  close?.()
}
</script>
