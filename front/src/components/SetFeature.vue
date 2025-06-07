<template>
  <div>
    <div class="flex justify-between items-center">
      <p>{{ props.headline1 }}</p>
      <BaseToggle v-model="enabled1" />
    </div>
    <div class="flex justify-between items-center">
      <p>{{ props.headline2 }}</p>
      <BaseToggle v-model="enabled2" />
    </div>
  </div>
</template>

<script setup>
  import { ref, defineProps } from 'vue'
  import BaseToggle from '@/components/BaseToggle.vue'

  const enabled1 = ref(false)
  const enabled2 = ref(false)

  const props = defineProps({
    headline1: {
      type: String,
      required: true,
      default: '標題',
    },
    headline2: {
      type: String,
      required: true,
      default: '標題',
    },
  })
</script>
