<template>
  <div class="p-8">
    <div class="grid grid-cols-4 gap-4 mb-8">
      <div class="bg-white rounded-xl shadow-sm p-5">
        <div class="flex items-center space-x-4">
          <div class="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
            <i class="fas fa-paper-plane text-blue-600"></i>
          </div>
          <div>
            <p class="text-2xl font-bold text-gray-900">{{ stats.total }}</p>
            <p class="text-sm text-gray-500">全部投递</p>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl shadow-sm p-5">
        <div class="flex items-center space-x-4">
          <div class="w-12 h-12 bg-yellow-100 rounded-xl flex items-center justify-center">
            <i class="fas fa-spinner text-yellow-600"></i>
          </div>
          <div>
            <p class="text-2xl font-bold text-gray-900">{{ stats.pending }}</p>
            <p class="text-sm text-gray-500">待审核</p>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl shadow-sm p-5">
        <div class="flex items-center space-x-4">
          <div class="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center">
            <i class="fas fa-comments text-purple-600"></i>
          </div>
          <div>
            <p class="text-2xl font-bold text-gray-900">{{ stats.interview }}</p>
            <p class="text-sm text-gray-500">面试邀请</p>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl shadow-sm p-5">
        <div class="flex items-center space-x-4">
          <div class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
            <i class="fas fa-check-circle text-green-600"></i>
          </div>
          <div>
            <p class="text-2xl font-bold text-gray-900">{{ stats.offer }}</p>
            <p class="text-sm text-gray-500">offer</p>
          </div>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-xl shadow-sm mb-6">
      <div class="flex border-b border-gray-100">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          @click="activeTab = tab.key"
          :class="[
            'px-6 py-4 transition-colors',
            activeTab === tab.key
              ? 'text-blue-600 border-b-2 border-blue-600 font-medium'
              : 'text-gray-600 hover:text-blue-600'
          ]"
        >
          {{ tab.label }} ({{ tab.count }})
        </button>
      </div>
    </div>

    <div class="space-y-4">
      <div
        v-for="app in filteredApplications"
        :key="app.id"
        :class="['bg-white rounded-xl shadow-sm p-6', app.status === 'rejected' ? 'opacity-60' : '']"
      >
        <div class="flex items-start justify-between">
          <div class="flex items-start space-x-4">
            <div v-if="app.logo" class="w-14 h-14 rounded-xl object-cover overflow-hidden">
              <img :src="app.logo" @error="app.logo = ''" class="w-full h-full object-cover">
            </div>
            <div v-else class="w-14 h-14 rounded-xl bg-blue-600 flex items-center justify-center text-white font-bold text-lg">
              {{ app.company?.charAt(0) || '企' }}
            </div>
            <div>
              <div class="flex items-center space-x-2 mb-1">
                <router-link :to="`/student/jobs/${app.jobId}`" class="font-bold text-gray-900 hover:text-blue-600">
                  {{ app.jobTitle }}
                </router-link>
                <span :class="[getStatusTagClass(app.status), 'px-2 py-0.5 text-xs rounded-full']">
                  {{ getStatusTagText(app.status) }}
                </span>
              </div>
              <div class="flex items-center space-x-2 mb-2">
                <p class="text-gray-600 text-sm">{{ app.company }}</p>
                <span class="px-2 py-0.5 bg-green-100 text-green-700 text-xs rounded-full">已投递</span>
              </div>
              <div class="flex items-center space-x-4 text-sm text-gray-500">
                <span><i class="fas fa-map-marker-alt mr-1"></i>{{ app.location }}</span>
                <span><i class="fas fa-money-bill-wave mr-1"></i>{{ app.salary }}</span>
                <span><i class="fas fa-clock mr-1"></i>投递于 {{ app.applyDaysAgo }}</span>
              </div>
            </div>
          </div>
          <div class="flex flex-col items-end space-y-2">
            <span class="text-gray-500 text-sm">{{ getStatusRightLabel(app.status) }}</span>
            <span :class="getStatusRightValueClass(app.status)">{{ getStatusRightValue(app) }}</span>
            <button
              v-if="app.status === 'interview'"
              @click="confirmInterview(app)"
              class="px-4 py-1.5 bg-purple-600 hover:bg-purple-700 text-white text-sm rounded-lg transition-colors"
            >
              确认参加
            </button>
            <button
              v-else-if="app.status === 'offer'"
              class="px-4 py-1.5 bg-green-600 hover:bg-green-700 text-white text-sm rounded-lg transition-colors"
            >
              查看offer
            </button>
            <button
              v-else-if="app.status === 'written'"
              class="px-4 py-1.5 bg-orange-600 hover:bg-orange-700 text-white text-sm rounded-lg transition-colors"
            >
              去笔试
            </button>
            <button
              v-else-if="app.status === 'pending'"
              @click="withdraw(app.id)"
              class="px-4 py-1.5 bg-white border border-gray-200 hover:bg-gray-50 text-gray-600 text-sm rounded-lg transition-colors"
            >
              撤回
            </button>
          </div>
        </div>

        <div v-if="app.interviewInfo || app.examInfo" class="mt-4 pt-4 border-t border-gray-100 flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <span v-if="app.interviewInfo" class="px-3 py-1 bg-blue-50 text-blue-600 text-xs rounded-full">
              {{ app.interviewInfo }}
            </span>
            <span v-if="app.examInfo" class="px-3 py-1 bg-green-50 text-green-600 text-xs rounded-full">
              {{ app.examInfo }}
            </span>
            <span v-if="app.feedback" class="text-sm text-gray-500">{{ app.feedback }}</span>
          </div>
          <div class="flex space-x-2">
            <button class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
              <i class="fas fa-calendar-plus"></i>
            </button>
            <button class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
              <i class="fas fa-times"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="mt-8 flex items-center justify-center space-x-2">
      <button class="px-4 py-2 bg-white text-gray-600 rounded-lg hover:bg-gray-100 transition-colors">
        <i class="fas fa-chevron-left"></i>
      </button>
      <button class="px-4 py-2 bg-blue-600 text-white rounded-lg">1</button>
      <button class="px-4 py-2 bg-white text-gray-600 rounded-lg hover:bg-gray-100 transition-colors">2</button>
      <button class="px-4 py-2 bg-white text-gray-600 rounded-lg hover:bg-gray-100 transition-colors">
        <i class="fas fa-chevron-right"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { studentAPI } from '@/api/index.js'

const activeTab = ref('all')
const applications = ref([])
const loading = ref(false)

const fetchApplications = async () => {
  try {
    loading.value = true
    const statusMap = { pending: 'pending', interview: 'interview', written: 'written', offer: 'offer', rejected: 'rejected' }
    const params = activeTab.value !== 'all' ? { status: statusMap[activeTab.value] || activeTab.value } : {}
    const res = await studentAPI.getApplications(params)
    const apps = Array.isArray(res) ? res : res.data || []
    applications.value = apps.map(app => ({
      id: app.id,
      jobId: app.job_id,
      jobTitle: app.job_title || '未知岗位',
      company: app.company_name || '未知公司',
      logo: app.company_logo || 'https://via.placeholder.com/80',
      location: app.city || app.province || '未知',
      salary: app.salary_show || `${(app.salary_min || 0) / 1000}-${(app.salary_max || 0) / 1000}K`,
      applyTime: app.created_at,
      applyDaysAgo: getDaysAgo(app.created_at),
      status: app.status,
      interviewInfo: app.interview_time ? `面试时间: ${formatDate(app.interview_time)}` : null,
      examInfo: null,
      feedback: app.feedback || null,
      interviewTime: app.interview_time,
      interviewLocation: app.interview_location,
      offerSalary: app.offer_salary
    }))
  } catch (error) {
    ElMessage.error('获取投递记录失败')
  } finally {
    loading.value = false
  }
}

const getDaysAgo = (date) => {
  if (!date) return ''
  const now = new Date()
  const d = new Date(date)
  const diff = Math.floor((now - d) / (1000 * 60 * 60 * 24))
  if (diff === 0) return '今天'
  if (diff === 1) return '1天前'
  return `${diff}天前`
}

const formatDate = (date) => {
  if (!date) return ''
  const d = new Date(date)
  return `${d.getMonth() + 1}月${d.getDate()}日 ${d.getHours()}:${String(d.getMinutes()).padStart(2, '0')}`
}

const tabs = computed(() => [
  { key: 'all', label: '全部', count: applications.value.length },
  { key: 'pending', label: '待审核', count: applications.value.filter(a => a.status === 'pending').length },
  { key: 'interview', label: '面试邀请', count: applications.value.filter(a => a.status === 'interview').length },
  { key: 'written', label: '笔试', count: applications.value.filter(a => a.status === 'written').length },
  { key: 'offer', label: 'offer', count: applications.value.filter(a => a.status === 'offer').length },
  { key: 'rejected', label: '不合适', count: applications.value.filter(a => a.status === 'rejected').length }
])

const stats = computed(() => ({
  total: applications.value.length,
  pending: applications.value.filter(a => a.status === 'pending').length,
  interview: applications.value.filter(a => a.status === 'interview').length,
  offer: applications.value.filter(a => a.status === 'offer').length
}))

const filteredApplications = computed(() => {
  if (activeTab.value === 'all') return applications.value
  return applications.value.filter(app => app.status === activeTab.value)
})

const getStatusTagText = (status) => {
  const map = {
    pending: '待审核',
    interview: '面试邀请',
    written: '笔试',
    offer: '待签约',
    rejected: '不合适'
  }
  return map[status] || status
}

const getStatusTagClass = (status) => {
  const map = {
    pending: 'bg-yellow-100 text-yellow-700',
    interview: 'bg-purple-100 text-purple-700',
    written: 'bg-orange-100 text-orange-700',
    offer: 'bg-green-100 text-green-700',
    rejected: 'bg-gray-100 text-gray-600'
  }
  return map[status] || ''
}

const getStatusRightLabel = (status) => {
  const map = {
    pending: '状态',
    interview: '面试时间',
    written: '截止时间',
    offer: '薪资',
    rejected: '反馈'
  }
  return map[status] || ''
}

const getStatusRightValue = (app) => {
  if (app.status === 'interview') return app.interviewTime ? formatDate(app.interviewTime) : '待定'
  if (app.status === 'written') return '笔试进行中'
  if (app.status === 'offer') return app.offerSalary ? `${app.offerSalary}K` : '待定'
  if (app.status === 'rejected') return app.feedback || '暂无反馈'
  return 'HR筛选中'
}

const getStatusRightValueClass = (status) => {
  const map = {
    pending: 'text-yellow-600 font-medium',
    interview: 'text-purple-600 font-medium',
    written: 'text-orange-600 font-medium',
    offer: 'text-green-600 font-bold',
    rejected: 'text-gray-600 text-sm'
  }
  return map[status] || ''
}

const confirmInterview = (app) => {
  ElMessage.success('已确认参加面试')
}

const withdraw = async (id) => {
  try {
    await ElMessageBox.confirm('确定要撤回该投递吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await studentAPI.withdrawApplication(id)
    await fetchApplications()
    ElMessage.success('已撤回')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('撤回失败')
    }
  }
}

onMounted(() => {
  fetchApplications()
})

watch(activeTab, () => {
  fetchApplications()
})
</script>
