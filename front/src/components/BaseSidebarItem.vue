<template>
  <li
    class="w-full cursor-pointer rounded-lg transition-all duration-100 ease-in-out transform hover:bg-gray-100 flex items-center"
    :class="[isExpanded ? 'px-3 py-2' : 'py-2', isActive ? 'bg-gray-100 hover:bg-gray-200' : '']"
  >
    <router-link :to="link" class="flex w-full items-center">
      <div
        :class="[
          'flex w-full items-center whitespace-nowrap overflow-ellipsis overflow-hidden',
          isExpanded ? 'justify-start' : 'justify-center',
        ]"
      >
        <component :is="iconComponent" :class="['w-6 h-6 text-black', isExpanded ? ' mr-2' : 'mr-0']" />
        <slot v-if="isExpanded">{{ buttonText }}</slot>
      </div>
    </router-link>
  </li>
  <div class="border-b border-gray-100" />
</template>

<script setup>
  import { computed } from 'vue'
  import { RouterLink, useRoute, useRouter } from 'vue-router'
  import * as Icons from '@iconify-prerendered/vue-jam'
  import { UsersIcon } from '@heroicons/vue/24/outline'
  import { UsersIcon as UsersIconF } from '@heroicons/vue/20/solid'

  const props = defineProps({
    buttonText: {
      type: String,
      default: '按鈕',
    },
    iconName: {
      type: String,
      default: 'Info',
    },
    isExpanded: {
      type: Boolean,
      default: false,
    },
    link: {
      type: [String, Object],
      required: true,
    },
  })

  const route = useRoute()
  const router = useRouter()

  const isActive = computed(() => {
    if (!router || !props.link) return false

    const resolved = router.resolve(props.link)
    const resolvedPath = resolved.href || ''

    // Compare the resolved path with the current route's full path
    return route.fullPath === resolvedPath
  })

  const iconComponent = computed(() => {
    const baseIconName = props.iconName
    const activeIconName = `${props.iconName}F`
    if (props.iconName !== 'IconSettingsAlt' && props.iconName !== 'IconUsers') {
      return isActive.value ? Icons[activeIconName] : Icons[baseIconName]
    } else if (props.iconName === 'IconUsers') {
      return isActive.value ? UsersIconF : UsersIcon
    }
    return Icons[baseIconName]
  })
</script>
