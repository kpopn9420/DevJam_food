<template>
  <TransitionRoot appear :show="isOpen" as="template">
    <Dialog as="div" class="relative z-10" @close="manualCloseModal">
      <div class="fixed inset-0 overflow-y-visible">
        <div class="flex min-h-full w-full items-top justify-center p-4 text-center">
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0 -translate-y-5"
            enter-to="opacity-100 translate-y-0"
            leave="duration-200 ease-in"
            leave-from="opacity-100 translate-y-0"
            leave-to="opacity-0 -translate-y-5"
          >
            <DialogPanel>
              <div
                :class="[
                  'relative isolate flex items-center gap-x-6 overflow-hidden rounded-md border border-opacity-60 px-6 py-2.5 sm:px-3.5 sm:before:flex-1 hover:shadow-md transition-all duration-200',
                  typeBackground[type],
                ]"
              >
                <div
                  class="absolute left-[max(-7rem,calc(50%-52rem))] top-1/2 -z-10 -translate-y-1/2 transform-gpu blur-2xl"
                  aria-hidden="true"
                ></div>
                <div
                  class="absolute left-[max(45rem,calc(50%+8rem))] top-1/2 -z-10 -translate-y-1/2 transform-gpu blur-2xl"
                  aria-hidden="true"
                ></div>
                <div class="flex flex-wrap items-center gap-x-4 gap-y-2">
                  <p :class="['text-sm leading-6', typeHeadline[type]]">
                    <strong class="font-semibold">{{ headline }}</strong
                    ><svg viewBox="0 0 2 2" class="mx-2 inline h-0.5 w-0.5 fill-current" aria-hidden="true">
                      <circle cx="1" cy="1" r="1" /></svg
                    >{{ content }}
                  </p>
                </div>
                <div class="flex flex-1 justify-end">
                  <button
                    type="button"
                    class="-m-3 p-3 focus:outline-none focus:ring-0"
                    @click="manualCloseModal"
                  >
                    <span :class="['sr-only', typeContent[type]]">Dismiss</span>
                    <XMarkIcon :class="['h-5 w-5', typeContent[type]]" aria-hidden="true" />
                  </button>
                </div>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
  import { ref, watch } from 'vue'
  import { Dialog, TransitionRoot, TransitionChild, DialogPanel } from '@headlessui/vue'
  import { XMarkIcon } from '@heroicons/vue/20/solid'

  const props = defineProps({
    headline: {
      type: String,
      default: '系統通知',
    },
    content: {
      type: String,
      default: '這是一則系統通知',
    },
    type: {
      type: String,
      default: 'info',
      validator: (value) => ['info', 'warn', 'error', 'success', 'other'].includes(value),
    },
    isOpen: {
      type: Boolean,
      required: true,
      default: false,
    },
  })

  const typeBackground = {
    info: 'bg-blue-100 border-blue-600',
    warn: 'bg-amber-100 border-amber-600',
    error: 'bg-red-100 border-red-600',
    success: 'bg-green-100 border-green-600',
    other: 'bg-gray-100 border-gray-600',
  }

  const typeHeadline = {
    info: 'text-blue-800',
    warn: 'text-amber-800',
    error: 'text-red-800',
    success: 'text-green-800',
    other: 'text-gray-800',
  }

  const typeContent = {
    info: 'text-blue-900 text-opacity-80',
    warn: 'text-amber-900 text-opacity-80',
    error: 'text-red-900 text-opacity-80',
    success: 'text-green-900 text-opacity-80',
    other: 'text-gray-900 text-opacity-80',
  }

  const emit = defineEmits(['close'])

  const localIsOpen = ref(props.isOpen)

  watch(
    () => props.isOpen,
    (newVal) => {
      localIsOpen.value = newVal

      if (newVal) {
        setTimeout(() => {
          localIsOpen.value = false
          emit('close')
        }, 2000)
      }
    }
  )

  function manualCloseModal() {
    localIsOpen.value = false
    emit('close')
  }
</script>
