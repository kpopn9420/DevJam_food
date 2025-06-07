import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

import PageNotFound from '@/views/404View.vue'
import SetPasswordView from '@/views/SetPasswordView.vue'
import LoginPage from '@/views/LoginView.vue'
import RegisterPage from '@/views/RegisterVIew.vue'
import ForgetView from '@/views/ForgetView.vue'
import FaqView from '@/views/FaqView.vue'
import SettingsView from '@/views/SettingsView.vue'
import ResetView from '@/views/ResetView.vue'
import StudentDiscuss from '@/views/DiscussStudent.vue'
import TeacherDiscuss from '@/views/DiscussTeacher.vue'
import CourseView from '@/views/CourseView.vue'
import Homepage from '@/views/HomeView.vue'
import AiChat from '@/views/AiChat.vue'
import ReportView from '@/views/ReportView.vue'
import RollCallStudent from '@/views/RollCallStudent.vue'
import RollcallTeacher from '@/views/RollcallTeacher.vue'
import TOSView from '@/views/TOSView.vue'
import GroupView from '@/views/GroupView.vue'
import Administrator from '@/views/AdministratorPlatform.vue'
import Trade from '@/views/TradingView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Trade',
      component: Trade
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPage,
    },
    {
      path: '/register',
      name: 'Register',
      component: RegisterPage,
    },
    {
      path: '/forget-password',
      name: 'Forget',
      component: ForgetView,
    },
    {
      path: '/reset-password',
      name: 'Reset',
      component: ResetView,
    },
    {
      path: '/set-password',
      name: 'SetPassword',
      component: SetPasswordView,
    },
    {
      path: '/faq',
      name: 'Faq',
      component: FaqView,
    },
    {
      path: '/report',
      name: 'Report',
      component: ReportView,
    },
    {
      path: '/settings',
      name: 'Settings',
      component: SettingsView,
      meta: { requiresAuth: true },
    },
    {
      path: '/tos',
      name: 'Tos',
      component: TOSView,
    },
    {
      path: '/course/:id/discuss',
      name: 'StudentDiscuss',
      component: StudentDiscuss,
      meta: { requiresAuth: true },
    },
    {
      path: '/course/:id/discuss-teacher',
      name: 'TeacherDiscuss',
      component: TeacherDiscuss,
      meta: { requiresAuth: true },
    },
    {
      path: '/chat',
      name: 'AiChat',
      component: AiChat,
      meta: { requiresAuth: true },
    },
    {
      path: '/course/:id',
      name: 'Course',
      props: true,
      component: CourseView,
      meta: { requiresAuth: true },
    },
    {
      path: '/course/:id/roll-call/student',
      name: 'RollCallStudent',
      props: true,
      component: RollCallStudent,
      meta: { requiresAuth: true },
    },
    {
      path: '/course/:id/roll-call/teacher',
      name: 'RollCallTeacher',
      props: true,
      component: RollcallTeacher,
      meta: { requiresAuth: true },
    },
    {
      path: '/course/:id/group',
      name: 'GroupView',
      props: true,
      component: GroupView,
      meta: { requiresAuth: true },
    },
    {
      path: '/administrator',
      name: 'Administrator',
      component: Administrator,
      meta: { requiresAuth: true },
    },
    {
      path: '/:pathMatch(.*)*',
      name: '404',
      component: PageNotFound,
    },
  ],
})

export default router
