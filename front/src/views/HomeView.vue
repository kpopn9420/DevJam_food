<template>
  <BaseBanner
    :is-open="notificationData.open.value"
    :type="notificationData.type.value"
    :headline="notificationData.headline.value"
    :content="notificationData.content.value"
    @close="notificationData.open.value = false"
  />
  <PageLayout :headline="headline">
    <ContentBox headline="系統公告">
      <ul class="w-full flex flex-col items-center space-y-1 -mt-1">
        <li
          v-for="notice in systemNotice"
          :key="notice.announcementTime"
          class="w-full flex justify-between p-2 bg-white rounded-md hover:bg-gray-100 transition-all duration-100"
        >
          <div class="flex items-center space-x-2">
            <p class="text-gray-900 font-medium">{{ notice.announcementTitle }}</p>
            <p class="text-gray-700 text-clip">{{ notice.announcementContent }}</p>
          </div>
          <p class="text-gray-500 max-sm:hidden">{{ notice.announcementTime }}</p>
        </li>
      </ul>
    </ContentBox>

    <PageTab
      :modifiable="modifiable"
      :categories="categories"
      :option-button="optionButton"
      :right-button="rightButton"
    ></PageTab>

    <PageDialog :is-open="newCourse" dialog-title="新增課程" @close="newCourseClose()">
      <div class="mb-4">
        <BaseInputPlace v-model="newCourseName" label="課程名稱" placeholder="請輸入新課程名稱..." />
      </div>
      <div class="mb-4">
        <BaseSelectorAutofill
          v-model="selectedTeacher"
          :options="teachers"
          headline="課程教師"
          placeholder="請選擇教師..."
        ></BaseSelectorAutofill>
      </div>
      <div class="mb-4">
        <BaseSelectorAutofill
          v-model="selectedClass"
          :options="classes"
          headline="課程班級"
          placeholder="請選擇班級..."
        ></BaseSelectorAutofill>
      </div>
      <div class="mb-4 flex space-x-2">
        <BaseSelectorAutofill
          v-model="selectedSchoolYear"
          :options="schoolYears"
          class="w-40"
          headline="課程學年"
          placeholder="請選擇學年..."
        ></BaseSelectorAutofill>
        <BaseSelectorAutofill
          v-model="selectedSemester"
          :options="semesters"
          class="w-40"
          headline="課程學期"
          placeholder="請選擇學期..."
        ></BaseSelectorAutofill>
      </div>
      <div class="mb-4 flex space-x-2">
        <BaseSelectorAutofill
          v-model="selectedDay"
          :options="days"
          class="w-40"
          headline="課程日期"
          placeholder="請選擇課程日期..."
        ></BaseSelectorAutofill>
        <BaseSelectorAutofill
          v-model="selectedPeriod"
          :options="periods"
          class="w-40"
          headline="課程節次"
          placeholder="請選擇節次..."
        ></BaseSelectorAutofill>
      </div>
      <div class="mt-4">
        <BaseButtonFilled button-text="新增課程" width="w-full" @click="addCourse" />
      </div>
    </PageDialog>
  </PageLayout>
</template>

<script setup>
  import { ref, computed, onMounted } from 'vue'
  import { useSemester } from '@/composables/useSemester'
  // import { useAuthStore } from '@/stores/authStore'
  import { useResourceStore } from '@/stores/resource'
  import Resource from '@/api/resource'
  import Course from '@/api/course'
  import PageLayout from '@/components/PageLayout.vue'
  import ContentBox from '@/components/ContentBox.vue'
  import PageTab from '@/components/PageTab.vue'
  import PageDialog from '@/components/PageDialog.vue'
  import BaseInputPlace from '@/components/BaseInputPlace.vue'
  import BaseButtonFilled from '@/components/BaseButtonFilled.vue'
  import BaseSelectorAutofill from '@/components/BaseSelectorAutofill.vue'
  import BaseBanner from '@/components/BaseBanner.vue'

  const notificationData = {
    open: ref(false),
    type: ref('info'),
    headline: ref('系統通知'),
    content: ref('這是一則系統通知'),
  }

  // const authStore = useAuthStore()
  const resourceStore = useResourceStore()

  // Username API
  const userName = ref('')
  const headline = ref('嗨！')
  const fetchUserName = async () => {
    try {
      const userID = 1
      const response = await Resource.getUser(userID)
      resourceStore.updateUserInfo(response.data)
      userName.value = resourceStore.userInfo.name || '使用者' // Default to '使用者' if name is missing
      headline.value = '嗨，' + userName.value + '！'
    } catch (error) {
      console.error('Failed to fetch user name:', error)
      // Fallback fake data
      resourceStore.updateUserInfo({
        name: 'Neokent',
        role: 'student',
      })
      headline.value = '嗨，' + resourceStore.userInfo.name + '！'
    }
  }

  const fetchSchoolId = async () => {
    try {
      const userID = 1
      const response = await Resource.getSchoolId(userID)
      resourceStore.updateSchoolId(response.data.schoolId)
      return resourceStore.schoolId
    } catch (error) {
      console.error('Failed to fetch school ID:', error)
      // Fallback fake data
      resourceStore.updateSchoolId('1')
    }
  }

  // Courses API
  const courses = ref([])
  const fetchCourses = async () => {
    try {
      const userID = 1
      const response = await Resource.getUserCourse(userID)
      courses.value = response.data.records
    } catch (error) {
      console.error('Failed to fetch user courses:', error)
      // Fallback fake data
      courses.value = [
        {
          courseId: 12,
          courseTitle: '軟體工程',
          courseName: '一年甲班',
          teacherName: 'Neokent',
          year: '2024',
          semester: 'Fall',
        },
        {
          courseId: 13,
          courseTitle: '程式設計（一）',
          courseName: '一年甲甲班',
          teacherName: 'Neokent',
          year: '2024',
          semester: 'Fall',
        },
        {
          courseId: 14,
          courseTitle: '程式設計（二）',
          courseName: '一年甲甲班',
          teacherName: 'Neokent',
          year: '2023',
          semester: 'Fall',
        },
      ]
    }
  }

  const modifiable = () => {
    resourceStore.userInfo.role === 'teacher'
  }

  const rightButton = {
    visible: modifiable.value,
    text: '新增課程',
    icon: 'IconPlusCircle',
    onClick: () => {
      newCourseOpen()
    },
  }

  // Map courses into ongoing and past categories
  const { semester, academicYear } = useSemester()
  const categories = computed(() => ({
    進行中課程: courses.value.filter(
      (course) => course.semester === semester.value && course.year === academicYear.value
    ),
    過去課程: courses.value.filter(
      (course) => course.semester !== semester.value || course.year !== academicYear.value
    ),
  }))

  // Announcements API
  const systemNotice = ref([])
  const fetchAnnouncement = async () => {
    try {
      const schoolID = '1' // Replace with actual school ID once available
      const response = await Resource.getSchoolAnnouncement(schoolID)
      systemNotice.value = response.data.records.slice(0, 3)
    } catch (error) {
      console.error('Failed to fetch system notices:', error)
      // Fallback fake data
      systemNotice.value = [
        {
          announcementTitle: '正式發行',
          announcementContent: '12/27版本正式上線',
          announcementTime: '2024-12-25 15:49:20',
        },
        {
          announcementTitle: '首映會',
          announcementContent: '12/27 9:00~12:00可到師大參觀',
          announcementTime: '2024-12-25 15:49:20',
        },
        // {
        //   announcementTitle: 'Fix bug',
        //   announcementContent: 'Fix the bug from resource server',
        //   announcementTime: '2024-10-25 23:36:20',
        // },
      ]
    }
  }

  const selectedClass = ref('')
  const selectedTeacher = ref('')
  const selectedSemester = ref('')
  const selectedSchoolYear = ref('')
  const selectedDay = ref('')
  const selectedPeriod = ref('')
  const newCourseName = ref('')

  const teachers = ref([])
  const classes = ref([])
  const days = [
    { name: 'Monday' },
    { name: 'Tuesday' },
    { name: 'Wednesday' },
    { name: 'Thursday' },
    { name: 'Friday' },
  ]
  const periods = [
    { name: '1' },
    { name: '2' },
    { name: '3' },
    { name: '4' },
    { name: '5' },
    { name: '6' },
    { name: '7' },
    { name: '8' },
  ]
  const semesters = [{ name: 'Fall' }, { name: 'Spring' }]
  const schoolYears = [{ name: '2023' }, { name: '2024' }, { name: '2025' }]

  // Add new course dialog
  const newCourse = ref(false)
  const newCourseOpen = () => {
    newCourse.value = true
    fetchTeachers()
    fetchClasses()
  }
  const newCourseClose = () => {
    newCourse.value = false
  }

  const fetchTeachers = async () => {
    try {
      const schoolId = '1'
      const response = await Resource.getTeacherList(schoolId)
      teachers.value = response.data.records
    } catch (error) {
      console.error('Failed to fetch teachers:', error)
      // Fallback fake data
      teachers.value = [{ name: 'Neokent' }, { name: 'Neokent' }, { name: 'Neokent' }]
    }
  }

  const fetchClasses = async () => {
    try {
      const schoolId = '1'
      const response = await Resource.getClassList(schoolId)
      classes.value = response.data.records
    } catch (error) {
      console.error('Failed to fetch classes:', error)
      // Fallback fake data
      classes.value = [{ name: '一年甲班' }, { name: '一年甲甲班' }, { name: '一年甲乙班' }]
    }
  }

  const addCourse = async () => {
    if (
      newCourseName.value &&
      selectedTeacher.value &&
      selectedClass.value &&
      selectedSchoolYear.value &&
      selectedSemester.value &&
      selectedDay.value &&
      selectedPeriod.value
    ) {
      const body = {
        title: newCourseName.value,
        teacher_id: selectedTeacher.value.name,
        class_id: selectedClass.value.name,
        year: selectedSchoolYear.value,
        semester: selectedSemester.value,
        course_time: {
          day: selectedDay.value.name,
          period: selectedPeriod.value.name,
        },
      }

      try {
        await Course.postNewCourse(body)
        selectedTeacher.value = ''
        selectedClass.value = ''
        newCourseClose()
        notificationData.open.value = true
        notificationData.type.value = 'success'
        notificationData.content.value = `課程「${newCourseName.value}」已成功建立`
        notificationData.headline.value = '新增成功'
        newCourseName.value = ''
      } catch (error) {
        console.error('Failed to add course:', error)
        notificationData.open.value = true
        notificationData.type.value = 'error'
        notificationData.content.value = '新增課程失敗，請稍後再試'
        notificationData.headline.value = '新增失敗'
      }
    } else {
      alert('請填寫所有欄位')
    }
  }

  onMounted(() => {
    fetchUserName()
    fetchCourses()
    fetchAnnouncement()
    fetchSchoolId()
  })
</script>
