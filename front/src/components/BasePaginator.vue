<template>
  <div class="flex items-center justify-center w-full border-gray-200 px-4 py-3 sm:px-6">
    <!-- Mobile pagination controls -->
    <div class="flex justify-center sm:hidden w-full">
      <button
        :disabled="localCurrentPage === 1"
        class="relative inline-flex items-center rounded-lg h-10 border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
        @click="goToPreviousPage"
      >
        Previous
      </button>
      <button
        :disabled="localCurrentPage === totalPages"
        class="relative ml-3 inline-flex items-center rounded-lg h-10 border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
        @click="goToNextPage"
      >
        Next
      </button>
    </div>

    <!-- Desktop pagination controls -->
    <div class="hidden sm:flex sm:items-center sm:justify-center w-full">
      <nav class="isolate inline-flex -space-x-px rounded-md" aria-label="Pagination">
        <!-- Previous Button -->
        <button
          :disabled="localCurrentPage === 1"
          class="relative inline-flex h-10 bg-white items-center rounded-l-lg px-2 py-2 text-gray-900 disabled:text-gray-400 ring-1 ring-inset disabled:hover:bg-white disabled:cursor-not-allowed ring-gray-200 hover:bg-gray-50 focus:z-20 focus:outline-offset-0"
          @click="goToPreviousPage"
        >
          <ChevronLeftIcon class="h-5 w-5" aria-hidden="true" />
          <span class="text-sm">Previous</span>
        </button>

        <!-- Page Numbers -->
        <template v-for="page in totalPages" :key="page">
          <button
            :class="[
              'relative inline-flex items-center h-10 px-4 py-2 text-sm font-semibold ring-1 ring-inset ring-gray-200 focus:z-20 focus:outline-offset-0',
              localCurrentPage === page
                ? 'z-10 bg-blue-500 text-white'
                : 'text-gray-900 bg-white hover:bg-gray-50',
            ]"
            @click="goToPage(page)"
          >
            {{ page }}
          </button>
        </template>

        <!-- Next Button -->
        <button
          :disabled="localCurrentPage === totalPages"
          class="relative inline-flex bg-white items-center rounded-r-lg px-2 py-2 text-gray-900 ring-1 ring-gray-200 ring-inset disabled:cursor-not-allowed disabled:hover:bg-white disabled:text-gray-400 hover:bg-gray-50 focus:z-20 focus:outline-offset-0"
          @click="goToNextPage"
        >
          <span class="text-sm">Next</span>
          <ChevronRightIcon class="h-5 w-5" aria-hidden="true" />
        </button>
      </nav>
    </div>
  </div>
</template>

<script setup>
  import { ref, watch, defineEmits } from 'vue'
  import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/vue/20/solid'

  // Props
  const props = defineProps({
    totalPages: {
      type: Number,
      required: true,
    },
    initialPage: {
      type: Number,
      default: 1,
    },
    currentPage: {
      type: Number,
      default: 1,
    },
  })

  // Methods for pagination
  const localCurrentPage = ref(props.currentPage)

  const goToPreviousPage = () => {
    if (localCurrentPage.value > 1) {
      localCurrentPage.value -= 1
      emitPageChange()
    }
  }

  const goToNextPage = () => {
    if (localCurrentPage.value < props.totalPages) {
      localCurrentPage.value += 1
      emitPageChange()
    }
  }

  const goToPage = (page) => {
    localCurrentPage.value = page
    emitPageChange()
  }

  const emit = defineEmits(['page-changed'])
  // Emit the page change to the parent component
  const emitPageChange = () => {
    console.log(localCurrentPage.value)
    emit('page-changed', localCurrentPage.value)
  }

  // Watch for changes to initialPage prop and update currentPage if needed
  watch(
    () => props.initialPage,
    (newPage) => {
      localCurrentPage.value = newPage
    }
  )
</script>
