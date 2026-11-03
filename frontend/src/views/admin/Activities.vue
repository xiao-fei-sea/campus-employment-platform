<template>
  <div class="space-y-6">
    <div class="bg-white rounded-xl shadow-sm p-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <button
            v-for="tab in tabs"
            :key="tab.value"
            :class="[
              'px-6 py-3 transition-colors flex items-center text-sm font-medium border-b-2',
              activeTab === tab.value
                ? 'text-blue-600 border-blue-600'
                : 'text-gray-600 hover:text-blue-600 border-transparent'
            ]"
            @click="activeTab = tab.value"
          >
            <i :class="tab.icon + ' mr-2'"></i>
            {{ tab.label }} ({{ tab.count }})
          </button>
        </div>
        <div class="flex items-center space-x-4">
          <el-select v-model="filterStatus" class="w-36">
            <el-option label="全部状态" value="" />
            <el-option label="待审核" value="pending" />
            <el-option label="报名中" value="approved" />
            <el-option label="已驳回" value="rejected" />
            <el-option label="已取消" value="cancelled" />
            <el-option label="已结束" value="ended" />
          </el-select>
          <el-input v-model="searchKeyword" placeholder="搜索企业名称..." class="w-64" prefix-icon="Search" @input="handleSearch" />
          <el-button type="primary" @click="openCreateDialog">
            <i class="fas fa-plus mr-2"></i>发布活动
          </el-button>
          <el-button @click="showExportMenu = !showExportMenu" class="relative">
            <i class="fas fa-download mr-2"></i>导出
            <div v-if="showExportMenu" class="absolute right-0 top-full mt-2 bg-white rounded-xl shadow-lg border border-gray-200 py-2 z-50 min-w-32">
              <button type="button" class="w-full px-4 py-2 text-left hover:bg-gray-50 text-sm" @click="exportData('xlsx')">导出 Excel</button>
              <button type="button" class="w-full px-4 py-2 text-left hover:bg-gray-50 text-sm" @click="exportData('csv')">导出 CSV</button>
            </div>
          </el-button>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-3 gap-6">
      <div
        v-for="activity in paginatedActivities"
        :key="activity.id"
        class="bg-white rounded-xl shadow-sm overflow-hidden"
      >
        <div class="h-40 relative overflow-hidden" :style="activity.poster ? '' : getGradientStyle(activity)">
          <img v-if="activity.poster" :src="activity.poster" class="w-full h-full object-cover">
          <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent"></div>
          <div v-if="activity.poster" class="absolute bottom-16 left-4 right-4">
            <p class="text-white font-bold text-base drop-shadow-lg">{{ activity.company_name }}</p>
          </div>
          <div v-else class="w-full h-full flex flex-col items-center justify-center text-white">
            <div class="w-16 h-16 rounded-2xl bg-white/30 backdrop-blur flex items-center justify-center mb-2">
              <span class="text-2xl font-bold">{{ getCompanyAbbr(activity.company_name) }}</span>
            </div>
            <p class="text-sm font-medium text-center px-2">{{ activity.company_name }}</p>
          </div>
          <div class="absolute top-4 left-4">
            <span class="px-3 py-1 bg-black/50 backdrop-blur text-white text-xs rounded-full">
              <i :class="getTypeIcon(activity) + ' mr-1'"></i>{{ getTypeText(activity) }}
            </span>
          </div>
          <div class="absolute bottom-4 right-4 bg-white/95 backdrop-blur rounded-lg p-3 text-center shadow-lg">
            <p class="text-2xl font-bold" :class="getAccentColor(activity)">{{ formatDay(activity.start_time) }}</p>
            <p class="text-xs text-gray-600">{{ formatWeekday(activity.start_time) }}</p>
          </div>
        </div>
        <div class="p-6">
          <div class="flex items-center space-x-3 mb-4">
            <div v-if="activity.company_logo" class="w-12 h-12 rounded-xl overflow-hidden">
              <img :src="activity.company_logo" class="w-full h-full object-cover">
            </div>
            <div v-else class="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white font-bold text-sm">
              {{ getCompanyAbbr(activity.company_name) }}
            </div>
            <div>
              <p class="font-bold text-gray-900">{{ activity.title }}</p>
              <p class="text-sm text-gray-500">{{ activity.company_name || '-' }}</p>
            </div>
          </div>
          <div class="grid grid-cols-3 gap-4 mb-4">
            <div class="text-center p-3 rounded-xl" :class="getAttendeesBg(activity)">
              <p class="text-lg font-bold" :class="getAttendeesColor(activity)">{{ activity.current_attendees || 0 }}</p>
              <p class="text-xs text-gray-500">报名人数</p>
            </div>
            <div class="text-center p-3 bg-blue-50 rounded-xl">
              <p class="text-lg font-bold text-blue-600">{{ activity.max_attendees || 0 }}</p>
              <p class="text-xs text-gray-500">场地容量</p>
            </div>
            <div class="text-center p-3 rounded-xl" :class="getRemainderBg(activity)">
              <p class="text-lg font-bold" :class="getRemainderColor(activity)">{{ getRemainder(activity) }}</p>
              <p class="text-xs text-gray-500">剩余名额</p>
            </div>
          </div>
          <div class="space-y-2 text-sm text-gray-600 mb-4">
            <p><i class="fas fa-clock mr-2 text-gray-400"></i>{{ formatTimeRange(activity.start_time, activity.end_time) }}</p>
            <p><i class="fas fa-map-marker-alt mr-2 text-gray-400"></i>{{ activity.location || '-' }}</p>
          </div>
          <div class="flex items-center justify-between pt-4 border-t border-gray-100">
            <span :class="getStatusClass(activity.status)" class="px-3 py-1 text-sm rounded-full">
              {{ getStatusText(activity.status) }}
            </span>
            <div class="flex space-x-2">
              <button class="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors" @click="viewDetail(activity)">
                <i class="fas fa-eye"></i>
              </button>
              <button class="p-2 text-gray-400 hover:text-purple-600 hover:bg-purple-50 rounded-lg transition-colors" @click="editActivity(activity)">
                <i class="fas fa-edit"></i>
              </button>
              <button class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors" @click="deleteActivity(activity)">
                <i class="fas fa-ellipsis-v"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="filteredActivities.length === 0" class="bg-white rounded-xl p-12 text-center">
      <i class="fas fa-calendar-alt text-gray-300 text-5xl mb-4"></i>
      <p class="text-gray-500">暂无活动信息</p>
    </div>

    <div class="px-6 py-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-t border-gray-200 bg-white rounded-b-xl" v-if="totalPages > 1">
      <p class="text-gray-500 text-sm">共 {{ totalActivities }} 条数据</p>
      <div class="flex items-center flex-wrap justify-center gap-1">
        <button type="button" class="px-3 py-2 bg-white text-gray-600 rounded-lg hover:bg-gray-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-sm border border-gray-200" :disabled="currentPage <= 1" @click="currentPage--" title="上一页">
          <i class="fas fa-chevron-left" />
        </button>
        <template v-for="(p, idx) in visiblePages">
          <span v-if="p === '...'" :key="`ellipsis-${idx}`" class="px-2 text-gray-400 text-sm">...</span>
          <button v-else :key="`page-btn-${p}`" type="button" class="px-3 py-2 rounded-lg transition-colors text-sm font-medium" :class="p === currentPage ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-100 border border-gray-200'" @click="currentPage = p">
            {{ p }}
          </button>
        </template>
        <button type="button" class="px-3 py-2 bg-white text-gray-600 rounded-lg hover:bg-gray-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-sm border border-gray-200" :disabled="currentPage >= totalPages" @click="currentPage++" title="下一页">
          <i class="fas fa-chevron-right" />
        </button>
      </div>
    </div>

    <el-dialog v-model="showDetailDialog" title="活动详情" width="600px">
      <div class="space-y-4" v-if="currentActivity.id">
        <div class="flex items-center space-x-4 mb-6">
          <div v-if="currentActivity.company_logo" class="w-16 h-16 rounded-xl overflow-hidden">
            <img :src="currentActivity.company_logo" class="w-full h-full object-cover">
          </div>
          <div v-else class="w-16 h-16 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white font-bold text-lg">
            {{ getCompanyAbbr(currentActivity.company_name) }}
          </div>
          <div>
            <h3 class="text-xl font-bold text-gray-900">{{ currentActivity.title }}</h3>
            <p class="text-gray-500">{{ currentActivity.company_name || '-' }}</p>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <p class="text-sm text-gray-500">活动时间</p>
            <p class="font-medium">{{ formatTime(currentActivity.start_time) }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">活动地点</p>
            <p class="font-medium">{{ currentActivity.location || '-' }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">参与人数</p>
            <p class="font-medium">{{ currentActivity.current_attendees || 0 }} / {{ currentActivity.max_attendees || 0 }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">状态</p>
            <p class="font-medium">{{ getStatusText(currentActivity.status) }}</p>
          </div>
        </div>

        <div v-if="currentActivity.description">
          <p class="text-sm text-gray-500 mb-2">活动描述</p>
          <p class="text-gray-700 whitespace-pre-wrap">{{ currentActivity.description }}</p>
        </div>

        <div v-if="currentActivity.approval_comment">
          <p class="text-sm text-gray-500 mb-2">审核备注</p>
          <p class="text-gray-700">{{ currentActivity.approval_comment }}</p>
        </div>
      </div>
    </el-dialog>

    <el-dialog v-model="showEditDialog" :title="editDialogTitle" width="600px">
      <el-form :model="editForm" label-position="top" class="space-y-4">
        <el-form-item label="活动标题">
          <el-input v-model="editForm.title" placeholder="请输入活动标题" />
        </el-form-item>
        <div class="grid grid-cols-2 gap-4">
          <el-form-item label="开始时间">
            <el-date-picker
              v-model="editForm.start_time"
              type="datetime"
              placeholder="选择开始时间"
              class="w-full"
              format="YYYY-MM-DD HH:mm"
              value-format="YYYY-MM-DDTHH:mm:ss"
            />
          </el-form-item>
          <el-form-item label="结束时间">
            <el-date-picker
              v-model="editForm.end_time"
              type="datetime"
              placeholder="选择结束时间"
              class="w-full"
              format="YYYY-MM-DD HH:mm"
              value-format="YYYY-MM-DDTHH:mm:ss"
            />
          </el-form-item>
        </div>
        <el-form-item label="活动地点">
          <el-input v-model="editForm.location" placeholder="请输入活动地点" />
        </el-form-item>
        <el-form-item label="场地容量">
          <el-input-number v-model="editForm.max_attendees" :min="1" class="w-full" />
        </el-form-item>
        <el-form-item label="活动描述">
          <el-input v-model="editForm.description" type="textarea" :rows="4" placeholder="请输入活动描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" @click="saveActivity" :loading="saving">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showCreateDialog" title="发布活动" width="600px">
      <el-form :model="createForm" label-position="top" class="space-y-4">
        <el-form-item label="所属企业" required>
          <el-select v-model="createForm.company_id" placeholder="请选择企业" filterable class="w-full">
            <el-option
              v-for="company in companies"
              :key="company.id"
              :label="company.name"
              :value="company.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="活动标题" required>
          <el-input v-model="createForm.title" placeholder="请输入活动标题" />
        </el-form-item>
        <el-form-item label="活动类型">
          <el-select v-model="createForm.activity_type" class="w-full">
            <el-option label="宣讲会" value="career_talk" />
            <el-option label="招聘会" value="job_fair" />
          </el-select>
        </el-form-item>
        <el-form-item label="主讲人">
          <el-input v-model="createForm.speaker_name" placeholder="请输入主讲人姓名" />
        </el-form-item>
        <div class="grid grid-cols-2 gap-4">
          <el-form-item label="开始时间" required>
            <el-date-picker
              v-model="createForm.start_time"
              type="datetime"
              placeholder="选择开始时间"
              class="w-full"
              format="YYYY-MM-DD HH:mm"
              value-format="YYYY-MM-DDTHH:mm:ss"
            />
          </el-form-item>
          <el-form-item label="结束时间" required>
            <el-date-picker
              v-model="createForm.end_time"
              type="datetime"
              placeholder="选择结束时间"
              class="w-full"
              format="YYYY-MM-DD HH:mm"
              value-format="YYYY-MM-DDTHH:mm:ss"
            />
          </el-form-item>
        </div>
        <el-form-item label="活动地点" required>
          <el-input v-model="createForm.location" placeholder="请输入活动地点" />
        </el-form-item>
        <el-form-item label="场地容量">
          <el-input-number v-model="createForm.max_attendees" :min="1" class="w-full" />
        </el-form-item>
        <el-form-item label="活动描述">
          <el-input v-model="createForm.description" type="textarea" :rows="4" placeholder="请输入活动描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="submitCreate" :loading="creating">发布</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
defineOptions({ name: 'Activities' })
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { adminAPI } from '@/api/index'
import * as XLSX from 'xlsx'

const showCreateDialog = ref(false)
const creating = ref(false)
const companies = ref([])
const createForm = ref({
  company_id: null,
  title: '',
  activity_type: 'career_talk',
  speaker_name: '',
  start_time: '',
  end_time: '',
  location: '',
  max_attendees: 200,
  description: ''
})

const showDetailDialog = ref(false)
const currentActivity = ref({})

const showEditDialog = ref(false)
const editDialogTitle = ref('编辑活动')
const editForm = ref({
  id: null,
  title: '',
  start_time: '',
  end_time: '',
  location: '',
  max_attendees: 200,
  description: ''
})
const saving = ref(false)

const searchKeyword = ref('')
const filterStatus = ref('')
const activeTab = ref('talk')
const currentPage = ref(1)
const pageSize = ref(10)

const stats = ref({
  careerTalks: 0,
  jobFairs: 0,
  participants: 0,
  companies: 0
})

const activitiesRaw = ref([])
const totalActivities = ref(0)
const loading = ref(false)
const showExportMenu = ref(false)

const gradientColors = [
  'from-blue-500 to-blue-600',
  'from-orange-500 to-orange-600',
  'from-purple-500 to-purple-600',
  'from-emerald-500 to-emerald-600',
  'from-red-500 to-red-600',
  'from-cyan-500 to-cyan-600',
  'from-pink-500 to-pink-600',
  'from-indigo-500 to-indigo-600'
]

async function fetchStats() {
  try {
    const res = await adminAPI.getActivities({ page: 1, page_size: 100 })
    if (res?.data) {
      const data = res.data
      const allActivities = data.activities || []
      stats.value = {
        careerTalks: allActivities.filter(a => a.activity_type === 'career_talk' || !a.activity_type).length,
        jobFairs: allActivities.filter(a => a.activity_type === 'job_fair').length,
        participants: allActivities.reduce((sum, a) => sum + (a.current_attendees || 0), 0),
        companies: new Set(allActivities.map(a => a.company_id)).size
      }
    }
  } catch (error) {
    console.error('Failed to fetch stats:', error)
    ElMessage.error('获取统计数据失败')
  }
}

async function fetchActivities() {
  loading.value = true
  try {
    const params = { page: 1, page_size: 100 }
    if (filterStatus.value && filterStatus.value !== 'all') {
      params.status = filterStatus.value
    }
    if (searchKeyword.value.trim()) {
      params.keyword = searchKeyword.value.trim()
    }
    const res = await adminAPI.getActivities(params)
    if (res?.data) {
      const data = res.data
      activitiesRaw.value = data.activities || []
      totalActivities.value = data.total || activitiesRaw.value.length
    }
  } catch (error) {
    console.error('获取活动列表失败:', error)
    ElMessage.error('获取活动列表失败')
  } finally {
    loading.value = false
  }
}

const tabs = computed(() => [
  { label: '宣讲会', value: 'talk', icon: 'fas fa-microphone-alt', count: stats.value.careerTalks },
  { label: '招聘会', value: 'fair', icon: 'fas fa-users', count: stats.value.jobFairs },
  { label: '场地管理', value: 'venue', icon: 'fas fa-building', count: 0 }
])

const totalPages = computed(() => Math.ceil(filteredActivities.value.length / pageSize.value) || 1)

const visiblePages = computed(() => {
  const pages = []
  const total = totalPages.value
  const current = currentPage.value
  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i)
  } else {
    pages.push(1)
    if (current > 3) pages.push('...')
    for (let i = Math.max(2, current - 1); i <= Math.min(total - 1, current + 1); i++) pages.push(i)
    if (current < total - 2) pages.push('...')
    pages.push(total)
  }
  return pages
})

const filteredActivities = computed(() => {
  let result = activitiesRaw.value
  if (activeTab.value === 'talk') {
    result = result.filter(a => a.activity_type === 'career_talk' || !a.activity_type)
  } else if (activeTab.value === 'fair') {
    result = result.filter(a => a.activity_type === 'job_fair')
  }
  return result
})

const paginatedActivities = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return filteredActivities.value.slice(start, start + pageSize.value)
})

const getTypeIcon = (activity) => {
  return activity.activity_type === 'job_fair' ? 'fas fa-users' : 'fas fa-microphone-alt'
}

const getTypeText = (activity) => {
  return activity.activity_type === 'job_fair' ? '招聘会' : '宣讲会'
}

const getGradientStyle = (activity) => {
  const index = (activity.id - 1) % gradientColors.length
  return {
    background: `linear-gradient(to right, ${gradientColors[index]})`
  }
}

const getAccentColor = (activity) => {
  const colors = ['blue', 'orange', 'purple', 'emerald', 'red', 'cyan', 'pink', 'indigo']
  const index = (activity.id - 1) % colors.length
  return colors[index] + '-600'
}

const getActivityBadge = (activity) => {
  if (!activity.start_time) return null
  const now = new Date()
  const start = new Date(activity.start_time)
  const diffDays = Math.ceil((start - now) / (1000 * 60 * 60 * 24))

  if (diffDays === 1) return '明天开始'
  if (diffDays > 1 && diffDays <= 7) return `${diffDays}天后`
  if (diffDays < 0) return '已结束'
  return null
}

const getBadgeClass = (activity) => {
  const badge = getActivityBadge(activity)
  if (badge === '明天开始') return 'bg-red-500 text-white'
  if (badge === '已结束') return 'bg-gray-500 text-white'
  return 'bg-yellow-400 text-yellow-900'
}

const getRemainder = (activity) => {
  const remainder = (activity.max_attendees || 0) - (activity.current_attendees || 0)
  return Math.max(0, remainder)
}

const getRemainderBg = (activity) => {
  const remainder = getRemainder(activity)
  if (remainder === 0) return 'bg-red-50'
  if (remainder < 10) return 'bg-orange-50'
  return 'bg-emerald-50'
}

const getRemainderColor = (activity) => {
  const remainder = getRemainder(activity)
  if (remainder === 0) return 'text-red-600'
  if (remainder < 10) return 'text-orange-600'
  return 'text-emerald-600'
}

const getAttendeesBg = (activity) => {
  const attendees = activity.current_attendees || 0
  const max = activity.max_attendees || 0
  if (max === 0) return 'bg-gray-50'
  const percentage = attendees / max
  if (percentage >= 0.9) return 'bg-red-50'
  if (percentage >= 0.7) return 'bg-orange-50'
  if (percentage >= 0.5) return 'bg-yellow-50'
  return 'bg-emerald-50'
}

const getAttendeesColor = (activity) => {
  const attendees = activity.current_attendees || 0
  const max = activity.max_attendees || 0
  if (max === 0) return 'text-gray-900'
  const percentage = attendees / max
  if (percentage >= 0.9) return 'text-red-600'
  if (percentage >= 0.7) return 'text-orange-600'
  if (percentage >= 0.5) return 'text-yellow-600'
  return 'text-emerald-600'
}

const getStatusClass = (status) => {
  const map = {
    pending: 'bg-yellow-100 text-yellow-700',
    approved: 'bg-green-100 text-green-700',
    rejected: 'bg-red-100 text-red-700',
    cancelled: 'bg-gray-100 text-gray-600',
    registering: 'bg-blue-100 text-blue-700',
    full: 'bg-red-100 text-red-700',
    ended: 'bg-gray-100 text-gray-500',
    draft: 'bg-gray-100 text-gray-500'
  }
  return map[status] || ''
}

const getStatusText = (status) => {
  const map = {
    pending: '待审核',
    approved: '报名中',
    rejected: '已驳回',
    cancelled: '已取消',
    registering: '报名中',
    full: '已满员',
    ended: '已结束',
    draft: '草稿'
  }
  return map[status] || status
}

const formatTime = (timeStr) => {
  if (!timeStr) return '-'
  const date = new Date(timeStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

const getCompanyAbbr = (name) => {
  if (!name) return '?'
  if (name.length <= 2) return name
  const matches = name.match(/[\u4e00-\u9fa5]/g)
  if (matches && matches.length >= 2) {
    return matches[0] + matches[1]
  }
  return name.slice(0, 2)
}

const formatDay = (timeStr) => {
  if (!timeStr) return '-'
  const date = new Date(timeStr)
  return date.getDate()
}

const formatWeekday = (timeStr) => {
  if (!timeStr) return '-'
  const date = new Date(timeStr)
  const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  return weekdays[date.getDay()]
}

const formatTimeRange = (startStr, endStr) => {
  if (!startStr) return '-'
  const start = new Date(startStr)
  const startTime = `${String(start.getHours()).padStart(2, '0')}:${String(start.getMinutes()).padStart(2, '0')}`
  if (!endStr) return startTime
  const end = new Date(endStr)
  const endTime = `${String(end.getHours()).padStart(2, '0')}:${String(end.getMinutes()).padStart(2, '0')}`
  return `${startTime} - ${endTime}`
}

const viewDetail = (activity) => {
  currentActivity.value = activity
  showDetailDialog.value = true
}

const editActivity = (activity) => {
  editDialogTitle.value = '编辑活动'
  editForm.value = {
    id: activity.id,
    title: activity.title || '',
    start_time: activity.start_time || '',
    end_time: activity.end_time || '',
    location: activity.location || '',
    max_attendees: activity.max_attendees || 200,
    description: activity.description || ''
  }
  showEditDialog.value = true
}

const saveActivity = async () => {
  if (!editForm.value.id) {
    ElMessage.warning('活动ID不存在')
    return
  }
  try {
    saving.value = true
    await adminAPI.updateActivity(editForm.value.id, editForm.value)
    ElMessage.success('保存成功')
    showEditDialog.value = false
    fetchActivities()
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

const loadCompanies = async () => {
  try {
    const res = await adminAPI.getCompanies({ page: 1, page_size: 100 })
    companies.value = res?.data?.companies || []
  } catch (error) {
    ElMessage.error('获取企业列表失败')
  }
}

const openCreateDialog = () => {
  createForm.value = {
    company_id: null,
    title: '',
    activity_type: activeTab.value === 'fair' ? 'job_fair' : 'career_talk',
    speaker_name: '',
    start_time: '',
    end_time: '',
    location: '',
    max_attendees: 200,
    description: ''
  }
  showCreateDialog.value = true
}

const submitCreate = async () => {
  const form = createForm.value
  if (!form.company_id) {
    ElMessage.warning('请选择所属企业')
    return
  }
  if (!form.title.trim()) {
    ElMessage.warning('请输入活动标题')
    return
  }
  if (!form.start_time || !form.end_time) {
    ElMessage.warning('请选择活动起止时间')
    return
  }
  if (new Date(form.end_time) <= new Date(form.start_time)) {
    ElMessage.warning('结束时间必须晚于开始时间')
    return
  }
  if (!form.location.trim()) {
    ElMessage.warning('请输入活动地点')
    return
  }
  try {
    creating.value = true
    await adminAPI.createActivity({
      ...form,
      title: form.title.trim(),
      location: form.location.trim(),
      speaker_name: form.speaker_name.trim() || null
    })
    ElMessage.success('活动发布成功')
    showCreateDialog.value = false
    fetchActivities()
    fetchStats()
  } catch (error) {
    ElMessage.error(error?.response?.data?.detail || '发布失败')
  } finally {
    creating.value = false
  }
}

const deleteActivity = async (activity) => {
  try {
    await ElMessageBox.confirm('确定要删除该活动吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await adminAPI.deleteActivity(activity.id)
    ElMessage.success('删除成功')
    fetchActivities()
    fetchStats()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const exportData = (format) => {
  showExportMenu.value = false
  const data = paginatedActivities.value.map(a => ({
    '活动标题': a.title,
    '活动类型': getTypeText(a),
    '时间': a.date || a.start_time || '-',
    '地点': a.location || '-',
    '参与人数': a.attendees || a.participant_count || 0,
    '状态': a.status === 'approved' ? '已通过' : a.status === 'pending' ? '待审核' : '已取消',
    '创建时间': a.created_at || '-'
  }))

  if (format === 'csv') {
    const ws = XLSX.utils.json_to_sheet(data)
    const csv = XLSX.utils.sheet_to_csv(ws)
    const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `活动数据_${new Date().toISOString().slice(0, 10)}.csv`
    a.click()
    URL.revokeObjectURL(url)
  } else {
    const ws = XLSX.utils.json_to_sheet(data)
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, '活动数据')
    XLSX.writeFile(wb, `活动数据_${new Date().toISOString().slice(0, 10)}.xlsx`)
  }
  ElMessage.success('导出成功')
}

let searchTimer = null
const handleSearch = () => {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    currentPage.value = 1
    fetchActivities()
  }, 500)
}

watch([activeTab, filterStatus, searchKeyword], () => {
  currentPage.value = 1
  fetchActivities()
})

onMounted(() => {
  fetchStats()
  fetchActivities()
  loadCompanies()
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.relative')) {
      showExportMenu.value = false
    }
  })
})
</script>
