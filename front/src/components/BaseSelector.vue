<template>
  <Listbox v-model="selectedOption" as="div">
    <ListboxLabel class="block leading-6 text-gray-700 mb-2" :class="headlineVisible ? '' : 'hidden'">
      {{ headline }}
    </ListboxLabel>
    <div class="relative">
      <ListboxButton
        class="relative w-full cursor-default bg-white p-2 pl-3 py-2.5 pr-10 text-left text-gray-900 border focus:outline-none focus:ring-2 focus:ring-blue-500 sm:text-sm sm:leading-6"
        :class="sizeClasses[size]"
      >
        <span class="flex items-center">
          <span class="ml-1 text-gray-500 block truncate" :class="sizeTextClasses[size]">
            <!-- Use optional chaining to handle null/undefined -->
            {{ selectedOption?.title || 'Select an option' }}
          </span>
        </span>
        <span class="pointer-events-none absolute inset-y-0 right-0 ml-3 flex items-center pr-2">
          <ChevronUpDownIcon class="h-5 w-5 text-gray-500" aria-hidden="true" />
        </span>
      </ListboxButton>

      <transition
        leave-active-class="transition ease-in duration-100"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <ListboxOptions
          class="absolute z-10 mb-1 max-h-56 w-full overflow-auto rounded-md bg-white p-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
        >
          <ListboxOption
            v-for="option in options"
            :key="option.index"
            v-slot="{ active, selected }"
            as="template"
            :value="option"
          >
            <li
              :class="[
                active ? 'bg-blue-500 text-white' : 'text-gray-900',
                'relative cursor-default select-none py-2 pl-3 pr-9 rounded-md m-1',
              ]"
            >
              <div class="flex items-center">
                <span :class="[selected ? 'font-semibold' : 'font-normal', 'ml-3 block truncate']">
                  {{ option.title }}
                </span>
                <span
                  v-if="selected"
                  :class="[
                    active ? 'text-white' : 'text-teal-600',
                    'absolute inset-y-0 right-0 flex items-center pr-4',
                  ]"
                >
                  <CheckIcon class="h-5 w-5" aria-hidden="true" />
                </span>
              </div>
            </li>
          </ListboxOption>
        </ListboxOptions>
      </transition>
    </div>
  </Listbox>
</template>

<script setup>
  import { ref, watch } from 'vue'
  import { Listbox, ListboxButton, ListboxLabel, ListboxOption, ListboxOptions } from '@headlessui/vue'
  import { CheckIcon, ChevronUpDownIcon } from '@heroicons/vue/20/solid'

  const props = defineProps({
    headline: {
      type: String,
      default: '標題', // 預設值
    },
    options: {
      type: Array,
      required: true,
    },
    selection: {
      type: [Number, String], // Allow both Number and String
      required: true,
    },
    headlineVisible: {
      type: Boolean,
      default: true, // 預設顯示標題
    },
    size: {
      type: String,
      default: 'base',
      validator: (value) => ['sm', 'md', 'base', 'lg'].includes(value),
    },
  })

  const sizeClasses = {
    base: 'rounded-lg',
    lg: 'h-12 rounded-md',
    md: 'h-10 rounded-lg',
    sm: 'h-8 rounded-full',
  }

  const sizeTextClasses = {
    base: 'text-md',
    lg: 'text-md',
    md: 'text-sm',
    sm: 'text-xs',
  }

  // Reactive selectedOption with fallback
  const selectedOption = ref(null)

  const findSelectedOption = () => {
    if (typeof props.selection === 'number') {
      return props.options[props.selection] || null
    } else if (typeof props.selection === 'string') {
      return props.options.find((option) => option.id === props.selection) || null
    }
    return null
  }

  // Initialize selectedOption and watch for changes to props.selection
  selectedOption.value = findSelectedOption()

  watch(
    () => props.selection,
    () => {
      selectedOption.value = findSelectedOption()
    },
    { immediate: true } // Ensure it runs on component initialization
  )
</script>
