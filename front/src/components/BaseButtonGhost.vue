<template>
  <div
    :class="[
      'items-center inline-flex cursor-pointer transition-all duration-100',
      width,
      bgColor,
      hoverColor,
      sizeClasses[props.size],
    ]"
  >
    <div :class="['flex', size === 'sm' || size === 'md' ? 'px-2' : 'px-4']">
      <div
        :class="[
          'font-medium leading-none tracking-wide items-center flex justify-center',
          size === 'sm' ? 'text-sm' : 'text-base',
          textColor,
        ]"
      >
        <component
          :is="iconComponent"
          v-if="showIcon"
          :class="['w-5 h-5', textColor, buttonText === '' ? 'mr-0' : 'mr-2']"
        />
        {{ props.buttonText }}
      </div>
    </div>
  </div>
</template>

<script setup>
  import { defineProps } from 'vue'
  import * as Icons from '@iconify-prerendered/vue-jam'

  const props = defineProps({
    bgColor: {
      type: String,
      default: 'bg-inherit',
    },
    hoverColor: {
      type: String,
      default: 'hover:bg-gray-100 hover:bg-opacity-50',
    },
    width: {
      type: String,
      default: 'w-full',
    },
    textColor: {
      type: String,
      default: 'text-gray-700',
    },
    buttonText: {
      type: String,
      default: '按鈕',
    },
    size: {
      type: String,
      default: 'lg',
      validator: (value) => ['lg', 'md', 'sm'].includes(value),
    },
    textAlign: {
      type: String,
      default: 'text-center',
    },
    iconName: {
      type: String,
      default: 'IconPlus',
    },
    showIcon: {
      type: Boolean,
      default: true,
    },
  })

  const sizeClasses = {
    lg: 'h-12 px-3 py-4 rounded-md',
    md: 'h-10 px-2 py-3 rounded-md',
    sm: 'h-8 px-2 py-2 rounded-full',
  }

  const iconComponent = Icons[props.iconName]
</script>
