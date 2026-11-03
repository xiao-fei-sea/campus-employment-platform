<template>
  <div class="space-y-6">
    <div class="flex items-center space-x-4">
      <button @click="goBack" class="p-2 hover:bg-gray-100 rounded-lg transition-colors">
        <i class="fas fa-arrow-left text-gray-600"></i>
      </button>
      <span class="text-gray-500">返回列表</span>
    </div>
    <div class="grid grid-cols-3 gap-6">
      <!-- Main Content -->
      <div class="col-span-2 space-y-6">
        <!-- Job Header -->
        <div class="card p-6">
          <div class="flex items-start justify-between">
            <div class="flex items-start space-x-4">
              <img :src="job.logo || '/placeholder-logo.png'" class="w-20 h-20 rounded-xl object-cover">
              <div>
                <h1 class="text-2xl font-bold text-gray-900">{{ job.title }}</h1>
                <p class="text-lg text-gray-600 mt-1">{{ job.company }}</p>
                <div class="flex items-center space-x-6 text-sm text-gray-500 mt-3">
                  <span class="flex items-center">
                    <i class="fas fa-money-bill mr-2 text-emerald-600"></i>
                    {{ job.salary }}
                  </span>
                  <span class="flex items-center">
                    <i class="fas fa-map-marker-alt mr-2 text-gray-400"></i>
                    {{ job.location }}
                  </span>
                  <span class="flex items-center">
                    <i class="fas fa-clock mr-2 text-gray-400"></i>
                    {{ job.experience }}
                  </span>
                </div>
              </div>
            </div>
            <div class="flex flex-col items-end space-y-2">
              <button @click="toggleFavorite" class="p-3 border-2 rounded-xl">
                <i :class="isFavorite ? 'fas fa-star text-yellow-500' : 'far fa-star text-gray-400'"></i>
              </button>
              <el-button type="primary" size="large" @click="handleApply" :disabled="isApplied">{{ isApplied ? '已投递' : '投递简历' }}</el-button>
            </div>
          </div>
        </div>

        <!-- Job Description -->
        <div class="card p-6">
          <h3 class="text-lg font-bold text-gray-900 mb-4">职位描述</h3>
          <div class="prose text-gray-600 space-y-4">
            <p>{{ job.description || '暂无描述' }}</p>
            <div class="mt-4">
              <h4 class="font-medium text-gray-900 mb-2">任职要求</h4>
              <ul class="list-disc list-inside space-y-1">
                <li v-for="(item, index) in job.requirements" :key="index">{{ item }}</li>
              </ul>
            </div>
            <div class="mt-4">
              <h4 class="font-medium text-gray-900 mb-2">员工福利</h4>
              <div class="flex flex-wrap gap-2">
                <span v-for="(item, index) in job.benefits" :key="index" class="px-3 py-1 bg-blue-50 text-blue-700 text-sm rounded-full">
                  {{ item }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Company Info -->
        <div class="card p-6">
          <h3 class="text-lg font-bold text-gray-900 mb-4">公司信息</h3>
          <div class="flex items-start space-x-4">
            <img :src="job.logo || '/placeholder-logo.png'" class="w-16 h-16 rounded-xl object-cover">
            <div class="flex-1">
              <h4 class="font-medium text-gray-900">{{ job.company }}</h4>
              <p class="text-gray-500 text-sm mt-1">{{ job.companyInfo }}</p>
              <div class="grid grid-cols-3 gap-4 mt-4 text-sm">
                <div>
                  <p class="text-gray-500">行业</p>
                  <p class="font-medium text-gray-900">{{ job.industry }}</p>
                </div>
                <div>
                  <p class="text-gray-500">规模</p>
                  <p class="font-medium text-gray-900">{{ job.scale }}</p>
                </div>
                <div>
                  <p class="text-gray-500">地址</p>
                  <p class="font-medium text-gray-900">{{ job.companyAddress || job.address || (job.location ? job.location : '暂无') }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Sidebar -->
      <div class="space-y-6">
        <!-- Job Tags -->
        <div class="card p-6">
          <h3 class="text-lg font-bold text-gray-900 mb-4">职位标签</h3>
          <div class="flex flex-wrap gap-2">
            <span v-if="job.jobTypeTag" class="px-3 py-1 bg-blue-50 text-blue-700 text-sm rounded-full">
              {{ job.jobTypeTag }}
            </span>
            <span v-if="job.isUrgent" class="px-3 py-1 bg-red-50 text-red-700 text-sm rounded-full">
              急招
            </span>
            <span v-if="job.isHighlight" class="px-3 py-1 bg-yellow-50 text-yellow-700 text-sm rounded-full">
              精挑
            </span>
            <span v-for="tag in job.tags" :key="tag" class="px-3 py-1 bg-emerald-50 text-emerald-700 text-sm rounded-full">
              {{ tag }}
            </span>
          </div>
        </div>

        <!-- Similar Jobs -->
        <div class="card p-6">
          <h3 class="text-lg font-bold text-gray-900 mb-4">相似职位</h3>
          <div class="space-y-4">
            <router-link v-for="similar in similarJobs" :key="similar.id" :to="`/student/jobs/${similar.id}`" class="block p-3 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors">
              <p class="font-medium text-gray-900">{{ similar.title }}</p>
              <p class="text-sm text-gray-500 mt-1">{{ similar.company_name }}</p>
              <p class="text-sm text-emerald-600 mt-1">{{ similar.salary }}</p>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { studentAPI } from '@/api'

const route = useRoute()
const router = useRouter()

const goBack = () => {
  router.push('/student/jobs')
}

const isFavorite = ref(false)
const isApplied = ref(false)

const job = ref({
  id: route.params.id,
  title: '',
  company: '',
  logo: '',
  salary: '',
  location: '',
  experience: '',
  education: '',
  tags: [],
  description: '',
  responsibilities: [],
  requirements: [],
  benefits: [],
  companyInfo: '',
  industry: '',
  scale: '',
  address: '',
  postedDaysAgo: '',
  companyShortName: '',
  companyWebsite: '',
  companyAddress: '',
  jobTypeTag: '',
  isUrgent: false,
  isHighlight: false
})

const similarJobs = ref([])

const getPostedDaysAgo = (dateStr) => {
  if (!dateStr) return '刚刚'
  const created = new Date(dateStr)
  const now = new Date()
  const diff = Math.floor((now - created) / (1000 * 60 * 60 * 24))
  if (diff === 0) return '今天'
  if (diff === 1) return '昨天'
  if (diff < 7) return `${diff}天前`
  if (diff < 30) return `${Math.floor(diff / 7)}周前`
  if (diff < 365) return `${Math.floor(diff / 30)}个月前`
  return `${Math.floor(diff / 365)}年前`
}

const getScaleText = (scale) => {
  const scaleMap = {
    'small': '50人以下',
    'medium': '50-200人',
    'large': '200-1000人',
    'super_large': '1000人以上'
  }
  return scaleMap[scale] || '未知规模'
}

const getIndustryText = (industry) => {
  const industryMap = {
    'it': '互联网/IT',
    'finance': '金融/银行',
    'manufacturing': '智能制造',
    'education': '教育培训',
    'healthcare': '医疗健康',
    'real_estate': '房地产',
    'retail': '零售',
    'other': '其他'
  }
  return industryMap[industry] || '其他'
}

const getJobTypeText = (type) => {
  const typeMap = {
    'full_time': '全职',
    'part_time': '兼职',
    'internship': '实习',
    'practice': '实训'
  }
  return typeMap[type] || '全职'
}

const fetchJobDetail = async () => {
  try {
    const res = await studentAPI.getJobDetail(job.value.id)
    const data = res.data?.data || res.data
    if (data) {
      job.value = {
        id: data.id,
        title: data.title || '',
        company: data.company_name || '',
        logo: data.company_logo || '',
        salary: data.salary_show || `${(data.salary_min || 0) / 1000}-${(data.salary_max || 0) / 1000}K`,
        location: data.city || data.province || '未知',
        experience: data.experience || '不限',
        education: data.education || '本科',
        tags: data.skills ? data.skills.split(',').filter(t => t.trim()).slice(0, 4) : [],
        description: data.description || '',
        responsibilities: [],
        requirements: data.requirement ? data.requirement.split('\n').filter(r => r.trim()) : ['本科及以上学历', '相关工作经验', '良好的沟通能力', '团队合作精神'],
        benefits: data.benefit ? data.benefit.split('\n').filter(r => r.trim()) : ['五险一金', '带薪年假', '节日福利', '定期体检'],
        companyInfo: data.company_description || '',
        industry: getIndustryText(data.company_industry),
        scale: getScaleText(data.company_scale),
        address: data.address || '',
        postedDaysAgo: getPostedDaysAgo(data.created_at),
        companyShortName: data.company_short_name || '',
        companyWebsite: data.company_website || '',
        companyAddress: data.company_address || (data.company_province || '') + (data.company_city ? (data.company_province ? ' ' : '') + data.company_city : '') || '',
        jobTypeTag: getJobTypeText(data.job_type),
        isUrgent: data.is_urgent || false,
        isHighlight: data.is_highlight || false
      }
      isFavorite.value = data.is_favorited || false
      isApplied.value = data.has_applied || false
      similarJobs.value = data.similar_jobs || []
    }
  } catch (error) {
    console.error('获取岗位详情失败:', error)
  }
}

const toggleFavorite = async () => {
  const jobId = job.value.id || route.params.id
  if (!jobId) {
    ElMessage.error('岗位ID不存在')
    return
  }
  try {
    if (isFavorite.value) {
      await studentAPI.cancelCollect(jobId)
      isFavorite.value = false
      ElMessage.success('已取消收藏')
    } else {
      await studentAPI.collectJob(jobId)
      isFavorite.value = true
      ElMessage.success('已添加到收藏')
    }
  } catch (error) {
    ElMessage.error('操作失败，请重试')
  }
}

const handleApply = async () => {
  const jobId = job.value.id || route.params.id
  if (!jobId) {
    ElMessage.error('岗位ID不存在')
    return
  }
  if (isApplied.value) return
  try {
    await ElMessageBox.confirm('确定要投递该岗位吗？', '投递确认', {
      confirmButtonText: '确定投递',
      cancelButtonText: '取消',
      type: 'info'
    })
    await studentAPI.applyJob(jobId, {})
    isApplied.value = true
    ElMessage.success('投递成功')
  } catch (error) {
    if (error !== 'cancel') {
      if (error.response?.data?.detail === '您已投递过此岗位') {
        isApplied.value = true
        ElMessage.warning('您已投递过此岗位')
      } else {
        ElMessage.error('投递失败，请重试')
      }
    }
  }
}

onMounted(() => {
  fetchJobDetail()
})
</script>