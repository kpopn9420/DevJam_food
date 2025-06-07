<template>
  <li
    class="bg-white w-full cursor-pointer rounded-lg transition-all duration-200 ease-in-out transform hover:bg-gray-100 flex items-center"
    :class="[isExpanded ? 'px-3 py-2' : 'py-2']"
    @click="openDropdown"
  >
    <div
      :class="[
        'flex w-full items-center whitespace-nowrap overflow-ellipsis overflow-hidden',
        isExpanded ? 'justify-start' : 'justify-center',
      ]"
    >
      <IconInboxes :class="['w-6 h-6 text-black', isExpanded ? 'mr-2' : 'mr-0']" />
      <slot v-if="isExpanded">課程清單</slot>
      <IconChevronDown
        v-if="isExpanded"
        :class="['w-6 h-6 text-black transition-all', dropdownVisible ? 'rotate-180' : '']"
        class="ml-auto"
      />
    </div>
  </li>
  <div class="border-b border-gray-100" />
  <ul v-if="dropdownVisible && isExpanded" class="pl-4 space-y-1 max-h-64 overflow-y-auto">
    <BaseSidebarItem
      icon-name="IconBook"
      button-text="範例課程1"
      link="/course/001"
      :is-expanded="sidebarExpanded"
    />
    <BaseSidebarItem
      icon-name="IconBook"
      button-text="範例課程2"
      link="/course/002"
      :is-expanded="sidebarExpanded"
    />
    <BaseSidebarItem
      icon-name="IconBook"
      button-text="範例課程3"
      link="/course/003"
      :is-expanded="sidebarExpanded"
    />
  </ul>
</template>

<script setup>
  import { defineProps, defineEmits } from 'vue'
  import { IconInboxes, IconChevronDown } from '@iconify-prerendered/vue-jam'
  import BaseSidebarItem from './BaseSidebarItem.vue'

  const props = defineProps({
    toggleDropdown: {
      type: Function,
      required: true,
    },
    isExpanded: {
      type: Boolean,
      required: true,
    },
    dropdownVisible: {
      type: Boolean,
      required: true,
    },
    sidebarExpanded: {
      type: Boolean,
      required: true,
    },
  })

  const emit = defineEmits(['expand'])
  const openDropdown = () => {
    if (!props.isExpanded) {
      emit('expand')
    } else {
      props.toggleDropdown()
    }
  }
</script>
