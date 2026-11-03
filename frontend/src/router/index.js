import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/student',
    component: () => import('@/layouts/StudentLayout.vue'),
    meta: { requiresAuth: true, role: 'student' },
    children: [
      {
        path: '',
        redirect: '/student/dashboard'
      },
      {
        path: 'dashboard',
        name: 'StudentDashboard',
        component: () => import('@/views/student/Dashboard.vue')
      },
      {
        path: 'jobs',
        name: 'StudentJobs',
        component: () => import('@/views/student/Jobs.vue')
      },
      {
        path: 'jobs/:id',
        name: 'StudentJobDetail',
        component: () => import('@/views/student/JobDetail.vue')
      },
      {
        path: 'resume',
        name: 'StudentResume',
        component: () => import('@/views/student/Resume.vue')
      },
      {
        path: 'applications',
        name: 'StudentApplications',
        component: () => import('@/views/student/Applications.vue')
      },
      {
        path: 'favorites',
        name: 'StudentFavorites',
        component: () => import('@/views/student/Favorites.vue')
      },
      {
        path: 'career-talks',
        name: 'StudentCareerTalks',
        component: () => import('@/views/student/CareerTalks.vue')
      },
      {
        path: 'career-talks/:id',
        name: 'StudentCareerTalkDetail',
        component: () => import('@/views/student/CareerTalkDetail.vue')
      },
      {
        path: 'messages',
        name: 'StudentMessages',
        component: () => import('@/views/student/Messages.vue')
      },
      {
        path: 'settings',
        name: 'StudentSettings',
        component: () => import('@/views/student/Settings.vue')
      }
    ]
  },
  {
    path: '/company',
    component: () => import('@/layouts/CompanyLayout.vue'),
    meta: { requiresAuth: true, role: 'company' },
    children: [
      {
        path: '',
        redirect: '/company/dashboard'
      },
      {
        path: 'dashboard',
        name: 'CompanyDashboard',
        component: () => import('@/views/company/Dashboard.vue')
      },
      {
        path: 'jobs',
        name: 'CompanyJobs',
        component: () => import('@/views/company/Jobs.vue')
      },
      {
        path: 'resumes',
        name: 'CompanyResumes',
        component: () => import('@/views/company/Resumes.vue')
      },
      {
        path: 'talks',
        name: 'CompanyTalks',
        component: () => import('@/views/company/Talks.vue')
      },
      {
        path: 'analytics',
        name: 'CompanyAnalytics',
        component: () => import('@/views/company/Analytics.vue')
      },
      {
        path: 'settings',
        name: 'CompanySettings',
        component: () => import('@/views/company/Settings.vue')
      }
    ]
  },
  {
    path: '/admin',
    component: () => import('@/layouts/AdminLayout.vue'),
    meta: { requiresAuth: true, role: 'admin' },
    children: [
      {
        path: '',
        redirect: '/admin/dashboard'
      },
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import('@/views/admin/Dashboard.vue')
      },
      {
        path: 'students',
        name: 'AdminStudents',
        component: () => import('@/views/admin/Students.vue')
      },
      {
        path: 'companies',
        name: 'AdminCompanies',
        component: () => import('@/views/admin/Companies.vue')
      },
      {
        path: 'jobs',
        name: 'AdminJobs',
        component: () => import('@/views/admin/Jobs.vue')
      },
      {
        path: 'activities',
        name: 'AdminActivities',
        component: () => import('@/views/admin/Activities.vue')
      },
      {
        path: 'statistics',
        name: 'AdminStatistics',
        component: () => import('@/views/admin/Statistics.vue')
      },
      {
        path: 'settings',
        name: 'AdminSettings',
        component: () => import('@/views/admin/Settings.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const token = localStorage.getItem('token')
  const userRole = localStorage.getItem('userRole')

  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.meta.role && to.meta.role !== userRole) {
    next(`/${userRole}/dashboard`)
  } else {
    next()
  }
})

export default router
