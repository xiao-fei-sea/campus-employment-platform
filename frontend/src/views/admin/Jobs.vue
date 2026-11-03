<template>
  <div class="space-y-6">
    <div class="grid grid-cols-5 gap-6">
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex items-center space-x-5">
        <div class="w-16 h-16 bg-emerald-100 rounded-2xl flex items-center justify-center flex-shrink-0">
          <i class="fas fa-briefcase text-emerald-500 text-3xl"></i>
        </div>
        <div>
          <p class="text-gray-500 text-base">岗位总数</p>
          <p class="text-4xl font-bold text-gray-900">{{ stats.totalJobs.toLocaleString() }}</p>
        </div>
      </div>
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex items-center space-x-5">
        <div class="w-16 h-16 bg-yellow-100 rounded-2xl flex items-center justify-center flex-shrink-0">
          <i class="fas fa-clock text-yellow-500 text-3xl"></i>
        </div>
        <div>
          <p class="text-gray-500 text-base">待审核</p>
          <p class="text-4xl font-bold text-yellow-600">{{ stats.pending.toLocaleString() }}</p>
        </div>
      </div>
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex items-center space-x-5">
        <div class="w-16 h-16 bg-green-100 rounded-2xl flex items-center justify-center flex-shrink-0">
          <i class="fas fa-check-circle text-green-500 text-3xl"></i>
        </div>
        <div>
          <p class="text-gray-500 text-base">已通过</p>
          <p class="text-4xl font-bold text-green-600">{{ stats.approved.toLocaleString() }}</p>
        </div>
      </div>
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex items-center space-x-5">
        <div class="w-16 h-16 bg-red-100 rounded-2xl flex items-center justify-center flex-shrink-0">
          <i class="fas fa-times-circle text-red-500 text-3xl"></i>
        </div>
        <div>
          <p class="text-gray-500 text-base">已驳回</p>
          <p class="text-4xl font-bold text-red-600">{{ stats.rejected.toLocaleString() }}</p>
        </div>
      </div>
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex items-center space-x-5">
        <div class="w-16 h-16 bg-gray-100 rounded-2xl flex items-center justify-center flex-shrink-0">
          <i class="fas fa-ban text-gray-500 text-3xl"></i>
        </div>
        <div>
          <p class="text-gray-500 text-base">已下架</p>
          <p class="text-4xl font-bold text-gray-600">{{ stats.closed.toLocaleString() }}</p>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-2xl p-6 shadow-sm">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <button
            v-for="tab in tabs"
            :key="tab.value"
            :class="[
              'px-4 py-2 rounded-xl transition-colors text-sm',
              filterStatus === tab.value
                ? 'bg-emerald-600 text-white'
                : 'text-gray-600 hover:bg-gray-100'
            ]"
            @click="filterStatus = tab.value"
          >
            {{ tab.label }}
          </button>
        </div>
        <div class="flex items-center space-x-4">
          <input v-model="filterIndustry" type="text" placeholder="搜索行业..." class="px-4 py-2.5 bg-gray-100 border-0 rounded-xl text-gray-600 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 hover:bg-gray-200 transition-colors w-40" />
          <el-select v-model="filterSort" class="w-40">
            <el-option label="最新提交" value="latest" />
            <el-option label="薪资最高" value="salary" />
            <el-option label="浏览最多" value="views" />
          </el-select>
        </div>
      </div>
    </div>

    <div class="space-y-4">
      <div
        v-for="job in filteredJobs"
        :key="job.id"
        :class="[
          'bg-white rounded-2xl p-6 shadow-sm transition-all hover:shadow-md',
          job.status === 'approved' ? 'border-l-4 border-green-500' : ''
        ]"
      >
        <div class="flex items-start justify-between">
          <div class="flex items-start space-x-4">
            <img :src="job.company_logo || 'https://via.placeholder.com/56'" class="w-14 h-14 rounded-xl object-cover">
            <div class="flex-1">
              <div class="flex items-center space-x-3 mb-2">
                <h3 class="text-lg font-bold text-gray-900">{{ job.title }}</h3>
                <span :class="getStatusClass(job.status)" class="px-2 py-0.5 rounded-full text-xs">{{ getJobStatusText(job.status) }}</span>
              </div>
              <p class="text-gray-600 mb-2">{{ job.company_name || '-' }}{{ job.industry ? ' · ' + getIndustryText(job.industry) : '' }}</p>
              <div class="flex items-center space-x-6 text-sm text-gray-500">
                <span><i class="fas fa-money-bill mr-1"></i>{{ job.salary_show || '-' }}</span>
                <span><i class="fas fa-map-marker-alt mr-1"></i>{{ job.province || '' }}{{ job.city || '' }}{{ job.district || '' }}</span>
                <span><i class="fas fa-clock mr-1"></i>{{ job.experience || '-' }}</span>
                <span><i class="fas fa-calendar mr-1"></i>{{ formatDate(job.created_at) }}</span>
              </div>
              <div v-if="job.skills" class="flex items-center space-x-2 mt-3">
                <span
                  v-for="tag in (job.skills || '').split(',')"
                  :key="tag"
                  class="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded"
                >
                  {{ tag.trim() }}
                </span>
              </div>
            </div>
          </div>
          <div class="flex flex-col items-end space-y-2">
            <div class="flex items-center space-x-2">
              <button class="p-2 text-gray-500 hover:text-emerald-600 hover:bg-emerald-50 rounded-lg transition-colors" title="查看详情" @click="viewDetail(job)">
                <i class="fas fa-eye"></i>
              </button>
            </div>
            <div v-if="job.status === 'pending'" class="flex items-center space-x-2 mt-2">
              <el-button type="success" size="small" @click="approve(job)">
                <i class="fas fa-check mr-1"></i>通过
              </el-button>
              <el-button type="danger" size="small" @click="reject(job)">
                <i class="fas fa-times mr-1"></i>驳回
              </el-button>
            </div>
          </div>
        </div>
      </div>

      <div class="px-6 py-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-t border-gray-200 bg-white rounded-b-2xl">
        <p class="text-gray-500 text-sm">共 {{ totalJobs.toLocaleString() }} 条数据</p>
        <div class="flex items-center flex-wrap justify-center gap-1">
          <button type="button" class="px-3 py-2 bg-white text-gray-600 rounded-lg hover:bg-gray-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-sm border border-gray-200" :disabled="currentPage <= 1" @click="currentPage--" title="上一页">
            <i class="fas fa-chevron-left" />
          </button>
          <template v-for="(p, idx) in visiblePages">
            <span v-if="p === '...'" :key="`ellipsis-${idx}`" class="px-2 text-gray-400 text-sm">...</span>
            <button v-else :key="`page-btn-${p}`" type="button" class="px-3 py-2 rounded-lg transition-colors text-sm font-medium" :class="p === currentPage ? 'bg-emerald-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-100 border border-gray-200'" @click="currentPage = p">
              {{ p }}
            </button>
          </template>
          <button type="button" class="px-3 py-2 bg-white text-gray-600 rounded-lg hover:bg-gray-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-sm border border-gray-200" :disabled="currentPage >= totalPages" @click="currentPage++" title="下一页">
            <i class="fas fa-chevron-right" />
          </button>
        </div>
      </div>
    </div>

    <el-dialog v-model="showDetailDialog" title="岗位详情" width="600px">
      <div class="space-y-4" v-if="currentJob.id">
        <div class="flex items-center space-x-4 mb-6">
          <img :src="currentJob.company_logo || 'https://via.placeholder.com/56'" class="w-16 h-16 rounded-xl object-cover">
          <div>
            <h3 class="text-xl font-bold text-gray-900">{{ currentJob.title }}</h3>
            <p class="text-gray-500">{{ currentJob.company_name || '-' }}</p>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <p class="text-sm text-gray-500">行业</p>
            <p class="font-medium">{{ getIndustryText(currentJob.industry) || '-' }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">薪资</p>
            <p class="font-medium">{{ currentJob.salary_show || '-' }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">工作地点</p>
            <p class="font-medium">{{ currentJob.province || '' }}{{ currentJob.city || '' }}{{ currentJob.district || '' }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">经验要求</p>
            <p class="font-medium">{{ currentJob.experience || '-' }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">学历要求</p>
            <p class="font-medium">{{ currentJob.education || '-' }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">招聘人数</p>
            <p class="font-medium">{{ currentJob.headcount || '-' }}</p>
          </div>
        </div>

        <div v-if="currentJob.skills">
          <p class="text-sm text-gray-500 mb-2">技能要求</p>
          <div class="flex flex-wrap gap-2">
            <span v-for="tag in currentJob.skills.split(',')" :key="tag" class="px-3 py-1 bg-gray-100 text-gray-600 text-sm rounded-full">
              {{ tag.trim() }}
            </span>
          </div>
        </div>

        <div v-if="currentJob.description">
          <p class="text-sm text-gray-500 mb-2">岗位描述</p>
          <p class="text-gray-700 whitespace-pre-wrap">{{ currentJob.description }}</p>
        </div>

        <div v-if="currentJob.requirement">
          <p class="text-sm text-gray-500 mb-2">岗位要求</p>
          <p class="text-gray-700 whitespace-pre-wrap">{{ currentJob.requirement }}</p>
        </div>

        <div v-if="currentJob.benefit">
          <p class="text-sm text-gray-500 mb-2">福利待遇</p>
          <p class="text-gray-700 whitespace-pre-wrap">{{ currentJob.benefit }}</p>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
defineOptions({ name: 'Jobs' })
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { adminAPI } from '@/api/index'

const searchKeyword = ref('')
const filterStatus = ref('')
const filterIndustry = ref('')
const filterSort = ref('latest')
const currentPage = ref(1)
const pageSize = ref(10)

const stats = ref({
  totalJobs: 0,
  pending: 0,
  approved: 0,
  rejected: 0,
  closed: 0
})

const jobsRaw = ref([])
const totalJobs = ref(0)
const loading = ref(false)
const showDetailDialog = ref(false)
const currentJob = ref({})

async function fetchStats() {
  try {
    const allJobsRes = await adminAPI.getJobs({ page: 1, page_size: 10000 })
    if (allJobsRes?.data) {
      const rawData = allJobsRes.data
      const allJobs = rawData.jobs || rawData.data?.jobs || []
      stats.value = {
        totalJobs: rawData.total || rawData.data?.total || allJobs.length,
        pending: allJobs.filter(j => j.status === 'pending').length,
        approved: allJobs.filter(j => j.status === 'approved').length,
        rejected: allJobs.filter(j => j.status === 'rejected').length,
        closed: allJobs.filter(j => j.status === 'closed').length
      }
    }
  } catch (error) {
    console.error('Failed to fetch stats:', error)
  }
}

async function fetchJobs() {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }
    if (filterStatus.value && filterStatus.value !== 'all') {
      params.status = filterStatus.value
    }
    if (searchKeyword.value.trim()) {
      params.keyword = searchKeyword.value.trim()
    }
    const res = await adminAPI.getJobs(params)
    if (res?.data) {
      const rawData = res.data
      jobsRaw.value = rawData.jobs || rawData.data?.jobs || []
      totalJobs.value = rawData.total || rawData.data?.total || 0
    }
  } catch (error) {
    console.error('Failed to fetch jobs:', error)
  } finally {
    loading.value = false
  }
}

const tabs = [
  { label: '全部', value: '' },
  { label: '待审核', value: 'pending' },
  { label: '已通过', value: 'approved' },
  { label: '已驳回', value: 'rejected' }
]

const totalPages = computed(() => Math.ceil(totalJobs.value / pageSize.value) || 1)

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

const filteredJobs = computed(() => {
  let result = jobsRaw.value.filter(job => {
    if (filterIndustry.value) {
      const industryText = getIndustryText(job.industry).toLowerCase()
      const searchText = filterIndustry.value.toLowerCase()
      if (!industryText.includes(searchText)) return false
    }
    return true
  })

  if (filterSort.value === 'salary') {
    result = [...result].sort((a, b) => {
      const salaryA = (a.salary_max || 0) * 1000
      const salaryB = (b.salary_max || 0) * 1000
      return salaryB - salaryA
    })
  }

  return result
})

const getStatusClass = (status) => {
  const map = {
    pending: 'bg-yellow-100 text-yellow-700',
    approved: 'bg-green-100 text-green-700',
    rejected: 'bg-red-100 text-red-700',
    closed: 'bg-gray-100 text-gray-600',
    draft: 'bg-gray-100 text-gray-500'
  }
  return map[status] || ''
}

const getJobStatusText = (status) => {
  const map = {
    pending: '待审核',
    approved: '已通过',
    rejected: '已驳回',
    closed: '已关闭',
    draft: '草稿'
  }
  return map[status] || status
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

const getIndustryText = (industry) => {
  const map = {
    it: '互联网/IT',
    finance: '金融',
    manufacturing: '制造业',
    education: '教育',
    healthcare: '医疗',
    real_estate: '房地产',
    retail: '零售'
  }
  return map[industry] || industry || '-'
}

const viewDetail = (job) => {
  currentJob.value = job
  showDetailDialog.value = true
}

async function approve(job) {
  try {
    await adminAPI.approveJob(job.id)
    job.status = 'approved'
    ElMessage.success('已通过审核')
    fetchStats()
    fetchJobs()
  } catch (error) {
    console.error('Approve failed:', error)
    ElMessage.error('操作失败')
  }
}

async function reject(job) {
  try {
    const { value: reason } = await ElMessageBox.prompt('请输入驳回原因', '岗位审核', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      inputPlaceholder: '请输入驳回原因'
    })
    if (!reason || !reason.trim()) {
      ElMessage.warning('请输入驳回原因')
      return
    }
    await adminAPI.rejectJob(job.id, { status: 'rejected', comment: reason.trim() })
    job.status = 'rejected'
    ElMessage.success('已驳回')
    fetchStats()
    fetchJobs()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Reject failed:', error)
      ElMessage.error('操作失败')
    }
  }
}

watch([filterStatus, filterIndustry, filterSort, searchKeyword], () => {
  currentPage.value = 1
  fetchJobs()
})

watch(currentPage, () => {
  fetchJobs()
})

onMounted(() => {
  fetchStats()
  fetchJobs()
})
</script>
