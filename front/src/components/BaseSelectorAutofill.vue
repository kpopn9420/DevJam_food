<!-- eslint-disable vue/no-template-shadow -->
<template>
  <Combobox v-model="selected" as="div">
    <p class="block mb-2 leading-6 text-gray-700" :class="headlineVisible ? '' : 'hidden'">{{ headline }}</p>
    <div class="relative mt-2">
      <div class="flex items-center">
        <ComboboxInput
          class="relative w-full cursor-default bg-white p-2 pl-3 ps-4 py-2.5 pr-10 text-left text-gray-900 border focus:outline-none focus:ring-2 focus:ring-blue-500 caret-blue-500 sm:text-sm sm:leading-6"
          :class="sizeClasses[size]"
          :display-value="(item) => item.name"
          :placeholder="placeholder"
          @change="query = $event.target.value"
        />
        <ComboboxButton class="absolute inset-y-0 ml-3 right-0 flex items-center pr-2">
          <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
        </ComboboxButton>
      </div>
      <TransitionRoot
        leave="transition ease-in duration-100"
        leave-from="opacity-100"
        leave-to="opacity-0"
        @after-leave="query = ''"
      >
        <ComboboxOptions
          class="z-10 absolute mt-1 max-h-40 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black/5 focus:outline-none sm:text-sm"
        >
          <div
            v-if="filteredData.length === 0 && query !== ''"
            class="relative cursor-default select-none px-4 py-2 text-gray-700"
          >
            無符合結果
          </div>

          <ComboboxOption
            v-for="item in filteredData"
            :key="item.id"
            v-slot="{ selected, active }"
            :value="item"
          >
            <li
              class="relative cursor-default select-none py-2 pl-3 pr-4 rounded-md m-1"
              :class="{
                'bg-blue-500 text-white': active,
                'text-gray-900': !active,
              }"
            >
              <span
                class="block truncate ml-3"
                :class="{ 'font-semibold': selected, 'font-normal': !selected }"
              >
                {{ item.name }}
              </span>
              <span
                v-if="selected"
                class="absolute inset-y-0 right-0 flex items-center pr-4"
                :class="{ 'text-white': active, 'text-teal-600': !active }"
              >
                <CheckIcon class="h-5 w-5" aria-hidden="true" />
              </span>
            </li>
          </ComboboxOption>
        </ComboboxOptions>
      </TransitionRoot>
    </div>
  </Combobox>
</template>

<script setup>
  import { ref, computed } from 'vue'
  import {
    Combobox,
    ComboboxInput,
    ComboboxButton,
    ComboboxOptions,
    ComboboxOption,
    TransitionRoot,
  } from '@headlessui/vue'
  import { CheckIcon, ChevronUpDownIcon } from '@heroicons/vue/20/solid'

  const props = defineProps({
    headline: {
      type: String,
      default: '標題',
    },
    headlineVisible: {
      type: Boolean,
      default: true,
    },
    placeholder: {
      type: String,
      default: '請輸入或展開清單選擇...',
    },
    options: {
      type: Array,
      required: true,
      default: () => [
        { id: 1, name: 'Jane Doe' },
        { id: 2, name: 'John Doe' },
      ],
    },
    size: {
      type: String,
      default: 'base',
      validator: (value) => ['sm', 'md', 'base', 'lg'].includes(value),
    },
  })

  let selected = ref('')
  let query = ref('')

  const sizeClasses = {
    base: 'rounded-lg',
    lg: 'h-12 rounded-md',
    md: 'h-10 rounded-lg',
    sm: 'h-8 rounded-full',
  }

  const filteredData = computed(() =>
    query.value === ''
      ? props.options
      : props.options.filter((item) =>
          item.name.toLowerCase().replace(/\s+/g, '').includes(query.value.toLowerCase().replace(/\s+/g, ''))
        )
  )
</script>
