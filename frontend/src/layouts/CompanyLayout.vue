<template>
  <div class="flex min-h-screen bg-gray-100">
    <!-- Sidebar -->
    <aside class="w-64 bg-gray-900 fixed h-full z-30">
      <div class="p-6 border-b border-gray-800">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 bg-gradient-to-br from-emerald-400 to-cyan-500 rounded-xl flex items-center justify-center">
            <i class="fas fa-building text-white"></i>
          </div>
          <div>
            <h1 class="font-bold text-white">企业招聘管理</h1>
            <p class="text-xs text-gray-400">企业端</p>
          </div>
        </div>
      </div>

      <nav class="p-4 space-y-1">
        <router-link
          to="/company/dashboard"
          class="nav-item"
          :class="{ 'active': $route.path === '/company/dashboard' }"
        >
          <i class="fas fa-chart-line w-5 mr-3"></i>
          <span>工作台</span>
        </router-link>
        <router-link
          to="/company/jobs"
          class="nav-item"
          :class="{ 'active': $route.path === '/company/jobs' }"
        >
          <i class="fas fa-briefcase w-5 mr-3"></i>
          <span>岗位管理</span>
        </router-link>
        <router-link
          to="/company/resumes"
          class="nav-item"
          :class="{ 'active': $route.path === '/company/resumes' }"
        >
          <i class="fas fa-user-tie w-5 mr-3"></i>
          <span>人才库</span>
        </router-link>
        <router-link
          to="/company/talks"
          class="nav-item"
          :class="{ 'active': $route.path === '/company/talks' }"
        >
          <i class="fas fa-chalkboard-teacher w-5 mr-3"></i>
          <span>宣讲会</span>
        </router-link>
        <router-link
          to="/company/analytics"
          class="nav-item"
          :class="{ 'active': $route.path === '/company/analytics' }"
        >
          <i class="fas fa-chart-bar w-5 mr-3"></i>
          <span>数据分析</span>
        </router-link>
        <router-link
          to="/company/settings"
          class="nav-item"
          :class="{ 'active': $route.path === '/company/settings' }"
        >
          <i class="fas fa-cog w-5 mr-3"></i>
          <span>企业设置</span>
        </router-link>
      </nav>

      <div class="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-800">
        <div class="flex items-center space-x-3">
          <img :src="companyProfile.logo || `https://ui-avatars.com/api/?name=${encodeURIComponent(companyProfile.name || '企业')}&background=6366f1&color=fff&size=40`" class="w-10 h-10 rounded-full border-2 border-emerald-500 object-cover">
          <div class="flex-1">
            <p class="font-medium text-white">{{ companyProfile.name || '企业用户' }}</p>
            <p class="text-xs text-gray-400">{{ companyProfile.status === 'approved' ? '已认证' : '待审核' }}</p>
          </div>
          <button @click="handleLogout" class="p-2 text-gray-400 hover:text-red-400 transition-colors">
            <i class="fas fa-sign-out-alt"></i>
          </button>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="ml-64 flex-1">
      <header class="bg-white border-b border-gray-200 px-8 py-4 sticky top-0 z-20">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <h2 class="text-xl font-bold text-gray-900">{{ pageTitle }}</h2>
          </div>
          <div class="flex items-center space-x-4">
            <button class="relative p-2 text-gray-500 hover:text-gray-700">
              <i class="fas fa-bell text-xl"></i>
              <span class="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
            </button>
          </div>
        </div>
      </header>

      <div class="p-8">
        <!-- ✅ keep-alive 缓存组件 -->
        <router-view v-slot="{ Component, route }">
          <keep-alive :include="['Dashboard', 'Jobs', 'Applications', 'Profile']">
            <component :is="Component" :key="route.fullPath" />
          </keep-alive>
        </router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessageBox } from 'element-plus'
import { companyAPI } from '@/api'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const companyProfile = ref({
  name: '',
  logo: localStorage.getItem('company_logo') || '',
  status: ''
})

const pageTitle = computed(() => {
  const titles = {
    'CompanyDashboard': '工作台',
    'CompanyJobs': '岗位管理',
    'CompanyResumes': '人才库',
    'CompanyTalks': '宣讲会',
    'CompanyAnalytics': '数据分析',
    'CompanySettings': '企业设置'
  }
  return titles[route.name] || '工作台'
})

const fetchCompanyProfile = async () => {
  try {
    const res = await companyAPI.getSettings()
    companyProfile.value = res.data
  } catch (error) {
    console.error('获取企业信息失败:', error)
  }
}

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

onMounted(() => {
  fetchCompanyProfile()
})
</script>
