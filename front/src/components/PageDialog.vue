<template>
  <TransitionRoot appear :show="localIsOpen">
    <Dialog as="div" class="relative z-20 h-auto" @close="closeModal">
      <TransitionChild
        enter="duration-300 ease-in-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="duration-200 ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black/25" />
      </TransitionChild>

      <div class="fixed inset-0 overflow-y-visible">
        <div class="flex min-w-full min-h-full items-center justify-center p-4 text-center">
          <TransitionChild
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel
              class="min-w-96 w-auto z-20 min-h-full transform rounded-2xl p-6 bg-white text-left align-middle shadow-xl transition-all"
            >
              <DialogTitle as="h3" class="text-3xl font-bold text-black text-center mb-3">{{
                dialogTitle
              }}</DialogTitle>
              <div class="overflow-visible"><slot :close-modal="closeModal"></slot></div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
  import { ref, watch } from 'vue'
  import { TransitionRoot, TransitionChild, Dialog, DialogPanel, DialogTitle } from '@headlessui/vue'

  const props = defineProps({
    dialogTitle: {
      type: String,
      default: '標題',
    },
    isOpen: {
      type: Boolean,
      required: true,
      default: false,
    },
  })

  const emit = defineEmits(['close'])

  const localIsOpen = ref(props.isOpen)

  watch(
    () => props.isOpen,
    (newVal) => {
      localIsOpen.value = newVal
    }
  )

  function closeModal() {
    localIsOpen.value = false
    emit('close')
  }
</script>
