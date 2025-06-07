<template>
  <TabGroup>
    <div class="relative rounded-xl p-1 bg-gray-100 items-center mb-4">
      <TabList class="relative flex z-10">
        <!-- Underline element for active tab animation -->
        <span
          class="absolute bottom-0 top-0 -z-10 rounded-lg bg-white transition-all duration-200 shadow"
          :style="{ left: `${underlineLeft}px`, width: `${underlineWidth}px` }"
        ></span>

        <Tab v-for="category in Object.keys(categories)" :key="category" v-slot="{ selected }" as="template">
          <button
            ref="tabRefs"
            :class="[
              'w-full rounded-lg py-2.5 text-sm font-medium leading-5 transition-all duration-200',
              'focus:outline-none',
              selected ? 'text-blue-700' : 'text-gray-500 hover:bg-white/[0.12] hover:text-gray-700',
            ]"
            @click="setActiveTab(category)"
          >
            {{ category }}
          </button>
        </Tab>
      </TabList>
    </div>
    <slot v-if="activeTabIndex === 0" name="tab1" class="space-y-4"></slot>
    <slot v-if="activeTabIndex === 1" name="tab2" class="space-y-4"></slot>
  </TabGroup>
</template>

<script setup>
  import { ref, watch, onMounted, nextTick } from 'vue'
  import { TabGroup, TabList, Tab } from '@headlessui/vue'

  const props = defineProps({
    categories: {
      type: Object,
      default: () => ({
        'Tab 1': [],
        'Tab 2': [],
      }),
    },
  })

  const activeTabIndex = ref(0)
  const underlineWidth = ref(0)
  const underlineLeft = ref(0)
  const tabRefs = ref([])
  const resizeObserver = ref(null)

  const setTabPosition = () => {
    const currentTab = tabRefs.value[activeTabIndex.value]
    if (currentTab) {
      underlineLeft.value = currentTab.offsetLeft
      underlineWidth.value = currentTab.clientWidth
    }
  }

  const setActiveTab = (category) => {
    activeTabIndex.value = Object.keys(props.categories).indexOf(category)
    observeActiveTab()
  }

  const observeActiveTab = () => {
    // Disconnect any previous observer
    if (resizeObserver.value) {
      resizeObserver.value.disconnect()
    }

    const currentTab = tabRefs.value[activeTabIndex.value]
    if (currentTab) {
      resizeObserver.value = new ResizeObserver(() => setTabPosition())
      resizeObserver.value.observe(currentTab)
    }
  }

  // Watch activeTabIndex to adjust underline position
  watch(activeTabIndex, () => {
    nextTick(() => setTabPosition())
  })

  // Set initial underline position on mount
  onMounted(() => {
    nextTick(() => setTabPosition())
  })
</script>
