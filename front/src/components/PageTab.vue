<template>
  <div class="w-full sm:px-0">
    <TabGroup :default-index="0">
      <div class="w-full border-b flex justify-between">
        <!-- Left-aligned TabList -->
        <TabList class="flex justify-start space-x-1">
          <Tab
            v-for="category in Object.keys(categories)"
            :key="category"
            v-slot="{ selected }"
            as="template"
          >
            <button
              :class="[
                'py-2.5 px-2.5 text-sm font-medium leading-5 transition-all duration-100 outline-none',
                selected
                  ? 'bg-inherit text-blue-700 border-b-2 border-blue-700'
                  : 'text-gray-500 hover:bg-gray-100 hover:text-gray-700',
              ]"
            >
              {{ category }}
            </button>
          </Tab>
        </TabList>

        <!-- Right-aligned TabList (optional button) -->
        <TabList v-if="modifiable()" class="flex justify-end space-x-1">
          <button
            :class="[
              'py-2.5 px-2.5 text-sm font-medium leading-5 transition-all duration-100 outline-none flex',
              'text-gray-500 hover:bg-gray-100 hover:text-gray-700',
            ]"
            @click="props.rightButton.onClick"
          >
            {{ rightButton.text }}
            <component :is="iconComponent" class="w-5 h-5 ml-2" />
          </button>
        </TabList>
      </div>

      <TabPanels class="mt-2 flex">
        <TabPanel
          v-for="(items, idx) in Object.values(categories)"
          :key="idx"
          :class="[
            'rounded-md bg-inherit w-full',
            'ring-white/60 ring-offset-2 ring-offset-blue-400 focus:outline-none',
          ]"
        >
          <ul
            class="grid grid-cols-1 mb-4 md:grid-cols-3 lg:grid-cols-4 gap-4 w-full transition-all duration-200"
          >
            <li
              v-for="item in items"
              :key="item.courseId"
              class="relative rounded-md bg-white p-3 border hover:shadow-md transition-all duration-200"
            >
              <p v-if="modifiable()" class="text-sm text-gray-500 mb-1">{{ item.courseName }}</p>
              <p v-else class="text-sm text-gray-500 mb-1">{{ item.teacherName }}</p>
              <h3 class="text-lg font-medium leading-5 mb-10">
                {{ item.courseTitle }}
              </h3>

              <BaseButtonFilled
                button-text="進入課程"
                width="w-full"
                class="mt-2"
                @click="() => toCourse(item)"
              ></BaseButtonFilled>
            </li>
          </ul>
        </TabPanel>
      </TabPanels>
    </TabGroup>
  </div>
</template>

<script setup>
  import { useRouter } from 'vue-router'
  import { defineProps, computed } from 'vue'
  import { TabGroup, TabList, Tab, TabPanels, TabPanel } from '@headlessui/vue'
  import * as Icons from '@iconify-prerendered/vue-jam'
  import BaseButtonFilled from './BaseButtonFilled.vue'

  const props = defineProps({
    modifiable: {
      type: Object,
      required: true,
    },
    categories: {
      type: Object,
      default: () => ({
        'Tab 1': [],
        'Tab 2': [],
      }),
    },
    optionButton: {
      type: Object,
      default: () => ({
        visible: false,
        onClick: () => {
          console.log('Option button clicked')
        },
      }),
    },
    options: {
      type: Array,
      default: () => [
        {
          text: 'Option 1',
          onClick: () => {
            console.log('Option 1 clicked')
          },
        },
        {
          text: 'Option 2',
          onClick: () => {
            console.log('Option 2 clicked')
          },
        },
      ],
    },
    rightButton: {
      type: Object,
      default: () => ({
        visible: true,
        text: 'More',
        icon: 'IconPlusCircle',
        onClick: () => {
          console.log('Right button clicked')
        },
      }),
    },
  })

  const router = useRouter()

  const toCourse = (item) => {
    router.push(`/course/${item.courseId}`)
  }

  const iconComponent = computed(() => {
    return Icons[props.rightButton.icon]
  })
</script>
