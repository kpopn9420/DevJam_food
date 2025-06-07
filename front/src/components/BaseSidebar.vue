<template>
  <div class="flex flex-col h-full">
    <div
      :class="[
        'bg-white text-black border-r transition-all duration-300 ease-in-out flex flex-col h-full overflow-y-auto max-h-full',
        sidebarExpanded ? 'w-56' : 'w-16',
      ]"
    >
      <BaseSidebarToggle :sidebar-expanded="sidebarExpanded" :expand-sidebar="toggleSidebar" />
      <ul class="list-none space-y-1 px-4 flex-grow">
        <slot>
          <BaseSidebarItem icon-name="IconHome" button-text="首頁" link="/" :is-expanded="sidebarExpanded" />
          <BaseSidebarItem
            v-if="authStore.isAuthenticated"
            icon-name="IconMessages"
            button-text="個人AI聊天室"
            link="/chat"
            :is-expanded="sidebarExpanded"
          />
          <BaseSidebarDropdown
            v-if="authStore.isAuthenticated"
            :toggle-dropdown="toggleDropdown"
            :is-expanded="sidebarExpanded"
            :dropdown-visible="dropdownVisible"
            :sidebar-expanded="sidebarExpanded"
            @expand="dropdownExpand"
          />
          <template v-if="isCoursePage">
            <BaseSidebarItem
              v-if="authStore.isAuthenticated"
              icon-name="IconClock"
              button-text="點名系統"
              :link="{ name: 'RollCallStudent', params: { id: courseId } }"
              :is-expanded="sidebarExpanded"
            />
            <BaseSidebarItem
              v-if="authStore.isAuthenticated"
              icon-name="IconUsers"
              button-text="分組系統"
              :link="{ name: 'GroupView', params: { id: courseId } }"
              :is-expanded="sidebarExpanded"
            />
          </template>
        </slot>
      </ul>
      <ul class="list-none space-y-1 px-4">
        <slot>
          <BaseSidebarItem
            v-if="authStore.isAuthenticated"
            icon-name="IconSettingsAlt"
            link="/settings"
            button-text="設定"
            :is-expanded="sidebarExpanded"
          />
          <BaseSidebarItem
            icon-name="IconInfo"
            link="/faq"
            button-text="常見問題"
            :is-expanded="sidebarExpanded"
          />
          <BaseSidebarItem
            icon-name="IconPadlock"
            button-text="隱私權及使用條款"
            link="/tos"
            :is-expanded="sidebarExpanded"
          />
        </slot>
      </ul>
      <div
        :class="[
          'flex items-center',
          sidebarExpanded ? 'justify-between px-8 py-6' : 'justify-center px-4 py-7',
        ]"
      >
        <img src="../assets/profile-placeholder.jpg" :class="['rounded-full transition-all w-8 h-8']" />
        <button
          v-if="sidebarExpanded && authStore.isAuthenticated"
          class="rounded-md p-2 duration-100 ease-in-out transform hover:bg-gray-100"
          @click="logOut"
        >
          <IconLogOut class="w-6 h-6"></IconLogOut>
        </button>
        <router-link
          v-if="sidebarExpanded && !authStore.isAuthenticated"
          to="/login"
          class="rounded-md p-2 duration-100 ease-in-out transform hover:bg-gray-100"
        >
          <IconLogIn class="w-6 h-6"></IconLogIn>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, computed } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { useAuthStore } from '@/stores/authStore'
  import BaseSidebarItem from './BaseSidebarItem.vue'
  import BaseSidebarToggle from './BaseSidebarToggle.vue'
  import BaseSidebarDropdown from './BaseSidebarDropdown.vue'
  import { IconLogIn, IconLogOut } from '@iconify-prerendered/vue-jam'

  const sidebarExpanded = ref(false)
  const dropdownVisible = ref(false)

  const toggleSidebar = () => {
    sidebarExpanded.value = !sidebarExpanded.value
  }

  function toggleDropdown() {
    console.log('Dropdown toggled', dropdownVisible.value)
    dropdownVisible.value = !dropdownVisible.value
  }

  function dropdownExpand() {
    dropdownVisible.value = true
    sidebarExpanded.value = true
  }

  function logOut() {
    const router = useRouter()
    authStore.logout()
    router.push('/login')
  }

  const route = useRoute()
  const authStore = useAuthStore()

  const isCoursePage = computed(() => route.path.startsWith('/course'))
</script>
