<template>
  <div class="flex min-h-screen bg-gray-100">
    <!-- Sidebar -->
    <aside class="w-64 bg-white border-r border-gray-200 fixed h-full z-30 shadow-sm">
      <div class="p-6 border-b border-gray-200">
        <div class="flex items-center space-x-3">
          <div class="w-12 h-12 bg-gradient-to-br from-emerald-400 to-cyan-500 rounded-xl flex items-center justify-center">
            <i class="fas fa-university text-white text-xl"></i>
          </div>
          <div>
            <h1 class="font-bold text-gray-900 text-xl">就业管理后台</h1>
            <p class="text-sm text-gray-500">学校端</p>
          </div>
        </div>
      </div>

      <nav class="p-4 space-y-1">
        <router-link
          to="/admin/dashboard"
          class="nav-item-light"
          :class="{ 'active-light': $route.path === '/admin/dashboard' }"
        >
          <i class="fas fa-chart-line w-5 mr-3"></i>
          <span>数据大屏</span>
        </router-link>
        <router-link
          to="/admin/students"
          class="nav-item-light"
          :class="{ 'active-light': $route.path === '/admin/students' }"
        >
          <i class="fas fa-user-graduate w-5 mr-3"></i>
          <span>学生管理</span>
        </router-link>
        <router-link
          to="/admin/companies"
          class="nav-item-light"
          :class="{ 'active-light': $route.path === '/admin/companies' }"
        >
          <i class="fas fa-building w-5 mr-3"></i>
          <span>企业管理</span>
        </router-link>
        <router-link
          to="/admin/jobs"
          class="nav-item-light"
          :class="{ 'active-light': $route.path === '/admin/jobs' }"
        >
          <i class="fas fa-briefcase w-5 mr-3"></i>
          <span>岗位审核</span>
        </router-link>
        <router-link
          to="/admin/activities"
          class="nav-item-light"
          :class="{ 'active-light': $route.path === '/admin/activities' }"
        >
          <i class="fas fa-calendar-check w-5 mr-3"></i>
          <span>活动管理</span>
        </router-link>
        <router-link
          to="/admin/statistics"
          class="nav-item-light"
          :class="{ 'active-light': $route.path === '/admin/statistics' }"
        >
          <i class="fas fa-chart-bar w-5 mr-3"></i>
          <span>统计分析</span>
        </router-link>
        <router-link
          to="/admin/settings"
          class="nav-item-light"
          :class="{ 'active-light': $route.path === '/admin/settings' }"
        >
          <i class="fas fa-cog w-5 mr-3"></i>
          <span>系统设置</span>
        </router-link>
      </nav>

      <div class="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200">
        <div class="flex items-center space-x-3">
          <img src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop&crop=face" class="w-10 h-10 rounded-full border-2 border-emerald-500">
          <div class="flex-1">
            <p class="font-medium text-gray-900">{{ userStore.userInfo.name || '管理员' }}</p>
            <p class="text-xs text-gray-500">就业指导中心</p>
          </div>
          <button @click="handleLogout" class="p-2 text-gray-400 hover:text-red-500 transition-colors">
            <i class="fas fa-sign-out-alt"></i>
          </button>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="ml-64 flex-1">
      <header class="bg-white border-b border-gray-200 px-8 py-4 shadow-sm">
        <div class="flex items-center justify-between flex-wrap gap-4">
          <div class="flex items-center space-x-4">
            <h2 class="text-2xl font-bold text-gray-900">{{ pageTitle }}</h2>
            <span v-if="pageConfig.badge" :class="['px-3 py-1 text-sm font-medium rounded-full', pageConfig.badgeClass]">
              {{ typeof pageConfig.badge === 'function' ? pageConfig.badge() : pageConfig.badge }}
            </span>
          </div>
        </div>
      </header>

      <!-- ✅ keep-alive 缓存组件，切走再回来不重新加载 -->
      <div class="pt-6 px-6">
        <router-view v-slot="{ Component, route }">
          <keep-alive :include="['Dashboard', 'Statistics', 'Students', 'Companies', 'Jobs', 'Activities']">
            <component :is="Component" :key="route.fullPath" />
          </keep-alive>
        </router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { adminAPI } from '@/api/index'
import { ElMessageBox } from 'element-plus'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const dashboardStats = ref({
  total_students: 0,
  total_companies: 0,
  pending_jobs: 0,
  pending_activities: 0
})
const pendingJobsCount = ref(0)
const activitiesCount = ref(0)

async function fetchDashboardStats() {
  try {
    const response = await adminAPI.getDashboardStats()
    dashboardStats.value = response.data
    await Promise.all([
      fetchPendingJobsCount(),
      fetchActivitiesCount()
    ])
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

async function fetchPendingJobsCount() {
  try {
    const response = await adminAPI.getJobs({ status: 'pending', page_size: 1 })
    pendingJobsCount.value = response.data.total || 0
  } catch (error) {
    console.error('获取待审核岗位数失败:', error)
  }
}

async function fetchActivitiesCount() {
  try {
    const response = await adminAPI.getActivities({ page_size: 1 })
    activitiesCount.value = response.data.total || 0
  } catch (error) {
    console.error('获取活动数失败:', error)
  }
}

onMounted(() => {
  fetchDashboardStats()
})

const pageConfig = computed(() => {
  const configs = {
    '/admin/dashboard': {
      title: '数据大屏',
      badge: null,
      badgeClass: '',
      searchPlaceholder: '搜索...',
      searchFocusRing: 'focus:ring-2 focus:ring-blue-500'
    },
    '/admin/students': {
      title: '学生管理',
      badge: computed(() => `应届生 ${dashboardStats.value.total_students.toLocaleString()} 人`),
      badgeClass: 'bg-blue-100 text-blue-700',
      searchPlaceholder: '搜索学生姓名、学号...',
      searchFocusRing: 'focus:ring-2 focus:ring-blue-500'
    },
    '/admin/companies': {
      title: '企业管理',
      badge: computed(() => `入驻企业 ${dashboardStats.value.total_companies.toLocaleString()} 家`),
      badgeClass: 'bg-emerald-100 text-emerald-700',
      searchPlaceholder: '搜索企业名称...',
      searchFocusRing: 'focus:ring-2 focus:ring-emerald-500'
    },
    '/admin/jobs': {
      title: '岗位审核',
      badge: computed(() => `待审核 ${pendingJobsCount.value} 个`),
      badgeClass: 'bg-amber-100 text-amber-700',
      searchPlaceholder: '搜索岗位名称...',
      searchFocusRing: 'focus:ring-2 focus:ring-amber-500'
    },
    '/admin/activities': {
      title: '活动管理',
      badge: computed(() => `宣讲会 ${activitiesCount.value} 场`),
      badgeClass: 'bg-purple-100 text-purple-700',
      searchPlaceholder: '搜索活动名称...',
      searchFocusRing: 'focus:ring-2 focus:ring-purple-500'
    },
    '/admin/statistics': {
      title: '统计分析',
      badge: null,
      badgeClass: '',
      searchPlaceholder: '搜索...',
      searchFocusRing: 'focus:ring-2 focus:ring-blue-500'
    },
    '/admin/settings': {
      title: '系统设置',
      badge: null,
      badgeClass: '',
      searchPlaceholder: '搜索...',
      searchFocusRing: 'focus:ring-2 focus:ring-blue-500'
    }
  }
  return configs[route.path] || configs['/admin/dashboard']
})

const pageTitle = computed(() => pageConfig.value.title)

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    userStore.logout()
    router.push('/login')
  } catch {
  }
}
</script>

<style scoped>
.nav-item-light {
  display: flex;
  align-items: center;
  padding: 14px 20px;
  margin: 6px 0;
  border-radius: 10px;
  color: #6b7280;
  font-size: 20px;
  font-weight: 500;
  transition: all 0.2s ease;
  text-decoration: none;
}

.nav-item-light:hover {
  background-color: #f3f4f6;
  color: #059669;
}

.nav-item-light.active-light {
  background-color: #ecfdf5;
  color: #059669;
  font-weight: 600;
}

.nav-item-light i {
  font-size: 22px;
}
</style>