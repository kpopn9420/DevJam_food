<template>
  <div class="py-4 flex items-center justify-end">
    <Switch
      v-model="enabled"
      :class="enabled ? 'bg-blue-500' : 'bg-gray-500'"
      class="relative inline-flex h-[19px] w-[37px] shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus-visible:ring-2 focus-visible:ring-white/75"
    >
      <span class="sr-only">Use setting</span>
      <span
        aria-hidden="true"
        :class="enabled ? 'translate-x-4' : 'translate-x-0'"
        class="pointer-events-none inline-block h-[17px] w-[17px] transform rounded-full bg-white shadow-lg ring-0 transition duration-200 ease-in-out"
      />
    </Switch>
  </div>
</template>

<script setup>
  import { ref } from 'vue'
  import { Switch } from '@headlessui/vue'

  const enabled = ref(false)
</script>
