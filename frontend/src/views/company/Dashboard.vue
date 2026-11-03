<template>
  <div class="space-y-6">
    <div class="grid grid-cols-4 gap-6">
      <div class="bg-white rounded-xl shadow-sm p-6 card-hover transition-all">
        <div class="flex items-center justify-between mb-4">
          <div class="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
            <i class="fas fa-eye text-blue-600 text-xl"></i>
          </div>
          <span class="text-green-500 text-sm font-medium"><i class="fas fa-arrow-up mr-1"></i>{{ stats.job_views_growth }}%</span>
        </div>
        <p class="text-3xl font-bold text-gray-900 mb-1">{{ stats.job_views.toLocaleString() }}</p>
        <p class="text-gray-500 text-sm">岗位浏览量</p>
        <p class="text-gray-400 text-xs mt-2">较上期 {{ stats.job_views_growth >= 0 ? '+' : '' }}{{ stats.job_views_growth }}%</p>
      </div>
      <div class="bg-white rounded-xl shadow-sm p-6 card-hover transition-all">
        <div class="flex items-center justify-between mb-4">
          <div class="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center">
            <i class="fas fa-paper-plane text-purple-600 text-xl"></i>
          </div>
          <span class="text-green-500 text-sm font-medium"><i class="fas fa-arrow-up mr-1"></i>{{ stats.received_resumes_growth }}%</span>
        </div>
        <p class="text-3xl font-bold text-gray-900 mb-1">{{ stats.received_resumes.toLocaleString() }}</p>
        <p class="text-gray-500 text-sm">收到简历</p>
        <p class="text-gray-400 text-xs mt-2">待筛选 {{ stats.pending_resumes }} 份</p>
      </div>
      <div class="bg-white rounded-xl shadow-sm p-6 card-hover transition-all">
        <div class="flex items-center justify-between mb-4">
          <div class="w-12 h-12 bg-emerald-100 rounded-xl flex items-center justify-center">
            <i class="fas fa-check-circle text-emerald-600 text-xl"></i>
          </div>
          <span class="text-green-500 text-sm font-medium"><i class="fas fa-arrow-up mr-1"></i>{{ stats.received_resumes_growth }}%</span>
        </div>
        <p class="text-3xl font-bold text-gray-900 mb-1">{{ stats.interview_invitations }}</p>
        <p class="text-gray-500 text-sm">面试邀请</p>
        <p class="text-gray-400 text-xs mt-2">待确认 {{ stats.pending_interviews }} 个</p>
      </div>
      <div class="bg-white rounded-xl shadow-sm p-6 card-hover transition-all">
        <div class="flex items-center justify-between mb-4">
          <div class="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center">
            <i class="fas fa-handshake text-orange-600 text-xl"></i>
          </div>
          <span class="text-green-500 text-sm font-medium"><i class="fas fa-arrow-up mr-1"></i>{{ stats.received_resumes_growth }}%</span>
        </div>
        <p class="text-3xl font-bold text-gray-900 mb-1">{{ stats.offers_extended }}</p>
        <p class="text-gray-500 text-sm">发放offer</p>
        <p class="text-gray-400 text-xs mt-2">待签约 {{ stats.pending_offers }} 个</p>
      </div>
    </div>

    <div class="grid grid-cols-3 gap-8">
      <div class="col-span-2 space-y-6">
        <div class="bg-white rounded-xl shadow-sm">
          <div class="p-6 border-b border-gray-100 flex items-center justify-between">
            <h3 class="text-lg font-bold text-gray-900">招聘漏斗</h3>
          </div>
          <div class="p-6">
            <div ref="funnelChartRef" class="w-full h-64"></div>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow-sm">
          <div class="p-6 border-b border-gray-100 flex items-center justify-between">
            <h3 class="text-lg font-bold text-gray-900">岗位列表</h3>
            <router-link to="/company/jobs" class="text-purple-600 hover:text-purple-700 text-sm font-medium">查看全部 <i class="fas fa-arrow-right ml-1"></i></router-link>
          </div>
          <div class="divide-y divide-gray-100">
            <div v-for="job in jobList" :key="job.id" class="p-6 hover:bg-gray-50 transition-colors">
              <div class="flex items-center justify-between">
                <div class="flex-1">
                  <div class="flex items-center space-x-3 mb-2">
                    <h4 class="font-medium text-gray-900">{{ job.title }}</h4>
                    <span :class="getJobStatusClass(job.status)">{{ job.status_text }}</span>
                    <span v-if="job.urgent" class="px-2 py-0.5 bg-blue-100 text-blue-700 text-xs rounded-full">急招</span>
                  </div>
                  <div class="flex items-center space-x-4 text-sm text-gray-500">
                    <span><i class="fas fa-map-marker-alt mr-1"></i>{{ job.location || '-' }}</span>
                    <span><i class="fas fa-money-bill-wave mr-1"></i>{{ job.salary || '-' }}</span>
                    <span><i class="fas fa-user-graduate mr-1"></i>{{ job.education || '-' }}</span>
                  </div>
                </div>
                <div class="flex items-center space-x-6">
                  <div class="text-center">
                    <p class="text-xl font-bold text-blue-600">{{ job.views }}</p>
                    <p class="text-xs text-gray-500">浏览</p>
                  </div>
                  <div class="text-center">
                    <p class="text-xl font-bold text-purple-600">{{ job.applications }}</p>
                    <p class="text-xs text-gray-500">投递</p>
                  </div>
                  <div class="text-center">
                    <p class="text-xl font-bold text-emerald-600">{{ job.interviews }}</p>
                    <p class="text-xs text-gray-500">面试</p>
                  </div>
                  <div class="flex space-x-2">
                    <button class="p-2 text-gray-400 hover:text-purple-600 hover:bg-purple-50 rounded-lg transition-colors">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
                      <i class="fas fa-ellipsis-v"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="jobList.length === 0" class="p-6 text-center text-gray-500">
              暂无岗位数据
            </div>
          </div>
        </div>
      </div>

      <div class="space-y-6">
        <div class="bg-white rounded-xl shadow-sm p-6">
          <h3 class="text-lg font-bold text-gray-900 mb-4">待办事项</h3>
          <div class="space-y-3">
            <div v-for="todo in todos" :key="todo.id" @click="handleTodoClick(todo)" class="flex items-center p-3 rounded-xl cursor-pointer hover:bg-gray-50 transition-colors" :class="todo.bgClass">
              <div class="w-10 h-10 rounded-lg flex items-center justify-center mr-3" :class="todo.iconBgClass">
                <i :class="[todo.icon, todo.iconClass]"></i>
              </div>
              <div class="flex-1">
                <p class="font-medium text-gray-900 text-sm">{{ todo.text }}</p>
                <p :class="todo.descClass">{{ todo.desc }}</p>
              </div>
              <i class="fas fa-chevron-right text-gray-400"></i>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow-sm p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-bold text-gray-900">最新投递</h3>
            <router-link to="/company/resumes" class="text-purple-600 hover:text-purple-700 text-sm">查看全部</router-link>
          </div>
          <div class="space-y-4">
            <div v-for="app in recentApplications" :key="app.id" class="flex items-center space-x-3 p-3 hover:bg-gray-50 rounded-xl transition-colors cursor-pointer">
              <img :src="app.avatar || `https://ui-avatars.com/api/?name=${encodeURIComponent(app.name)}&background=6366f1&color=fff&size=40`" :alt="app.name" class="w-10 h-10 rounded-full object-cover">
              <div class="flex-1">
                <p class="font-medium text-gray-900 text-sm">{{ app.name }}</p>
                <p class="text-gray-500 text-xs">{{ app.school }} · {{ app.major }}</p>
              </div>
              <span :class="getStatusClass(app.status)">{{ app.status_text }}</span>
            </div>
            <div v-if="recentApplications.length === 0" class="text-center text-gray-500 py-4">
              暂无投递记录
            </div>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow-sm p-6">
          <h3 class="text-lg font-bold text-gray-900 mb-4">快捷操作</h3>
          <div class="grid grid-cols-2 gap-3">
            <button class="p-4 bg-purple-50 hover:bg-purple-100 rounded-xl text-purple-600 text-center transition-colors">
              <i class="fas fa-plus mb-2"></i>
              <p class="text-sm font-medium">发布岗位</p>
            </button>
            <button class="p-4 bg-emerald-50 hover:bg-emerald-100 rounded-xl text-emerald-600 text-center transition-colors">
              <i class="fas fa-user-plus mb-2"></i>
              <p class="text-sm font-medium">邀请投递</p>
            </button>
            <button class="p-4 bg-blue-50 hover:bg-blue-100 rounded-xl text-blue-600 text-center transition-colors">
              <i class="fas fa-calendar-plus mb-2"></i>
              <p class="text-sm font-medium">宣讲会</p>
            </button>
            <button class="p-4 bg-orange-50 hover:bg-orange-100 rounded-xl text-orange-600 text-center transition-colors">
              <i class="fas fa-file-import mb-2"></i>
              <p class="text-sm font-medium">简历筛选</p>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'
import { companyAPI } from '@/api'

const router = useRouter()
const funnelChartRef = ref(null)
let funnelChart = null

const stats = reactive({
  job_views: 0,
  job_views_growth: 0,
  received_resumes: 0,
  received_resumes_growth: 0,
  pending_resumes: 0,
  interview_invitations: 0,
  pending_interviews: 0,
  offers_extended: 0,
  pending_offers: 0
})

const funnelData = ref([
  { name: '简历投递', value: 0, percent: 100 },
  { name: '简历筛选', value: 0, percent: 0 },
  { name: '笔试', value: 0, percent: 0 },
  { name: '面试', value: 0, percent: 0 },
  { name: '录用', value: 0, percent: 0 }
])

const jobList = ref([])
const recentApplications = ref([])

const todos = ref([
  { id: 1, text: '待筛选简历', desc: '', icon: 'fas fa-file-alt', bgClass: 'bg-red-50 hover:bg-red-100', iconBgClass: 'bg-red-100', iconClass: 'text-red-600', descClass: 'text-red-600 text-xs' },
  { id: 2, text: '待确认面试', desc: '', icon: 'fas fa-calendar-check', bgClass: 'bg-orange-50 hover:bg-orange-100', iconBgClass: 'bg-orange-100', iconClass: 'text-orange-600', descClass: 'text-orange-600 text-xs' },
  { id: 3, text: '宣讲会报名', desc: '0 场宣讲会待审核', icon: 'fas fa-clock', bgClass: 'bg-blue-50 hover:bg-blue-100', iconBgClass: 'bg-blue-100', iconClass: 'text-blue-600', descClass: 'text-blue-600 text-xs' },
  { id: 4, text: '待签约', desc: '', icon: 'fas fa-handshake', bgClass: 'bg-purple-50 hover:bg-purple-100', iconBgClass: 'bg-purple-100', iconClass: 'text-purple-600', descClass: 'text-purple-600 text-xs' }
])

const initFunnelChart = () => {
  if (!funnelChartRef.value) return

  funnelChart = echarts.init(funnelChartRef.value)

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c}人 ({d}%)'
    },
    color: ['#8b5cf6', '#a78bfa', '#c4b5fd', '#ddd6fe', '#ede9fe'],
    series: [
      {
        name: '招聘漏斗',
        type: 'funnel',
        left: '10%',
        top: 20,
        bottom: 20,
        width: '80%',
        min: 0,
        max: 100,
        minSize: '15%',
        maxSize: '100%',
        gap: 4,
        label: {
          show: true,
          position: 'inside',
          formatter: '{b}\n{c}人',
          fontSize: 12,
          color: '#fff'
        },
        labelLine: {
          show: false
        },
        itemStyle: {
          borderColor: '#fff',
          borderWidth: 2
        },
        data: funnelData.value.map(item => ({
          name: item.name,
          value: item.value
        }))
      }
    ]
  }

  funnelChart.setOption(option)
}

const handleResize = () => {
  funnelChart?.resize()
}

const fetchDashboardData = async () => {
  try {
    const res = await companyAPI.getDashboard()
    const data = res.data

    Object.assign(stats, data.stats)

    if (data.funnel && data.funnel.length > 0) {
      funnelData.value = data.funnel
      if (funnelChart) {
        funnelChart.setOption({
          series: [{
            data: funnelData.value.map(item => ({
              name: item.name,
              value: item.value
            }))
          }]
        })
      }
    }

    if (data.jobs) {
      jobList.value = data.jobs
    }

    if (data.todos) {
      todos.value = data.todos.map((todo, index) => {
        const todoMap = [
          { icon: 'fas fa-file-alt', bgClass: 'bg-red-50 hover:bg-red-100', iconBgClass: 'bg-red-100', iconClass: 'text-red-600', descClass: 'text-red-600 text-xs' },
          { icon: 'fas fa-calendar-check', bgClass: 'bg-orange-50 hover:bg-orange-100', iconBgClass: 'bg-orange-100', iconClass: 'text-orange-600', descClass: 'text-orange-600 text-xs' },
          { icon: 'fas fa-clock', bgClass: 'bg-blue-50 hover:bg-blue-100', iconBgClass: 'bg-blue-100', iconClass: 'text-blue-600', descClass: 'text-blue-600 text-xs' },
          { icon: 'fas fa-handshake', bgClass: 'bg-purple-50 hover:bg-purple-100', iconBgClass: 'bg-purple-100', iconClass: 'text-purple-600', descClass: 'text-purple-600 text-xs' }
        ]
        return { ...todo, ...todoMap[index] }
      })
    }

    if (data.recent_applications) {
      recentApplications.value = data.recent_applications
    }
  } catch (error) {
    console.error('获取仪表盘数据失败:', error)
  }
}

const handleTodoClick = (todo) => {
  const routes = {
    1: '/company/resumes',
    2: '/company/resumes',
    3: '/company/talks',
    4: '/company/analytics'
  }
  if (routes[todo.id]) {
    router.push(routes[todo.id])
  }
}

onMounted(() => {
  fetchDashboardData()
  initFunnelChart()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  funnelChart?.dispose()
})

const getStatusClass = (status) => {
  const map = {
    pending: 'px-2 py-0.5 bg-yellow-100 text-yellow-700 text-xs rounded-full',
    viewed: 'px-2 py-0.5 bg-blue-100 text-blue-700 text-xs rounded-full',
    passed: 'px-2 py-0.5 bg-blue-100 text-blue-700 text-xs rounded-full',
    failed: 'px-2 py-0.5 bg-red-100 text-red-700 text-xs rounded-full',
    offered: 'px-2 py-0.5 bg-purple-100 text-purple-700 text-xs rounded-full',
    rejected: 'px-2 py-0.5 bg-red-100 text-red-700 text-xs rounded-full',
    withdrawn: 'px-2 py-0.5 bg-gray-100 text-gray-700 text-xs rounded-full'
  }
  return map[status] || ''
}

const getJobStatusClass = (status) => {
  const map = {
    active: 'px-2 py-0.5 bg-green-100 text-green-700 text-xs rounded-full',
    paused: 'px-2 py-0.5 bg-yellow-100 text-yellow-700 text-xs rounded-full',
    closed: 'px-2 py-0.5 bg-gray-100 text-gray-700 text-xs rounded-full'
  }
  return map[status] || ''
}
</script>