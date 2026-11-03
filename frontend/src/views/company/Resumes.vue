<template>
  <div class="space-y-6">
    <div class="grid grid-cols-4 gap-6 mb-6">
      <div class="bg-white rounded-2xl p-6 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">收到简历</p>
            <p class="text-3xl font-bold text-gray-900 mt-1">{{ stats.total }}</p>
          </div>
          <div class="w-14 h-14 bg-purple-50 rounded-xl flex items-center justify-center">
            <i class="fas fa-inbox text-purple-500 text-2xl"></i>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-2xl p-6 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">待筛选</p>
            <p class="text-3xl font-bold text-gray-900 mt-1">{{ stats.pending }}</p>
          </div>
          <div class="w-14 h-14 bg-yellow-50 rounded-xl flex items-center justify-center">
            <i class="fas fa-clock text-yellow-500 text-2xl"></i>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-2xl p-6 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">已通过</p>
            <p class="text-3xl font-bold text-gray-900 mt-1">{{ stats.passed }}</p>
          </div>
          <div class="w-14 h-14 bg-green-50 rounded-xl flex items-center justify-center">
            <i class="fas fa-check-circle text-green-500 text-2xl"></i>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-2xl p-6 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">不合适</p>
            <p class="text-3xl font-bold text-gray-900 mt-1">{{ stats.rejected }}</p>
          </div>
          <div class="w-14 h-14 bg-gray-100 rounded-xl flex items-center justify-center">
            <i class="fas fa-user-times text-gray-500 text-2xl"></i>
          </div>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-2xl p-6 shadow-sm mb-6">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <div class="relative">
            <input v-model="searchQuery" type="text" placeholder="搜索姓名、学校..." class="w-80 pl-10 pr-4 py-2.5 bg-gray-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500">
            <i class="fas fa-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"></i>
          </div>
          <el-select v-model="filterStatus" class="w-36">
            <el-option label="全部状态" value="" />
            <el-option label="待筛选" value="pending" />
            <el-option label="已查看" value="viewed" />
            <el-option label="已通过" value="passed" />
            <el-option label="不合适" value="rejected" />
            <el-option label="录用" value="offered" />
          </el-select>
        </div>
        <el-button type="primary" @click="exportResumes">
          <i class="fas fa-download mr-2"></i>导出简历
        </el-button>
      </div>
    </div>

    <div class="bg-white rounded-2xl shadow-sm overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-4 text-left text-sm font-medium text-gray-500">简历信息</th>
            <th class="px-6 py-4 text-left text-sm font-medium text-gray-500">应聘岗位</th>
            <th class="px-6 py-4 text-left text-sm font-medium text-gray-500">学历</th>
            <th class="px-6 py-4 text-left text-sm font-medium text-gray-500">投递时间</th>
            <th class="px-6 py-4 text-left text-sm font-medium text-gray-500">状态</th>
            <th class="px-6 py-4 text-right text-sm font-medium text-gray-500">操作</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="resume in filteredResumes" :key="resume.id" class="hover:bg-gray-50">
            <td class="px-6 py-4">
              <div class="flex items-center space-x-4">
                <img :src="resume.avatar || `https://ui-avatars.com/api/?name=${encodeURIComponent(resume.student_name || '学生')}&background=6366f1&color=fff&size=48`" :alt="resume.student_name" class="w-12 h-12 rounded-full object-cover">
                <div>
                  <p class="font-medium text-gray-900">{{ resume.student_name }}</p>
                  <p class="text-sm text-gray-500">{{ resume.school }} · {{ resume.major || '-' }}</p>
                </div>
              </div>
            </td>
            <td class="px-6 py-4 text-gray-700">{{ resume.job_title }}</td>
            <td class="px-6 py-4 text-gray-700">{{ resume.education || '-' }}</td>
            <td class="px-6 py-4 text-gray-500 text-sm">{{ formatDate(resume.created_at) }}</td>
            <td class="px-6 py-4">
              <span :class="getStatusClass(resume.status)">{{ getStatusText(resume.status) }}</span>
            </td>
            <td class="px-6 py-4 text-right">
              <div class="flex items-center justify-end space-x-2">
                <button @click="viewResume(resume)" class="p-2 text-gray-500 hover:text-purple-600 hover:bg-purple-50 rounded-lg transition-colors">
                  <i class="fas fa-eye"></i>
                </button>
                <button @click="markResume(resume, 'passed')" class="p-2 text-gray-500 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors">
                  <i class="fas fa-check"></i>
                </button>
                <button @click="markResume(resume, 'rejected')" class="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors">
                  <i class="fas fa-times"></i>
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="filteredResumes.length === 0">
            <td colspan="6" class="px-6 py-8 text-center text-gray-500">暂无简历数据</td>
          </tr>
        </tbody>
      </table>
    </div>

    <el-dialog v-model="showResumeDialog" title="简历详情" width="700px">
      <div v-if="currentResume" class="space-y-4">
        <div class="flex items-center space-x-4 mb-6">
          <img :src="currentResume.avatar || `https://ui-avatars.com/api/?name=${encodeURIComponent(currentResume.student_name || '学生')}&background=6366f1&color=fff&size=80`" :alt="currentResume.student_name" class="w-20 h-20 rounded-full object-cover">
          <div>
            <h3 class="text-xl font-bold text-gray-900">{{ currentResume.student_name }}</h3>
            <p class="text-gray-500">{{ currentResume.school }} · {{ currentResume.major || '-' }}</p>
            <p class="text-gray-500">{{ currentResume.education || '-' }}</p>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="text-sm text-gray-500">应聘岗位</label>
            <p class="font-medium">{{ currentResume.job_title }}</p>
          </div>
          <div>
            <label class="text-sm text-gray-500">投递时间</label>
            <p class="font-medium">{{ formatDate(currentResume.created_at) }}</p>
          </div>
          <div>
            <label class="text-sm text-gray-500">联系电话</label>
            <p class="font-medium">{{ currentResume.phone || '-' }}</p>
          </div>
          <div>
            <label class="text-sm text-gray-500">邮箱</label>
            <p class="font-medium">{{ currentResume.email || '-' }}</p>
          </div>
        </div>
        <div v-if="currentResume.resume_url">
          <label class="text-sm text-gray-500">简历附件</label>
          <a :href="currentResume.resume_url" target="_blank" class="text-purple-600 hover:text-purple-700">
            <i class="fas fa-file-pdf mr-1"></i>查看简历
          </a>
        </div>
        <div v-if="currentResume.cover_letter">
          <label class="text-sm text-gray-500">求职信</label>
          <p class="text-gray-700 mt-1">{{ currentResume.cover_letter }}</p>
        </div>
      </div>
      <template #footer>
        <el-button @click="showResumeDialog = false">关闭</el-button>
        <el-button type="success" @click="markAndClose('passed')">标记为通过</el-button>
        <el-button type="danger" @click="markAndClose('rejected')">标记为不合适</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { companyAPI } from '@/api'

const searchQuery = ref('')
const filterStatus = ref('')
const loading = ref(false)
const showResumeDialog = ref(false)
const currentResume = ref(null)

const stats = ref({
  total: 0,
  pending: 0,
  passed: 0,
  rejected: 0
})

const resumes = ref([])

const filteredResumes = computed(() => {
  return resumes.value.filter(resume => {
    const matchesSearch = !searchQuery.value ||
      resume.student_name?.includes(searchQuery.value) ||
      resume.school?.includes(searchQuery.value) ||
      resume.job_title?.includes(searchQuery.value)
    const matchesStatus = !filterStatus.value || resume.status === filterStatus.value
    return matchesSearch && matchesStatus
  })
})

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('zh-CN')
}

const getStatusClass = (status) => {
  const map = {
    pending: 'px-3 py-1 bg-yellow-100 text-yellow-700 text-xs rounded-full',
    viewed: 'px-3 py-1 bg-blue-100 text-blue-700 text-xs rounded-full',
    passed: 'px-3 py-1 bg-green-100 text-green-700 text-xs rounded-full',
    rejected: 'px-3 py-1 bg-red-100 text-red-600 text-xs rounded-full',
    offered: 'px-3 py-1 bg-purple-100 text-purple-700 text-xs rounded-full'
  }
  return map[status] || ''
}

const getStatusText = (status) => {
  const map = {
    pending: '待筛选',
    viewed: '已查看',
    passed: '已通过',
    rejected: '不合适',
    offered: '录用'
  }
  return map[status] || status
}

const fetchResumes = async () => {
  loading.value = true
  try {
    const res = await companyAPI.getResumes()
    resumes.value = res.data || []

    stats.value = {
      total: resumes.value.length,
      pending: resumes.value.filter(r => r.status === 'pending').length,
      passed: resumes.value.filter(r => ['passed', 'offered'].includes(r.status)).length,
      rejected: resumes.value.filter(r => r.status === 'rejected').length
    }
  } catch (error) {
    console.error('获取简历列表失败:', error)
    ElMessage.error('获取简历列表失败')
  } finally {
    loading.value = false
  }
}

const viewResume = (resume) => {
  currentResume.value = resume
  showResumeDialog.value = true
}

const markResume = async (resume, status) => {
  try {
    await companyAPI.reviewApplication(resume.id, { status })
    ElMessage.success(status === 'passed' ? '已标记为通过' : '已标记为不合适')
    fetchResumes()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const markAndClose = async (status) => {
  if (currentResume.value) {
    await markResume(currentResume.value, status)
    showResumeDialog.value = false
  }
}

const exportResumes = () => {
  ElMessage.success('简历导出中...')
}

onMounted(() => {
  fetchResumes()
})
</script>