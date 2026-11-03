<template>
  <div class="flex min-h-screen bg-gray-100">
    <aside class="w-64 bg-white border-r border-gray-200 fixed h-full z-30">
      <div class="p-6 border-b border-gray-200">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center">
            <i class="fas fa-graduation-cap text-white"></i>
          </div>
          <div>
            <h1 class="font-bold text-gray-900">高校就业平台</h1>
            <p class="text-xs text-gray-500">学生端</p>
          </div>
        </div>
      </div>

      <nav class="p-4 space-y-1">
        <router-link to="/student/dashboard" class="nav-item" :class="{ 'active': $route.path === '/student/dashboard' }">
          <i class="fas fa-home w-5 mr-3"></i>
          <span>首页</span>
        </router-link>
        <router-link to="/student/jobs" class="nav-item" :class="{ 'active': $route.path.startsWith('/student/jobs') }">
          <i class="fas fa-briefcase w-5 mr-3"></i>
          <span>岗位搜索</span>
        </router-link>
        <router-link to="/student/resume" class="nav-item" :class="{ 'active': $route.path === '/student/resume' }">
          <i class="fas fa-file-alt w-5 mr-3"></i>
          <span>我的简历</span>
        </router-link>
        <router-link to="/student/applications" class="nav-item" :class="{ 'active': $route.path === '/student/applications' }">
          <i class="fas fa-paper-plane w-5 mr-3"></i>
          <span>我的投递</span>
        </router-link>
        <router-link to="/student/career-talks" class="nav-item" :class="{ 'active': $route.path === '/student/career-talks' }">
          <i class="fas fa-chalkboard-teacher w-5 mr-3"></i>
          <span>宣讲会</span>
        </router-link>
        <router-link to="/student/favorites" class="nav-item" :class="{ 'active': $route.path === '/student/favorites' }">
          <i class="fas fa-star w-5 mr-3"></i>
          <span>我的收藏</span>
        </router-link>
        <router-link to="/student/messages" class="nav-item" :class="{ 'active': $route.path === '/student/messages' }">
          <i class="fas fa-comments w-5 mr-3"></i>
          <span>消息中心</span>
          <span class="ml-auto bg-red-500 text-white text-xs px-2 py-0.5 rounded-full">3</span>
        </router-link>
        <router-link to="/student/settings" class="nav-item" :class="{ 'active': $route.path === '/student/settings' }">
          <i class="fas fa-cog w-5 mr-3"></i>
          <span>账号设置</span>
        </router-link>
      </nav>

      <div class="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 rounded-full border-2 border-blue-500 bg-blue-600 flex items-center justify-center text-white font-bold text-lg overflow-hidden">
            <img v-if="userStore.userInfo?.student_profile?.avatar" :src="userStore.userInfo.student_profile.avatar" class="w-full h-full object-cover">
            <span v-else>{{ userStore.userInfo?.student_profile?.name?.charAt(0) || '学' }}</span>
          </div>
          <div class="flex-1">
            <p class="font-medium text-gray-900">{{ userStore.userInfo?.student_profile?.name || '学生' }}</p>
            <p class="text-xs text-gray-500">{{ userStore.userInfo?.student_profile?.major }}</p>
          </div>
          <button @click="handleLogout" class="p-2 text-gray-400 hover:text-red-500 transition-colors">
            <i class="fas fa-sign-out-alt"></i>
          </button>
        </div>
      </div>
    </aside>

    <main class="ml-64 flex-1">
      <header class="bg-white border-b border-gray-200 px-8 py-4 sticky top-0 z-20">
        <div class="flex items-center justify-between">
          <div></div>
          <div class="flex items-center space-x-4">
            <button class="relative p-2 text-gray-500 hover:text-gray-700">
              <i class="fas fa-bell text-xl"></i>
              <span class="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
            </button>
            <div class="flex items-center space-x-3 pl-4 border-l border-gray-200">
              <div class="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold text-lg overflow-hidden">
                <img v-if="userStore.userInfo?.student_profile?.avatar" :src="userStore.userInfo.student_profile.avatar" class="w-full h-full object-cover">
                <span v-else>{{ userStore.userInfo?.student_profile?.name?.charAt(0) || '学' }}</span>
              </div>
              <div>
                <p class="font-medium text-gray-900">{{ userStore.userInfo?.student_profile?.name || '学生' }}</p>
                <p class="text-xs text-gray-500">{{ userStore.userInfo?.student_profile?.major }} · {{ userStore.userInfo?.student_profile?.graduation_year }}</p>
              </div>
            </div>
          </div>
        </div>
      </header>
      <div class="p-8">
        <!-- ✅ keep-alive 缓存组件 -->
        <router-view v-slot="{ Component, route }">
          <keep-alive :include="['Dashboard', 'Jobs', 'Resume', 'Applications', 'Favorites', 'Profile']">
            <component :is="Component" :key="route.fullPath" />
          </keep-alive>
        </router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { studentAPI } from '@/api'

const router = useRouter()
const userStore = useUserStore()

const fetchStudentProfile = async () => {
  try {
    const res = await studentAPI.getSettings()
    const profileData = res.data
    userStore.userInfo.student_profile = profileData
    userStore.userInfo.student_profile.name = profileData.name
    userStore.userInfo.student_profile.avatar = profileData.avatar
    userStore.userInfo.student_profile.major = profileData.major
    userStore.userInfo.student_profile.graduation_year = profileData.graduation_year
    localStorage.setItem('userInfo', JSON.stringify(userStore.userInfo))
  } catch (error) {
    console.error('获取学生信息失败', error)
  }
}

onMounted(() => {
  if (userStore.userInfo?.student_profile?.name) {
    return
  }
  fetchStudentProfile()
})

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    userStore.logout()
    router.push('/login')
  } catch {}
}
</script>

<style scoped>
</style>