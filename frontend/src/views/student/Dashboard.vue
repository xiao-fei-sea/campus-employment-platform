<template>
  <div class="space-y-6">
    <!-- Welcome Banner -->
    <div class="bg-gradient-to-r from-blue-600 to-blue-700 rounded-2xl p-8 text-white">
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-2xl font-bold mb-2">下午好，{{ userStore.userInfo.student_profile?.name || '同学' }} 👋</h2>
          <p class="text-blue-100">本周新增 <span class="font-bold text-white">{{ dashboardStats.new_jobs_this_week }}</span> 个适合你的岗位</p>
        </div>
        <div class="flex space-x-4">
          <div class="bg-white/10 rounded-xl px-6 py-4 text-center">
            <p class="text-3xl font-bold">{{ dashboardStats.pending_applications }}</p>
            <p class="text-sm text-blue-100">投递中</p>
          </div>
          <div class="bg-white/10 rounded-xl px-6 py-4 text-center">
            <p class="text-3xl font-bold">{{ dashboardStats.interview_invitations }}</p>
            <p class="text-sm text-blue-100">面试邀请</p>
          </div>
          <div class="bg-white/10 rounded-xl px-6 py-4 text-center">
            <p class="text-3xl font-bold">{{ dashboardStats.resume_completion }}%</p>
            <p class="text-sm text-blue-100">简历完整度</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="grid grid-cols-4 gap-4">
      <router-link to="/student/resume" class="bg-white rounded-xl p-5 shadow-sm hover:shadow-md transition-all card-hover">
        <div class="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center mb-4">
          <i class="fas fa-edit text-blue-600 text-xl"></i>
        </div>
        <h3 class="font-medium text-gray-900 mb-1">完善简历</h3>
        <p class="text-sm text-gray-500">提升求职竞争力</p>
      </router-link>
      <router-link to="/student/jobs" class="bg-white rounded-xl p-5 shadow-sm hover:shadow-md transition-all card-hover">
        <div class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center mb-4">
          <i class="fas fa-search text-green-600 text-xl"></i>
        </div>
        <h3 class="font-medium text-gray-900 mb-1">搜索岗位</h3>
        <p class="text-sm text-gray-500">发现更多机会</p>
      </router-link>
      <router-link to="/student/career-talks" class="bg-white rounded-xl p-5 shadow-sm hover:shadow-md transition-all card-hover">
        <div class="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center mb-4">
          <i class="fas fa-calendar-check text-purple-600 text-xl"></i>
        </div>
        <h3 class="font-medium text-gray-900 mb-1">宣讲会报名</h3>
        <p class="text-sm text-gray-500">3场即将开始</p>
      </router-link>
      <router-link to="/student/resume" class="bg-white rounded-xl p-5 shadow-sm hover:shadow-md transition-all card-hover">
        <div class="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center mb-4">
          <i class="fas fa-chart-line text-orange-600 text-xl"></i>
        </div>
        <h3 class="font-medium text-gray-900 mb-1">求职分析</h3>
        <p class="text-sm text-gray-500">了解就业行情</p>
      </router-link>
    </div>

    <div class="grid grid-cols-3 gap-8">
      <!-- Recommended Jobs -->
      <div class="col-span-2">
        <div class="bg-white rounded-xl shadow-sm">
          <div class="p-6 border-b border-gray-100 flex items-center justify-between">
            <h3 class="text-lg font-bold text-gray-900">为你推荐</h3>
            <router-link to="/student/jobs" class="text-blue-600 hover:text-blue-700 text-sm font-medium">查看更多 <i class="fas fa-arrow-right ml-1"></i></router-link>
          </div>
          <div class="divide-y divide-gray-100">
            <div v-for="job in recommendedJobs" :key="job.id" class="p-6 hover:bg-gray-50 transition-colors cursor-pointer">
              <div class="flex items-start justify-between">
                <div class="flex items-start space-x-4">
                  <div v-if="job.logo" class="w-14 h-14 rounded-xl object-cover overflow-hidden">
                    <img :src="job.logo" @error="job.logo = ''" class="w-full h-full object-cover">
                  </div>
                  <div v-else class="w-14 h-14 rounded-xl bg-blue-600 flex items-center justify-center text-white font-bold text-lg">
                    {{ job.company?.charAt(0) || '企' }}
                  </div>
                  <div>
                    <h4 class="font-medium text-gray-900 mb-1">{{ job.title }}</h4>
                    <p class="text-gray-600 text-sm mb-2">{{ job.company }}</p>
                    <div class="flex items-center space-x-3 text-sm text-gray-500">
                      <span><i class="fas fa-map-marker-alt mr-1"></i>{{ job.location }}</span>
                      <span><i class="fas fa-money-bill-wave mr-1"></i>{{ job.salary }}</span>
                    </div>
                  </div>
                </div>
                <div class="flex flex-col items-end space-y-2">
                  <span :class="job.tagClass">{{ job.tag }}</span>
                  <span class="text-gray-400 text-sm">{{ job.posted }}</span>
                </div>
              </div>
              <div class="mt-4 flex flex-wrap gap-2">
                <span v-for="(tag, index) in job.tags" :key="index" class="px-3 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">{{ tag }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Sidebar -->
      <div class="space-y-6">
        <!-- Application Status -->
        <div class="bg-white rounded-xl shadow-sm p-6">
          <h3 class="text-lg font-bold text-gray-900 mb-4">投递进度</h3>
          <div class="space-y-4">
            <router-link to="/student/applications?status=pending" class="flex items-center justify-between p-4 bg-blue-50 rounded-xl cursor-pointer hover:bg-blue-100 transition-colors">
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
                  <i class="fas fa-spinner text-white"></i>
                </div>
                <div>
                  <p class="font-medium text-gray-900">审核中</p>
                  <p class="text-sm text-gray-500">{{ dashboardStats.pending_applications }}个岗位</p>
                </div>
              </div>
              <span class="text-blue-600 font-bold">{{ dashboardStats.pending_applications }}</span>
            </router-link>
            <router-link to="/student/applications?status=passed" class="flex items-center justify-between p-4 bg-orange-50 rounded-xl cursor-pointer hover:bg-orange-100 transition-colors">
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-orange-500 rounded-lg flex items-center justify-center">
                  <i class="fas fa-comments text-white"></i>
                </div>
                <div>
                  <p class="font-medium text-gray-900">面试邀请</p>
                  <p class="text-sm text-gray-500">{{ dashboardStats.interview_invitations }}个岗位</p>
                </div>
              </div>
              <span class="text-orange-500 font-bold">{{ dashboardStats.interview_invitations }}</span>
            </router-link>
            <router-link to="/student/applications?status=offered" class="flex items-center justify-between p-4 bg-green-50 rounded-xl cursor-pointer hover:bg-green-100 transition-colors">
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-green-500 rounded-lg flex items-center justify-center">
                  <i class="fas fa-check text-white"></i>
                </div>
                <div>
                  <p class="font-medium text-gray-900">已录用</p>
                  <p class="text-sm text-gray-500">{{ dashboardStats.offered_applications }}个岗位</p>
                </div>
              </div>
              <span class="text-green-500 font-bold">{{ dashboardStats.offered_applications }}</span>
            </router-link>
          </div>
        </div>

        <!-- Upcoming Career Talks -->
        <div class="bg-white rounded-xl shadow-sm p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-bold text-gray-900">近期宣讲会</h3>
            <router-link to="/student/career-talks" class="text-blue-600 hover:text-blue-700 text-sm font-medium">全部</router-link>
          </div>
          <div class="space-y-4">
            <div v-for="talk in upcomingTalks" :key="talk.id" class="p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors cursor-pointer">
              <div class="flex items-center space-x-3 mb-2">
                <img :src="talk.logo" class="w-10 h-10 rounded-lg object-cover">
                <div class="flex-1 min-w-0">
                  <p class="font-medium text-gray-900 truncate">{{ talk.company }}</p>
                  <p class="text-xs text-gray-500">{{ talk.date }}</p>
                </div>
              </div>
              <p class="text-sm text-blue-600 font-medium">{{ talk.time }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { studentAPI } from '@/api'

const userStore = useUserStore()

const dashboardStats = reactive({
  new_jobs_this_week: 0,
  pending_applications: 0,
  interview_invitations: 0,
  offered_applications: 0,
  resume_completion: 0.0
})

const recommendedJobs = ref([])

const fetchDashboard = async () => {
  try {
    const res = await studentAPI.getDashboard()
    Object.assign(dashboardStats, res.data)
  } catch (error) {
    console.error('获取仪表盘数据失败:', error)
  }
}

const fetchRecommendedJobs = async () => {
  try {
    const res = await studentAPI.getJobs({ page: 1, page_size: 5 })
    const data = res.data?.data || res.data
    recommendedJobs.value = (Array.isArray(data) ? data : []).map(job => ({
      id: job.id,
      title: job.title,
      company: job.company_name,
      logo: job.company_logo || '/placeholder-logo.png',
      salary: job.salary_show || `${(job.salary_min || 0) / 1000}-${(job.salary_max || 0) / 1000}K`,
      location: job.city || job.province || '未知',
      posted: formatDate(job.created_at),
      tag: job.is_top ? '急聘' : '最新',
      tagClass: job.is_top ? 'px-3 py-1 bg-green-100 text-green-700 text-xs rounded-full' : 'px-3 py-1 bg-blue-100 text-blue-700 text-xs rounded-full',
      isFavorite: false,
      tags: []
    }))
  } catch (error) {
    console.error('获取推荐岗位失败:', error)
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return '未知'
  const date = new Date(dateStr)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

onMounted(() => {
  fetchDashboard()
  fetchRecommendedJobs()
  fetchUpcomingTalks()
})

const upcomingTalks = ref([])

const fetchUpcomingTalks = async () => {
  try {
    const res = await studentAPI.getCareerTalks({ page: 1, page_size: 3 })
    const data = res.data?.data || res.data
    upcomingTalks.value = (Array.isArray(data) ? data : []).map(talk => ({
      id: talk.id,
      company: talk.company_name,
      logo: talk.company_logo || '/placeholder-logo.png',
      date: formatTalkDate(talk.start_time),
      time: `${formatTime(talk.start_time)} - ${formatTime(talk.end_time)}`
    }))
  } catch (error) {
    console.error('获取宣讲会失败:', error)
  }
}

const formatTalkDate = (dateStr) => {
  if (!dateStr) return '未知'
  const date = new Date(dateStr)
  const month = date.getMonth() + 1
  const day = date.getDate()
  return `${month}月${day}日`
}

const formatTime = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  return `${hours}:${minutes}`
}
</script>

<style scoped>
.card-hover:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}
</style>
