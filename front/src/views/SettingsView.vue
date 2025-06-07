<template>
  <BaseBanner
    :is-open="notificationData.open.value"
    :type="notificationData.type.value"
    :headline="notificationData.headline.value"
    :content="notificationData.content.value"
    @close="notificationData.open.value = false"
  />
  <BasePageLayout headline="設定">
    <div class="w-full">
      <span class="text-gray-700 font-bold leading-none">身份：</span
      ><span class="text-gray-700 font-normal leading-none">{{ userTitle }}</span>
    </div>
    <div class="grid sm:flex sm:grid-cols-[auto, auto]">
      <div class="flex-col">
        <PageMenu class="mb-4">
          <PageMenuItem headline="一般" :is-active="isGeneral" :is-clicked="setGeneral" />
          <PageMenuItem
            v-if="userGroup === 'admin'"
            headline="匯入資料"
            :is-active="!isGeneral"
            :is-clicked="setImport"
          />
        </PageMenu>
      </div>

      <!-- Content Section -->
      <div class="sm:flex sm:flex-col sm:flex-grow space-y-4 sm:mr-4 mb-4 flex-wrap">
        <template v-if="isGeneral">
          <ContentBox
            class="sm:ml-4 sm:flex-grow focus-within:shadow-md hover:shadow-md transition-all duration-200"
            headline="更換頭像"
          >
            <div class="justify-start align-middle items-center gap-6 flex">
              <!--Profile Picture-->
              <img :src="profileImage" alt="Profile Picture" class="w-24 h-24 object-cover rounded-full" />
              <div class="flex-col text-center items-center gap-1">
                <BaseButtonOutlined
                  button-text="選擇檔案"
                  border-color="border-blue-500 hover:border-blue-700"
                  hover-background-color="bg-blue-100 hover:bg-blue-300"
                  text-color="text-blue-500 hover:text-blue-700"
                  link=""
                  @click="openFile('profile')"
                />
                <BaseLink link="" text="移除照片" @click="deleteFile('profile')" />
              </div>
            </div>
            <div class="border-l max-md:hidden border-gray-100 w-px h-full"></div>
            <div
              class="max-md:hidden grow shrink basis-0 pr-12 flex-col justify-center items-start gap-2 inline-flex"
            >
              <div class="text-gray-700 text-lg font-normal leading-[25.20px]">檔案要求</div>
              <div class="text-gray-700 text-sm font-normal leading-tight">1. 待定</div>
            </div>
          </ContentBox>

          <ContentBox
            class="sm:ml-4 sm:flex-grow justify-start flex-col w-full focus-within:shadow-md hover:shadow-md transition-all duration-200"
            headline="系統外觀"
          >
            <div class="flex flex-col items-center w-full space-y-4">
              <BaseSelector
                v-model="systemTheme"
                headline="系統主題"
                :options="theme"
                :selection="resourceStore.userSettings.theme"
                class="self-stretch w-full"
              />
              <BaseSelector
                v-model="systemLang"
                headline="系統語言"
                :options="lang"
                :selection="resourceStore.userSettings.language"
                class="self-stretch w-full"
              />
            </div>
          </ContentBox>

          <ContentBox
            class="sm:ml-4 sm:flex-grow flex flex-col w-full focus-within:shadow-md hover:shadow-md transition-all duration-200"
            headline="修改密碼"
          >
            <div class="flex flex-col w-full">
              <PasswordInput
                v-model="oldPassword"
                label="舊密碼"
                placeholder="請輸入舊密碼"
                class="self-stretch w-full"
              ></PasswordInput>
              <PasswordInput
                v-model="newPassword"
                label="新密碼"
                placeholder="請輸入新密碼"
                class="self-stretch w-full"
              ></PasswordInput>
              <PasswordInput
                v-model="confirmPassword"
                label="確認新密碼"
                placeholder="請再次輸入新密碼"
                class="self-stretch w-full"
              ></PasswordInput>
              <BaseButtonFilled
                button-text="修改密碼"
                size="md"
                width="w-fit"
                class="ml-auto"
                @click="changePassword"
              ></BaseButtonFilled>
            </div>
          </ContentBox>
        </template>
        <template v-else>
          <!--Import Data page starts from here-->
          <ContentBox
            class="sm:ml-4 sm:flex-grow hover:shadow-md transition-all duration-200"
            headline="課程資料匯入"
          >
            <div class="pr-12 border-r justify-start items-center gap-6 flex">
              <!--資料-->
              <div class="w-24 h-24 bg-gray-100 rounded-lg justify-center items-center gap-2.5 flex">
                <!--匯入的圖案-->
              </div>
              <div class="flex-col text-center justify-center items-center gap-1">
                <BaseButtonOutlined
                  button-text="上傳 .csv 檔"
                  link=""
                  border-color="border-blue-500 hover:border-blue-700"
                  hover-background-color="bg-blue-100 hover:bg-blue-300"
                  text-color="text-blue-500 hover:text-blue-700"
                  @click="openFile('csv-course')"
                />
                <BaseLink link="" text="移除檔案" @click="deleteFile('csv-course')" />
              </div>
            </div>
            <div class="grow shrink basis-0 pr-12 flex-col justify-center items-start gap-2 inline-flex">
              <div class="text-gray-700 text-lg font-normal leading-[25.20px]">檔案要求</div>
              <div class="text-gray-700 text-sm font-normal leading-tight">1. 待定</div>
            </div>
          </ContentBox>
          <ContentBox
            class="sm:ml-4 sm:flex-grow hover:shadow-md transition-all duration-200"
            headline="教職員資料匯入"
          >
            <div class="pr-12 border-r justify-start items-center gap-6 flex">
              <!-- 資料 -->
              <div class="w-24 h-24 bg-gray-100 rounded-lg justify-center items-center gap-2.5 flex">
                <!--頭像的圖案-->
              </div>
              <div class="flex-col justify-center text-center items-center gap-1">
                <BaseButtonOutlined
                  button-text="上傳 .csv 檔"
                  link=""
                  border-color="border-blue-500 hover:border-blue-700"
                  hover-background-color="bg-blue-100 hover:bg-blue-300"
                  text-color="text-blue-500 hover:text-blue-700"
                  @click="openFile('csv-members')"
                />
                <BaseLink link="" text="移除檔案" @click="deleteFile('csv-members')" />
              </div>
            </div>
            <!-- File Status Section -->
            <div class="grow shrink basis-0 pr-12 flex-col justify-center items-start gap-2 inline-flex">
              <div class="text-gray-700 text-lg font-normal leading-[25.20px]">檔案要求</div>
              <div class="text-gray-700 text-sm font-normal leading-tight">1. 待定</div>
            </div>
          </ContentBox>
          <ContentBox
            class="sm:ml-4 sm:flex-grow flex-col hover:shadow-md transition-all duration-200"
            headline="學校網域名稱"
          >
            <div class="flex-col grid w-full space-y-4">
              <BaseInputPlace v-model="schoolDomain" label="學校電子郵件網域" placeholder="example.edu" />
              <BaseButtonFilled
                button-text="儲存"
                size="md"
                width="w-fit"
                class="ml-auto"
                @click="openDialog"
              />
            </div>
          </ContentBox>
          <ContentBox
            class="sm:ml-4 sm:flex-grow flex-col hover:shadow-md transition-all duration-200"
            headline="新增用戶"
          >
            <!-- Add User Button -->
            <BaseButtonFilled
              button-text="個別新增用戶"
              size="md"
              width="w-fit"
              class="ml-auto"
              @click="newUserOpen"
            />
          </ContentBox>
          <ContentBox
            class="sm:ml-4 sm:flex-grow flex-col hover:shadow-md transition-all duration-200"
            headline="新增課程"
          >
            <!-- Add User Button -->
            <BaseButtonFilled
              button-text="個別新增課程"
              size="md"
              width="w-fit"
              class="ml-auto"
              @click="newCourseOpen"
            />
          </ContentBox>
        </template>
      </div>
    </div>
  </BasePageLayout>

  <!--Dialog for uploading files-->
  <PageDialog dialog-title="上傳檔案" :is-open="isFileOpen" @close="closeFile">
    <div class="mb-4">
      <InputFile @drop.prevent="drop" @change="selectedFile" />
    </div>

    <div v-if="fileData[fileType]?.file" class="text-sm text-gray-600 mt-2">
      <p>檔案名稱：{{ fileData[fileType]?.file?.name }}</p>
      <p>檔案大小：{{ (fileData[fileType]?.file?.size / 1024).toFixed(2) }} KB</p>
    </div>

    <div v-if="fileData[fileType]?.url" class="mt-4">
      <p class="text-sm text-gray-600">檔案預覽：</p>
      <a :href="fileData[fileType]?.url" target="_blank" class="text-blue-500 hover:underline"
        >點此查看檔案</a
      >
    </div>

    <div class="mt-4">
      <BaseButtonFilled button-text="儲存檔案" @click="handleSaveFile" />
    </div>
  </PageDialog>

  <!--Dialog for adding users-->
  <PageDialog class="hidden" dialog-title="新增用戶" :is-open="isUserOpen" @close="newUserClose">
    <div class="mb-4 flex space-x-2">
      <BaseInputPlace v-model="newUser.name" label="姓名" placeholder="請輸入名字"></BaseInputPlace>
    </div>
    <div class="mb-4">
      <BaseInputPlace
        v-model="newUser.idNumber"
        label="學號／教職員編號"
        placeholder="請輸入教職員編號"
      ></BaseInputPlace>
    </div>
    <div class="mb-4">
      <BaseInputPlace
        v-model="newUser.email"
        label="電子郵件地址"
        placeholder="example@example.com"
      ></BaseInputPlace>
    </div>
    <div class="mb-4 flex space-x-2">
      <BaseSelectorAutofill
        v-model="newUser.school"
        headline="學校"
        placeholder="請輸入用戶所屬學校"
        :options="newUserSchools"
      ></BaseSelectorAutofill>
      <BaseSelectorAutofill
        v-model="newUser.class"
        headline="班級"
        placeholder="請輸入班級（學生再輸入）"
        :options="newUserClasses"
      ></BaseSelectorAutofill>
    </div>
    <div class="mb-4">
      <BaseSelectorAutofill
        v-model="newUser.group"
        headline="用戶組"
        placeholder="請輸入用戶組"
        :options="newUserGroups"
      ></BaseSelectorAutofill>
    </div>
    <div class="mt-2">
      <BaseButtonFilled button-text="新增用戶" @click="addUser" />
    </div>
  </PageDialog>
  <!--新增課程對話框-->
  <PageDialog :is-open="isCourseOpen" dialog-title="新增課程" @close="newCourseClose">
    <div class="mb-4">
      <BaseInputPlace
        v-model="newCourse.name"
        label="課程名稱"
        placeholder="請輸入新課程名稱..."
      ></BaseInputPlace>
    </div>
    <div class="mb-4">
      <BaseSelectorAutofill
        v-model="newCourse.teacher"
        :options="newCourseTeachers"
        headline="課程教師"
        placeholder="請選擇教師..."
      ></BaseSelectorAutofill>
    </div>
    <div class="mb-4">
      <BaseSelectorAutofill
        v-model="newCourse.class"
        :options="newCourseClasses"
        headline="課程班級"
        placeholder="請選擇班級..."
      ></BaseSelectorAutofill>
    </div>
    <div class="mb-4 flex space-x-2">
      <BaseSelectorAutofill
        v-model="newCourse.year"
        :options="newCourseYears"
        headline="課程學年"
        placeholder="請選擇課程學年..."
      ></BaseSelectorAutofill>
      <BaseSelectorAutofill
        v-model="newCourse.semester"
        :options="newCourseSemesters"
        headline="課程學期"
        placeholder="請選擇課程學期..."
      ></BaseSelectorAutofill>
    </div>
    <div class="mb-4 flex space-x-2">
      <BaseSelectorAutofill
        v-model="newCourse.course_time.date"
        :options="newCourseDates"
        headline="課程日期"
        placeholder="請選擇課程日期..."
      ></BaseSelectorAutofill>
      <BaseSelectorAutofill
        v-model="newCourse.course_time.period"
        :options="newCoursePeriods"
        headline="課程節次"
        placeholder="請選擇課程節次..."
      ></BaseSelectorAutofill>
    </div>
    <div class="mt-4">
      <BaseButtonFilled button-text="新增課程" width="w-full" @click="addCourse" />
    </div>
  </PageDialog>
</template>

<script setup>
  import { ref, computed, onMounted, watch } from 'vue'
  import Resource from '@/api/resource'
  import Course from '@/api/course'
  import Auth from '@/api/auth'
  import { useFileHandler } from '@/composables/useFileHandler'
  import { useResourceStore } from '@/stores/resource'
  import { hashPassword } from '@/utils/hashUtil'
  import BasePageLayout from '@/components/PageLayout.vue'
  import BaseBanner from '@/components/BaseBanner.vue'
  import PageMenu from '@/components/PageMenu.vue'
  import ContentBox from '@/components/ContentBox.vue'
  import BaseButtonOutlined from '@/components/BaseButtonOutlined.vue'
  import BaseLink from '@/components/BaseLink.vue'
  import BaseButtonFilled from '@/components/BaseButtonFilled.vue'
  import BaseSelectorAutofill from '@/components/BaseSelectorAutofill.vue'
  import BaseSelector from '@/components/BaseSelector.vue'
  import PageMenuItem from '@/components/PageMenuItem.vue'
  import PasswordInput from '@/components/PasswordInput.vue'
  import PageDialog from '@/components/PageDialog.vue'
  import BaseInputPlace from '@/components/BaseInputPlace.vue'
  import InputFile from '@/components/InputFile.vue'
  import { useAuthStore } from '@/stores/authStore'

  // Banner data
  const notificationData = {
    open: ref(false),
    type: ref('error'),
    headline: ref('登入失敗'),
    content: ref('請檢查您的輸入帳號或密碼是否正確。'),
  }

  // Get user's setting preferences
  const resourceStore = useResourceStore()

  const fetchSettings = async () => {
    const userID = '1'
    try {
      const response = await Resource.getUserSetting(userID)
      resourceStore.userSettings.value = response.data
      console.log(response)
    } catch (error) {
      console.error(error)
      console.log(resourceStore.userSettings)
    }
  }

  const profileImage = computed(() => {
    return resourceStore.userSettings?.profileImage || '../assets/profile-placeholder.jpg' // Fallback image
  })

  // General and Import logic
  const isGeneral = ref(true)
  const setGeneral = () => {
    isGeneral.value = true
  }
  const setImport = () => {
    isGeneral.value = false
  }

  // User Group
  const userGroup = ref('student') // TODO: Change it to global state later

  const userTitle = computed(() => {
    return userGroup.value === 'admin' ? '管理員' : '使用者'
  })

  // Settings Selector
  const systemLang = ref(resourceStore.userSettings.language)
  const systemTheme = ref(resourceStore.userSettings.theme)
  const lang = [
    {
      index: 1,
      id: 'zh-tw',
      title: '中文（繁體）',
    },
    {
      index: 2,
      id: 'en-us',
      title: '英文（美式）',
    },
  ]

  const theme = [
    {
      index: 1,
      id: 'auto',
      title: '自動',
    },
    {
      index: 2,
      id: 'light',
      title: '淺色模式',
    },
    {
      index: 3,
      id: 'dark',
      title: '深色模式',
    },
  ]

  watch(systemLang, (newValue) => {
    if (newValue?.id) {
      resourceStore.userSettings.language = newValue.id
      Resource.postUserLangTheme({ language: newValue.id, theme: resourceStore.userSettings.theme })
      console.log(`Language updated to: ${newValue.id}`)
    }
  })

  watch(systemTheme, (newValue) => {
    if (newValue?.id) {
      resourceStore.userSettings.theme = newValue.id
      Resource.postUserLangTheme({ language: resourceStore.userSettings.language, theme: newValue.id })
      console.log(`Theme updated to: ${newValue.id}`)
    }
  })

  const isDialog = ref(false)
  const openDialog = (profile) => {
    isDialog.value = true
    fileType.value = profile
  }

  const notificationHandler = (notification) => {
    notificationData.open.value = true
    notificationData.type.value = notification.type
    notificationData.headline.value = notification.headline
    notificationData.content.value = notification.content
  }

  const {
    fileData,
    fileType,
    isFileOpen,
    initializeFileData,
    openFile,
    closeFile,
    drop,
    selectedFile,
    deleteFile,
    saveFile,
  } = useFileHandler(notificationHandler)

  // Initialize file types specific to this component
  initializeFileData(['profile', 'csv-course', 'csv-members'])

  // Define save handlers
  const saveHandlers = {
    profile: async (file) => {
      console.log('Saving profile file:', file)
      await Resource.postUserImage(file)
    },
    'csv-course': async (file) => {
      console.log('Saving course file:', file)
      await Resource.postUploadCourse(file)
    },
    'csv-members': async (file) => {
      console.log('Saving members file:', file)
      await Resource.postUploadUser(file)
    },
  }

  // Example: Save the current file using handlers
  const handleSaveFile = () => {
    saveFile(saveHandlers)
  }

  const oldPassword = ref('')
  const newPassword = ref('')
  const confirmPassword = ref('')

  const changePassword = async () => {
    // Validation
    if (!oldPassword.value) {
      notificationData.open.value = true
      notificationData.headline.value = '錯誤'
      notificationData.content.value = '舊密碼欄位不得為空！'
      notificationData.type.value = 'error'
      return
    }
    if (!newPassword.value) {
      notificationData.open.value = true
      notificationData.headline.value = '錯誤'
      notificationData.content.value = '新密碼欄位不得為空！'
      notificationData.type.value = 'error'
      return
    }
    if (newPassword.value.length < 8) {
      notificationData.open.value = true
      notificationData.headline.value = '錯誤'
      notificationData.content.value = '新密碼欄位不得少於八個字元！'
      notificationData.type.value = 'error'
      return
    }
    if (newPassword.value !== confirmPassword.value) {
      notificationData.open.value = true
      notificationData.headline.value = '錯誤'
      notificationData.content.value = '確認密碼與新密碼不一致！'
      notificationData.type.value = 'error'
      return
    }

    try {
      const payload = {
        originalPassword: await hashPassword(oldPassword.value),
        newPassword: await hashPassword(newPassword.value),
      }

      const response = await Auth.changePassword(payload)

      if (response && response.data.success) {
        useAuthStore().login(response)
        notificationData.open.value = true
        notificationData.headline.value = '更改成功'
        notificationData.content.value = '密碼修改成功！'
        notificationData.type.value = 'success'
        oldPassword.value = ''
        newPassword.value = ''
        confirmPassword.value = ''
      } else {
        alert(response.message || '密碼修改失敗，請再試一次。')
      }
    } catch (error) {
      console.error('Error changing password:', error)
      notificationData.open.value = true
      notificationData.headline.value = '系統錯誤'
      notificationData.content.value = '發生錯誤，請稍後再試'
      notificationData.type.value = 'error'
    }
  }

  // New User Logic
  const newUser = ref({
    name: '',
    idNumber: '',
    email: '',
    school: '',
    group: '',
    class: '',
  })
  const newUserSchools = ref([])
  const newUserClasses = ref([])
  const newUserGroups = [
    { index: 1, name: '管理員' },
    { index: 2, name: '教師' },
    { index: 3, name: '學生' },
  ]

  const isUserOpen = ref(false)
  const newUserOpen = async () => {
    isUserOpen.value = true
    const schoolId = '1' // How the fuck do I write this???
    newUserSchools.value = await Resource.getSchoolList()
    newUserSchools.value = await Resource.getClassList(schoolId)
  }
  const newUserClose = () => {
    isUserOpen.value = false
  }

  const addUser = async () => {
    try {
      const response = await Resource.postNewUser(newUser.value)

      if (response && response.data.success) {
        notificationData.open.value = true
        notificationData.headline.value = '新增成功'
        notificationData.content.value = '新增用戶成功！'
        notificationData.type.value = 'success'
        // Optionally clear the input fields
        newUser.value = ''
      } else {
        alert(response.message || '新增用戶失敗，請再試一次。')
      }
    } catch (error) {
      console.error('Error adding user', error)
      notificationData.open.value = true
      notificationData.headline.value = '系統錯誤'
      notificationData.content.value = '發生錯誤，請稍後再試'
      notificationData.type.value = 'error'
    }
  }

  // New course logic
  const newCourse = ref({
    name: '',
    teacher: '',
    class: '',
    year: '',
    semester: '',
    course_time: {
      date: '',
      period: '',
    },
  })

  const newCourseClasses = ref([])
  const newCourseTeachers = ref([])
  const newCourseSemesters = [{ name: 'Fall' }, { name: 'Spring' }, { name: 'Summer' }]
  const newCourseYears = [{ name: '2021' }, { name: '2022' }, { name: '2023' }, { name: '2024' }]
  const newCourseDates = [
    { name: 'Monday' },
    { name: 'Tuesday' },
    { name: 'Wednesday' },
    { name: 'Thursday' },
    { name: 'Friday' },
  ]
  const newCoursePeriods = [
    { name: '1' },
    { name: '2' },
    { name: '3' },
    { name: '4' },
    { name: '5' },
    { name: '6' },
    { name: '7' },
    { name: '8' },
  ]

  const isCourseOpen = ref(false)
  const newCourseOpen = async () => {
    isCourseOpen.value = true
    const schoolId = '1' // Again, how do I write this?
    newCourseClasses.value = await Resource.getClassList(schoolId)
    newCourseTeachers.value = await Resource.getTeacherList(schoolId)
  }
  const newCourseClose = () => {
    isCourseOpen.value = false
  }

  const addCourse = async () => {
    try {
      const response = await Course.postNewCourse(newCourse.value)

      // Assume the API returns a success message
      if (response && response.success) {
        notificationData.open.value = true
        notificationData.headline.value = '新增成功'
        notificationData.content.value = '新增課程成功！'
        notificationData.type.value = 'success'
        // Optionally clear the input fields
        newCourse.value.name.value = ''
      } else {
        alert(response.message || '新增課程失敗，請再試一次。')
      }
    } catch (error) {
      console.error('Error adding course', error)
      notificationData.open.value = true
      notificationData.headline.value = '系統錯誤'
      notificationData.content.value = '發生錯誤，請稍後再試'
      notificationData.type.value = 'error'
    }
  }

  onMounted(() => {
    fetchSettings()
  })
</script>
