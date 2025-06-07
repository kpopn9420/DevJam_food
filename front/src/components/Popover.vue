<template>
  <div class="relative top-16 w-full max-w-sm px-4">
    <Popover v-slot="{ open }" class="relative">
      <!-- 🔸 透明按鈕加 icon -->
      <PopoverButton
        class="p-2 rounded-full hover:bg-gray-100 transition focus:outline-none focus-visible:ring-2 focus-visible:ring-gray-500"
        aria-label="More options"
      >
        <EllipsisHorizontalIcon class="h-5 w-5 text-gray-600 rotate-90" />
      </PopoverButton>

      <!-- 🔹 往上顯示的 dropdown panel -->
      <transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="translate-y-2 opacity-0"
        enter-to-class="translate-y-0 opacity-100"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="translate-y-0 opacity-100"
        leave-to-class="translate-y-2 opacity-0"
      >
        <PopoverPanel
          class="absolute right-0 bottom-12 z-10 mb-2 w-screen max-w-sm transform px-4 sm:px-0"
        >
          <div class="overflow-hidden rounded-lg shadow-lg ring-1 ring-black/5">
            <div
              class="relative grid gap-8 bg-white p-7"
              :class="{ 'lg:grid-cols-2': options.length > 1 }"
            >
              <a
                v-for="item in options"
                :key="item.name"
                :href="item.href"
                class="-m-3 flex items-center rounded-lg p-2 transition duration-150 ease-in-out hover:bg-gray-50 focus:outline-none focus-visible:ring focus-visible:ring-orange-500/50"
              >
                <div class="flex h-10 w-10 shrink-0 items-center justify-center text-white sm:h-12 sm:w-12">
                  <div v-html="item.icon"></div>
                </div>
                <div class="ml-4">
                  <p class="text-sm font-medium text-gray-900">
                    {{ item.name }}
                  </p>
                  <p class="text-sm text-gray-500">
                    {{ item.description }}
                  </p>
                </div>
              </a>
            </div>
            <div class="bg-gray-50 p-4">
              <a
                href="#"
                class="flow-root rounded-md px-2 py-2 transition duration-150 ease-in-out hover:bg-gray-100 focus:outline-none focus-visible:ring focus-visible:ring-orange-500/50"
              >
                <span class="flex items-center">
                  <span class="text-sm font-medium text-gray-900">
                    Documentation
                  </span>
                </span>
                <span class="block text-sm text-gray-500">
                  Start integrating products and tools
                </span>
              </a>
            </div>
          </div>
        </PopoverPanel>
      </transition>
    </Popover>
  </div>
</template>

<script setup>
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/vue'
import { EllipsisHorizontalIcon } from '@heroicons/vue/20/solid'

defineProps({
  options: {
    type: Array,
    required: true,
  },
})
</script>
