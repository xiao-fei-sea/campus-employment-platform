<template>
  <div class="min-h-screen p-4 pl-2">
    <div class="mb-4 flex items-center justify-between">
      <p class="text-gray-600 text-lg">找到 <span class="font-bold text-blue-600 text-xl">{{ total }}</span> 个匹配岗位</p>
      <div class="flex items-center space-x-2">
        <input
          v-model="searchKeyword"
          @keyup.enter="searchJobs"
          type="text"
          placeholder="搜索岗位名称..."
          class="pl-4 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 w-64"
        >
        <button @click="searchJobs" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
          <i class="fas fa-search"></i>
        </button>
      </div>
    </div>

    <div class="flex gap-8">
      <div class="w-72 flex-shrink-0">
        <div class="bg-white rounded-xl shadow-sm p-6 sticky top-24">
          <h3 class="font-bold text-gray-900 mb-6 flex items-center">
            <i class="fas fa-filter mr-2"></i>
            筛选条件
          </h3>

          <div class="mb-6">
            <h4 class="text-sm font-medium text-gray-700 mb-3">行业领域</h4>
            <div class="space-y-2">
              <label v-for="industry in industryOptions" :key="industry.value" class="flex items-center">
                <input
                  type="checkbox"
                  v-model="filters.industry"
                  :value="industry.value"
                  class="w-4 h-4 text-blue-600 border-gray-300 rounded"
                >
                <span class="ml-2 text-sm text-gray-600">{{ industry.label }}</span>
              </label>
            </div>
          </div>

          <div class="mb-6">
            <h4 class="text-sm font-medium text-gray-700 mb-3">工作地点</h4>
            <div class="space-y-2">
              <label v-for="city in cityOptions" :key="city.value" class="flex items-center">
                <input
                  type="checkbox"
                  v-model="filters.location"
                  :value="city.value"
                  class="w-4 h-4 text-blue-600 border-gray-300 rounded"
                >
                <span class="ml-2 text-sm text-gray-600">{{ city.label }}</span>
              </label>
            </div>
          </div>

          <div class="mb-6">
            <h4 class="text-sm font-medium text-gray-700 mb-3">薪资范围</h4>
            <div class="space-y-2">
              <label v-for="salary in salaryOptions" :key="salary.value" class="flex items-center">
                <input
                  type="checkbox"
                  v-model="filters.salary"
                  :value="salary.value"
                  class="w-4 h-4 text-blue-600 border-gray-300 rounded"
                >
                <span class="ml-2 text-sm text-gray-600">{{ salary.label }}</span>
              </label>
            </div>
          </div>

          <div class="mb-6">
            <h4 class="text-sm font-medium text-gray-700 mb-3">学历要求</h4>
            <div class="space-y-2">
              <label v-for="edu in educationOptions" :key="edu.value" class="flex items-center">
                <input
                  type="checkbox"
                  v-model="filters.education"
                  :value="edu.value"
                  class="w-4 h-4 text-blue-600 border-gray-300 rounded"
                >
                <span class="ml-2 text-sm text-gray-600">{{ edu.label }}</span>
              </label>
            </div>
          </div>

          <div class="mb-6">
            <h4 class="text-sm font-medium text-gray-700 mb-3">企业性质</h4>
            <div class="space-y-2">
              <label v-for="type in companyTypeOptions" :key="type.value" class="flex items-center">
                <input
                  type="checkbox"
                  v-model="filters.companyType"
                  :value="type.value"
                  class="w-4 h-4 text-blue-600 border-gray-300 rounded"
                >
                <span class="ml-2 text-sm text-gray-600">{{ type.label }}</span>
              </label>
            </div>
          </div>

          <button @click="handleSearch" class="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-xl transition-colors">
            应用筛选
          </button>
          <button @click="resetFilters" class="w-full py-2.5 mt-2 text-gray-600 hover:bg-gray-100 rounded-xl transition-colors">
            重置筛选
          </button>
        </div>
      </div>

      <div class="flex-1">
        <div class="bg-white rounded-xl shadow-sm p-4 mb-4 flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-500">排序方式：</span>
            <button
              v-for="sort in sortOptions"
              :key="sort.value"
              @click="sortBy = sort.value; handleSearch()"
              :class="[
                'px-4 py-1.5 text-sm rounded-lg',
                sortBy === sort.value ? 'bg-blue-50 text-blue-600 font-medium' : 'text-gray-600 hover:bg-gray-100'
              ]"
            >
              {{ sort.label }}
            </button>
          </div>
          <div class="flex items-center space-x-2">
            <button @click="viewMode = 'grid'" class="p-2 rounded-lg" :class="viewMode === 'grid' ? 'text-blue-600 bg-blue-50' : 'text-gray-600 hover:bg-gray-100'">
              <i class="fas fa-th-large"></i>
            </button>
            <button @click="viewMode = 'list'" class="p-2 rounded-lg" :class="viewMode === 'list' ? 'text-blue-600 bg-blue-50' : 'text-gray-600 hover:bg-gray-100'">
              <i class="fas fa-list"></i>
            </button>
          </div>
        </div>

        <div :class="viewMode === 'grid' ? 'grid grid-cols-2 gap-4' : 'space-y-4'">
          <div
            v-for="job in jobList"
            :key="job.id"
            class="bg-white rounded-xl shadow-sm p-4 hover:shadow-md transition-all cursor-pointer"
            :class="viewMode === 'grid' ? '' : ''"
            @click="goToJobDetail(job.id)"
          >
            <div class="flex items-start justify-between">
              <div class="flex items-start space-x-3">
                <div v-if="job.logo" class="w-14 h-14 rounded-xl object-cover overflow-hidden">
                  <img :src="job.logo" @error="job.logo = ''" class="w-full h-full object-cover">
                </div>
                <div v-else class="w-14 h-14 rounded-xl bg-blue-600 flex items-center justify-center text-white font-bold text-lg">
                  {{ job.company?.charAt(0) || '企' }}
                </div>
                <div>
                  <div class="flex items-center space-x-2 mb-0.5">
                    <span class="font-bold text-gray-900 hover:text-blue-600 text-sm cursor-pointer">
                      {{ job.title }}
                    </span>
                    <span v-if="job.is_urgent" class="px-2 py-0.5 bg-green-100 text-green-700 text-xs rounded-full">急聘</span>
                    <span v-if="job.is_campus" class="px-2 py-0.5 bg-blue-100 text-blue-700 text-xs rounded-full">校招</span>
                  </div>
                  <div class="flex items-center space-x-2 mb-1">
                    <p class="text-gray-600 text-sm">{{ job.company }}</p>
                    <span v-if="job.isApplied" class="px-2 py-0.5 bg-green-100 text-green-700 text-xs rounded-full">已投递</span>
                  </div>
                  <div class="flex items-center space-x-3 text-xs text-gray-500">
                    <span><i class="fas fa-map-marker-alt mr-1"></i>{{ job.location }}</span>
                    <span><i class="fas fa-money-bill-wave mr-1"></i>{{ job.salary }}</span>
                    <span><i class="fas fa-graduation-cap mr-1"></i>{{ job.education }}</span>
                    <span><i class="fas fa-clock mr-1"></i>{{ job.postedDaysAgo }}</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="mt-2 flex flex-wrap gap-1.5">
              <span
                v-for="(tag, index) in job.tags"
                :key="index"
                class="px-3 py-1 bg-gray-100 text-gray-600 text-xs rounded-full"
              >
                {{ tag }}
              </span>
            </div>
            <div class="mt-2 pt-2 border-t border-gray-100 flex items-center justify-between">
              <div class="flex items-center space-x-4 text-sm text-gray-500">
                <span><i class="fas fa-eye mr-1"></i>{{ job.viewCount || 0 }} 浏览</span>
                <span><i class="fas fa-paper-plane mr-1"></i>{{ job.applyCount || 0 }} 投递</span>
              </div>
              <button @click.stop="applyJob(job)" class="px-4 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs rounded-lg transition-colors" :class="{ 'bg-green-600 hover:bg-green-700': job.isApplied, 'cursor-not-allowed': job.isApplied }">
                {{ job.isApplied ? '已投递' : '投递简历' }}
              </button>
            </div>
          </div>
        </div>

        <div class="flex justify-center mt-6">
          <el-pagination
            :current-page="currentPage"
            :page-size="10"
            :total="total"
            layout="total, prev, pager, next"
            background
            @current-change="handlePageChange"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { studentAPI } from '@/api'
import { useRouter } from 'vue-router'

const router = useRouter()

const goToJobDetail = (id) => {
  router.push(`/student/jobs/${id}`)
}

const searchKeyword = ref('')
const currentPage = ref(1)
const total = ref(0)
const sortBy = ref('comprehensive')
const viewMode = ref('list')

const sortOptions = [
  { label: '综合排序', value: 'comprehensive' },
  { label: '最新发布', value: 'latest' },
  { label: '薪资最高', value: 'salary' },
  { label: '浏览最多', value: 'views' }
]

const filters = reactive({
  location: [],
  industry: [],
  salary: [],
  education: [],
  companyType: []
})

const cityOptions = [
  { label: '北京', value: '北京' },
  { label: '上海', value: '上海' },
  { label: '深圳', value: '深圳' },
  { label: '杭州', value: '杭州' },
  { label: '广州', value: '广州' }
]

const industryOptions = [
  { label: '互联网/IT', value: 'it' },
  { label: '金融/银行', value: 'finance' },
  { label: '教育培训', value: 'education' },
  { label: '智能制造', value: 'manufacturing' },
  { label: '医疗健康', value: 'healthcare' }
]

const salaryOptions = [
  { label: '20K以上', value: '20+' },
  { label: '15K-20K', value: '15-20' },
  { label: '10K-15K', value: '10-15' },
  { label: '5K-10K', value: '5-10' }
]

const educationOptions = [
  { label: '博士', value: '博士' },
  { label: '硕士', value: '硕士' },
  { label: '本科', value: '本科' },
  { label: '大专', value: '大专' }
]

const companyTypeOptions = [
  { label: '上市公司', value: 'public' },
  { label: '国有企业', value: 'state' },
  { label: '民营企业', value: 'private' },
  { label: '外资企业', value: 'foreign' }
]

const jobList = ref([])

const fetchJobs = async () => {
  try {
    const params = {
      page: currentPage.value,
      page_size: 10,
      sort: sortBy.value
    }
    if (searchKeyword.value) {
      params.keyword = searchKeyword.value
    }
    if (filters.location.length > 0) {
      params.city = filters.location.join(',')
    }
    if (filters.salary.length > 0) {
      const salaryMap = {
        '20+': { min: 20000, max: 100000 },
        '15-20': { min: 15000, max: 20000 },
        '10-15': { min: 10000, max: 15000 },
        '5-10': { min: 5000, max: 10000 }
      }
      const ranges = filters.salary.map(s => salaryMap[s]).filter(Boolean)
      if (ranges.length > 0) {
        const minSalaries = ranges.map(r => r.min)
        const maxSalaries = ranges.map(r => r.max)
        params.salary_min = Math.min(...minSalaries)
        params.salary_max = Math.max(...maxSalaries)
      }
    }
    if (filters.industry.length > 0) {
      params.industry = filters.industry.join(',')
    }
    if (filters.education.length > 0) {
      params.education = filters.education.join(',')
    }

    const res = await studentAPI.getJobs(params)
    const data = res.data?.data || res.data
    const totalCount = res.data?.total || (Array.isArray(data) ? data.length : 0)
    jobList.value = (Array.isArray(data) ? data : []).map(job => ({
      id: job.id,
      title: job.title,
      company: job.company_name,
      logo: job.company_logo || 'https://via.placeholder.com/80',
      salary: job.salary_show || `${(job.salary_min || 0) / 1000}-${(job.salary_max || 0) / 1000}K`,
      location: job.city || job.province || '未知',
      experience: job.requirement || '不限',
      education: job.education || '本科',
      tags: job.skills ? job.skills.split(',').slice(0, 4) : [],
      isFavorite: job.is_favorited || false,
      isApplied: job.has_applied || false,
      is_urgent: job.is_urgent || false,
      is_campus: job.is_campus_recruit || false,
      viewCount: job.view_count ?? Math.floor(Math.random() * 2000),
      applyCount: job.application_count ?? Math.floor(Math.random() * 200),
      postedDaysAgo: getPostedDaysAgo(job.created_at)
    }))
    total.value = totalCount
  } catch (error) {
    console.error('获取岗位列表失败:', error)
  }
}

const getPostedDaysAgo = (dateStr) => {
  if (!dateStr) return '未知'
  const date = new Date(dateStr)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

const handleSearch = () => {
  currentPage.value = 1
  fetchJobs()
}

const handlePageChange = (page) => {
  currentPage.value = page
  fetchJobs()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const resetFilters = () => {
  filters.location = []
  filters.industry = []
  filters.salary = []
  filters.education = []
  filters.companyType = []
  handleSearch()
}

const applyJob = async (job) => {
  if (job.isApplied) return
  try {
    await studentAPI.applyJob(job.id, {})
    job.isApplied = true
    ElMessage.success('投递成功')
    await fetchJobs()
  } catch (error) {
    if (error.response?.data?.detail === '您已投递过此岗位') {
      job.isApplied = true
      ElMessage.warning('您已投递过此岗位')
    } else if (error.response?.data?.detail) {
      ElMessage.error(error.response.data.detail)
    } else {
      ElMessage.error('投递失败，请重试')
    }
  }
}

const searchJobs = () => {
  currentPage.value = 1
  fetchJobs()
}

onMounted(() => {
  fetchJobs()
})
</script>
