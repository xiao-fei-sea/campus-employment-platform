<template>
  <div class="space-y-6">
    <div class="grid grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-xl shadow-sm p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
            <i class="fas fa-briefcase text-blue-600 text-xl"></i>
          </div>
        </div>
        <p class="text-3xl font-bold text-gray-900 mb-1">{{ stats.total }}</p>
        <p class="text-gray-500 text-sm">全部岗位</p>
      </div>
      <div class="bg-white rounded-xl shadow-sm p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
            <i class="fas fa-check-circle text-green-600 text-xl"></i>
          </div>
        </div>
        <p class="text-3xl font-bold text-gray-900 mb-1">{{ stats.active }}</p>
        <p class="text-gray-500 text-sm">招聘中</p>
      </div>
      <div class="bg-white rounded-xl shadow-sm p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="w-12 h-12 bg-yellow-100 rounded-xl flex items-center justify-center">
            <i class="fas fa-pause-circle text-yellow-600 text-xl"></i>
          </div>
        </div>
        <p class="text-3xl font-bold text-gray-900 mb-1">{{ stats.paused }}</p>
        <p class="text-gray-500 text-sm">暂停招聘</p>
      </div>
      <div class="bg-white rounded-xl shadow-sm p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center">
            <i class="fas fa-times-circle text-purple-600 text-xl"></i>
          </div>
        </div>
        <p class="text-3xl font-bold text-gray-900 mb-1">{{ stats.offline }}</p>
        <p class="text-gray-500 text-sm">已下架</p>
      </div>
    </div>

    <div class="bg-white rounded-xl shadow-sm p-4 flex items-center justify-between">
      <div class="flex items-center space-x-4">
        <div class="relative">
          <input v-model="searchQuery" type="text" placeholder="搜索岗位名称..." class="w-64 pl-10 pr-4 py-2.5 bg-gray-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500">
          <i class="fas fa-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"></i>
        </div>
        <el-select v-model="filterStatus" class="w-36">
          <el-option label="全部状态" value="" />
          <el-option label="招聘中" value="approved" />
          <el-option label="待审核" value="pending" />
          <el-option label="已下架" value="closed" />
        </el-select>
      </div>
      <div class="flex space-x-2">
        <el-button @click="exportData">导出数据</el-button>
        <el-button type="primary" @click="openCreateDialog">发布新岗位</el-button>
      </div>
    </div>

    <div class="bg-white rounded-xl shadow-sm overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-4 text-left text-sm font-medium text-gray-500">岗位信息</th>
            <th class="px-6 py-4 text-left text-sm font-medium text-gray-500">薪资范围</th>
            <th class="px-6 py-4 text-left text-sm font-medium text-gray-500">简历</th>
            <th class="px-6 py-4 text-left text-sm font-medium text-gray-500">状态</th>
            <th class="px-6 py-4 text-left text-sm font-medium text-gray-500">发布时间</th>
            <th class="px-6 py-4 text-right text-sm font-medium text-gray-500">操作</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="job in filteredJobs" :key="job.id" class="hover:bg-gray-50 transition-colors">
            <td class="px-6 py-4">
              <div class="flex items-center space-x-4">
                <img :src="job.company?.logo || `https://ui-avatars.com/api/?name=${encodeURIComponent(job.company?.name || '企')}&background=6366f1&color=fff&size=48`" :alt="job.company?.name" class="w-12 h-12 rounded-xl object-cover">
                <div>
                  <p class="font-medium text-gray-900">{{ job.title }}</p>
                  <p class="text-sm text-gray-500">{{ job.province || job.city || '未知' }} · {{ formatEducation(job.education) }}</p>
                </div>
              </div>
            </td>
            <td class="px-6 py-4">
              <p class="font-medium text-gray-900">{{ job.salary_min / 1000 }}-{{ job.salary_max / 1000 }}K</p>
            </td>
            <td class="px-6 py-4">
              <div class="flex items-center space-x-4">
                <div class="text-center">
                  <p class="font-bold text-blue-600">{{ job.view_count }}</p>
                  <p class="text-xs text-gray-500">浏览</p>
                </div>
                <div class="text-center">
                  <p class="font-bold text-purple-600">{{ job.application_count || 0 }}</p>
                  <p class="text-xs text-gray-500">投递</p>
                </div>
                <div class="text-center">
                  <p class="font-bold text-emerald-600">{{ job.pending_count || 0 }}</p>
                  <p class="text-xs text-gray-500">待筛</p>
                </div>
              </div>
            </td>
            <td class="px-6 py-4">
              <span :class="getStatusClass(job.status)">{{ getStatusText(job.status) }}</span>
            </td>
            <td class="px-6 py-4">
              <p class="text-gray-600">{{ formatDate(job.created_at) }}</p>
            </td>
            <td class="px-6 py-4">
              <div class="flex items-center justify-end space-x-2">
                <button @click="editJob(job)" class="p-2 text-gray-400 hover:text-purple-600 hover:bg-purple-50 rounded-lg transition-colors">
                  <i class="fas fa-edit"></i>
                </button>
                <button @click="toggleJobStatus(job)" class="p-2 text-gray-400 hover:text-yellow-600 hover:bg-yellow-50 rounded-lg transition-colors">
                  <i :class="job.status === 'approved' ? 'fas fa-pause' : 'fas fa-play'"></i>
                </button>
                <button @click="deleteJob(job)" class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors">
                  <i class="fas fa-trash-alt"></i>
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="filteredJobs.length === 0">
            <td colspan="6" class="px-6 py-8 text-center text-gray-500">暂无岗位数据</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="flex justify-end mt-4">
      <el-pagination
        :current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next"
        @current-change="handlePageChange"
      />
    </div>

    <el-dialog v-model="showDialog" :title="isEditing ? '编辑岗位' : '发布岗位'" width="700px">
      <el-form :model="jobForm" label-position="top">
        <el-form-item label="岗位名称" required>
          <el-input v-model="jobForm.title" placeholder="请输入岗位名称" />
        </el-form-item>
        <div class="grid grid-cols-2 gap-4">
          <el-form-item label="最低薪资 (K)" required>
            <el-input-number v-model="jobForm.salary_min" :min="0" :step="1" class="w-full" />
          </el-form-item>
          <el-form-item label="最高薪资 (K)" required>
            <el-input-number v-model="jobForm.salary_max" :min="0" :step="1" class="w-full" />
          </el-form-item>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <el-form-item label="工作地点" required>
            <el-input v-model="jobForm.location" placeholder="请输入工作地点" />
          </el-form-item>
          <el-form-item label="学历要求">
            <el-select v-model="jobForm.education" class="w-full">
              <el-option label="不限" value="" />
              <el-option label="大专及以上" value="college" />
              <el-option label="本科及以上" value="bachelor" />
              <el-option label="硕士及以上" value="master" />
              <el-option label="博士及以上" value="doctor" />
            </el-select>
          </el-form-item>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <el-form-item label="工作经验">
            <el-input v-model="jobForm.experience" placeholder="如：1-3年" />
          </el-form-item>
          <el-form-item label="招聘人数">
            <el-input-number v-model="jobForm.headcount" :min="1" class="w-full" />
          </el-form-item>
        </div>
        <el-form-item label="岗位类型">
          <el-select v-model="jobForm.job_type" class="w-full">
            <el-option label="全职" value="full_time" />
            <el-option label="兼职" value="part_time" />
            <el-option label="实习" value="internship" />
            <el-option label="实训" value="practice" />
          </el-select>
        </el-form-item>
        <el-form-item label="岗位描述" required>
          <el-input v-model="jobForm.description" type="textarea" :rows="4" placeholder="请输入岗位描述" />
        </el-form-item>
        <el-form-item label="岗位要求">
          <el-input v-model="jobForm.requirements" type="textarea" :rows="3" placeholder="请输入岗位要求" />
        </el-form-item>
        <el-form-item label="福利标签">
          <el-input v-model="jobForm.benefits" placeholder="如：五险一金,年终奖,带薪年假" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="submitJob" :loading="submitting">{{ isEditing ? '保存' : '发布' }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { companyAPI } from '@/api'

const showDialog = ref(false)
const isEditing = ref(false)
const submitting = ref(false)
const searchQuery = ref('')
const filterStatus = ref('')
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const stats = ref({
  total: 0,
  active: 0,
  paused: 0,
  offline: 0
})

const jobForm = reactive({
  id: null,
  title: '',
  salary_min: 10,
  salary_max: 20,
  location: '',
  education: 'bachelor',
  experience: '',
  headcount: 1,
  job_type: 'full_time',
  description: '',
  requirements: '',
  benefits: ''
})

const jobs = ref([])

const filteredJobs = computed(() => {
  return jobs.value.filter(job => {
    const matchesSearch = !searchQuery.value || job.title.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesStatus = !filterStatus.value || job.status === filterStatus.value
    return matchesSearch && matchesStatus
  })
})

const formatEducation = (edu) => {
  const map = { college: '大专及以上', bachelor: '本科及以上', master: '硕士及以上', doctor: '博士及以上' }
  return map[edu] || edu || '不限'
}

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('zh-CN')
}

const getStatusClass = (status) => {
  const map = {
    pending: 'px-3 py-1 bg-yellow-100 text-yellow-700 text-sm rounded-full',
    approved: 'px-3 py-1 bg-green-100 text-green-700 text-sm rounded-full',
    draft: 'px-3 py-1 bg-gray-100 text-gray-700 text-sm rounded-full',
    rejected: 'px-3 py-1 bg-red-100 text-red-700 text-sm rounded-full',
    closed: 'px-3 py-1 bg-gray-100 text-gray-700 text-sm rounded-full'
  }
  return map[status] || ''
}

const getStatusText = (status) => {
  const map = {
    pending: '待审核',
    approved: '招聘中',
    draft: '草稿',
    rejected: '已拒绝',
    closed: '已下架'
  }
  return map[status] || status
}

const fetchJobs = async () => {
  loading.value = true
  try {
    const res = await companyAPI.getJobs({ page: currentPage.value, page_size: pageSize.value })
    jobs.value = res.data?.data || []
    total.value = res.data?.total || 0

    stats.value = {
      total: total.value,
      active: jobs.value.filter(j => j.status === 'approved').length,
      paused: jobs.value.filter(j => j.status === 'pending').length,
      offline: jobs.value.filter(j => j.status === 'closed').length
    }
  } catch (error) {
    console.error('获取岗位列表失败:', error)
    ElMessage.error('获取岗位列表失败')
  } finally {
    loading.value = false
  }
}

const handlePageChange = (page) => {
  currentPage.value = page
  fetchJobs()
}

const openCreateDialog = () => {
  isEditing.value = false
  Object.assign(jobForm, {
    id: null,
    title: '',
    salary_min: 10,
    salary_max: 20,
    location: '',
    education: 'bachelor',
    experience: '',
    headcount: 1,
    job_type: 'full_time',
    description: '',
    requirements: '',
    benefits: ''
  })
  showDialog.value = true
}

const editJob = (job) => {
  isEditing.value = true
  Object.assign(jobForm, {
    id: job.id,
    title: job.title,
    salary_min: job.salary_min / 1000,
    salary_max: job.salary_max / 1000,
    location: job.province || job.location || '',
    education: job.education || 'bachelor',
    experience: job.experience || '',
    headcount: job.headcount || 1,
    job_type: job.job_type || 'full_time',
    description: job.description || '',
    requirements: job.requirement || '',
    benefits: job.benefit || ''
  })
  showDialog.value = true
}

const submitJob = async () => {
  if (!jobForm.title || !jobForm.location) {
    ElMessage.warning('请填写必填项')
    return
  }

  submitting.value = true
  try {
    const data = {
      title: jobForm.title,
      salary_min: jobForm.salary_min * 1000,
      salary_max: jobForm.salary_max * 1000,
      province: jobForm.location,
      city: '',
      district: '',
      address: '',
      experience: jobForm.experience,
      education: jobForm.education,
      headcount: jobForm.headcount,
      job_type: jobForm.job_type,
      description: jobForm.description,
      requirement: jobForm.requirements,
      benefit: jobForm.benefits
    }

    if (isEditing.value) {
      await companyAPI.updateJob(jobForm.id, data)
      ElMessage.success('岗位已保存')
    } else {
      await companyAPI.createJob(data)
      ElMessage.success('岗位发布成功')
    }
    showDialog.value = false
    fetchJobs()
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error('操作失败')
  } finally {
    submitting.value = false
  }
}

const toggleJobStatus = async (job) => {
  try {
    const newStatus = job.status === 'approved' ? 'closed' : 'approved'
    await companyAPI.updateJob(job.id, { status: newStatus })
    ElMessage.success(`岗位已${newStatus === 'approved' ? '恢复招聘' : '暂停'}`)
    fetchJobs()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const deleteJob = async (job) => {
  try {
    await ElMessageBox.confirm('确定删除该岗位吗？', '提示', { type: 'warning' })
    await companyAPI.deleteJob(job.id)
    ElMessage.success('删除成功')
    fetchJobs()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const exportData = () => {
  ElMessage.success('数据导出中...')
}

onMounted(() => {
  fetchJobs()
})
</script>