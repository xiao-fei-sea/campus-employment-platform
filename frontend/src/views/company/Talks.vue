<template>
  <div class="space-y-6">
    <div class="grid grid-cols-4 gap-6 mb-6">
      <div class="bg-white rounded-2xl p-6 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">总场次</p>
            <p class="text-3xl font-bold text-gray-900 mt-1">{{ stats.total }}</p>
          </div>
          <div class="w-14 h-14 bg-purple-50 rounded-xl flex items-center justify-center">
            <i class="fas fa-calendar text-purple-500 text-2xl"></i>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-2xl p-6 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">进行中</p>
            <p class="text-3xl font-bold text-green-600 mt-1">{{ stats.active }}</p>
          </div>
          <div class="w-14 h-14 bg-green-50 rounded-xl flex items-center justify-center">
            <i class="fas fa-play text-green-500 text-2xl"></i>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-2xl p-6 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">报名人数</p>
            <p class="text-3xl font-bold text-gray-900 mt-1">{{ stats.registered }}</p>
          </div>
          <div class="w-14 h-14 bg-blue-50 rounded-xl flex items-center justify-center">
            <i class="fas fa-users text-blue-500 text-2xl"></i>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-2xl p-6 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">签到率</p>
            <p class="text-3xl font-bold text-gray-900 mt-1">{{ stats.checkinRate }}%</p>
          </div>
          <div class="w-14 h-14 bg-yellow-50 rounded-xl flex items-center justify-center">
            <i class="fas fa-clipboard-check text-yellow-500 text-2xl"></i>
          </div>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-2xl p-6 shadow-sm mb-6">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <button v-for="tab in tabs" :key="tab.value" :class="activeTab === tab.value ? 'bg-purple-600 text-white' : 'text-gray-600 hover:bg-gray-100'" class="px-4 py-2 rounded-xl transition-colors" @click="activeTab = tab.value">
            {{ tab.label }}
          </button>
        </div>
        <div class="flex items-center space-x-4">
          <div class="relative">
            <input v-model="searchQuery" type="text" placeholder="搜索宣讲会..." class="w-64 pl-10 pr-4 py-2.5 bg-gray-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500">
            <i class="fas fa-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"></i>
          </div>
          <el-button type="primary" @click="openCreateDialog">发布宣讲会</el-button>
        </div>
      </div>
    </div>

    <div class="space-y-4">
      <div v-for="talk in filteredTalks" :key="talk.id" class="bg-white rounded-2xl p-6 shadow-sm">
        <div class="flex items-start justify-between">
          <div class="flex items-start space-x-4">
            <div :class="getTalkIconBg(talk.status)" class="w-16 h-16 rounded-xl flex items-center justify-center">
              <i :class="getTalkIcon(talk.status)" class="text-white text-2xl"></i>
            </div>
            <div class="flex-1">
              <div class="flex items-center space-x-3 mb-2">
                <h3 class="text-lg font-bold text-gray-900">{{ talk.title }}</h3>
                <span :class="getTalkStatusClass(talk.status)">{{ getTalkStatusText(talk.status) }}</span>
              </div>
              <div class="flex items-center space-x-6 text-sm text-gray-500 mb-3">
                <span><i class="fas fa-clock mr-1"></i>{{ formatDateTime(talk.start_time || talk.scheduled_at) }}</span>
                <span v-if="talk.location"><i class="fas fa-map-marker-alt mr-1"></i>{{ talk.location }}</span>
                <span><i class="fas fa-users mr-1"></i>已报名 {{ talk.registration_count || 0 }} 人</span>
              </div>
            </div>
          </div>
          <div class="flex flex-col items-end space-y-3">
            <div class="flex items-center space-x-2">
              <button @click="viewTalk(talk)" class="p-2 text-gray-500 hover:text-purple-600 hover:bg-purple-50 rounded-lg transition-colors">
                <i class="fas fa-eye"></i>
              </button>
              <button @click="editTalk(talk)" class="p-2 text-gray-500 hover:text-purple-600 hover:bg-purple-50 rounded-lg transition-colors">
                <i class="fas fa-edit"></i>
              </button>
              <button @click="deleteTalk(talk)" class="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors">
                <i class="fas fa-trash-alt"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
      <div v-if="filteredTalks.length === 0" class="bg-white rounded-2xl p-8 text-center text-gray-500">
        暂无宣讲会数据
      </div>
    </div>

    <el-dialog v-model="showDialog" :title="isEditing ? '编辑宣讲会' : '发布宣讲会'" width="600px">
      <el-form :model="talkForm" label-position="top">
        <el-form-item label="宣讲会标题" required>
          <el-input v-model="talkForm.title" placeholder="请输入宣讲会标题" />
        </el-form-item>
        <div class="grid grid-cols-2 gap-4">
          <el-form-item label="开始时间" required>
            <el-date-picker v-model="talkForm.start_time" type="datetime" class="w-full" placeholder="选择开始时间" format="YYYY-MM-DD HH:mm:ss" value-format="YYYY-MM-DDTHH:mm:ss" />
          </el-form-item>
          <el-form-item label="宣讲地点" required>
            <el-input v-model="talkForm.location" placeholder="请输入宣讲地点" />
          </el-form-item>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <el-form-item label="结束时间" required>
            <el-date-picker v-model="talkForm.end_time" type="datetime" class="w-full" placeholder="选择结束时间" format="YYYY-MM-DD HH:mm:ss" value-format="YYYY-MM-DDTHH:mm:ss" />
          </el-form-item>
        </div>
        <el-form-item label="宣讲内容">
          <el-input v-model="talkForm.description" type="textarea" :rows="4" placeholder="请输入宣讲内容" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="submitTalk" :loading="submitting">{{ isEditing ? '保存' : '发布' }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { companyAPI } from '@/api'

const showDialog = ref(false)
const isEditing = ref(false)
const submitting = ref(false)
const searchQuery = ref('')
const activeTab = ref('all')
const loading = ref(false)

const tabs = [
  { label: '全部', value: 'all' },
  { label: '待审核', value: 'pending' },
  { label: '已通过', value: 'approved' },
  { label: '已结束', value: 'ended' }
]

const stats = ref({
  total: 0,
  active: 0,
  registered: 0,
  checkinRate: 0
})

const talkForm = ref({
  id: null,
  title: '',
  start_time: '',
  end_time: '',
  location: '',
  description: ''
})

const talks = ref([])

const filteredTalks = computed(() => {
  return talks.value.filter(talk => {
    if (talk.status === 'cancelled') return false
    const matchesSearch = !searchQuery.value || talk.title.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesTab = activeTab.value === 'all' || talk.status === activeTab.value
    return matchesSearch && matchesTab
  })
})

const formatDateTime = (datetime) => {
  if (!datetime) return '-'
  return new Date(datetime).toLocaleString('zh-CN')
}

const getTalkStatusClass = (status) => {
  const map = {
    draft: 'px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded-full',
    pending: 'px-2 py-0.5 bg-yellow-100 text-yellow-700 text-xs rounded-full',
    approved: 'px-2 py-0.5 bg-green-100 text-green-700 text-xs rounded-full',
    rejected: 'px-2 py-0.5 bg-red-100 text-red-600 text-xs rounded-full',
    cancelled: 'px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded-full',
    ended: 'px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded-full'
  }
  return map[status] || ''
}

const getTalkStatusText = (status) => {
  const map = {
    draft: '草稿',
    pending: '待审核',
    approved: '已通过',
    rejected: '已拒绝',
    cancelled: '已取消',
    ended: '已结束'
  }
  return map[status] || status
}

const getTalkIcon = (status) => {
  const map = {
    live: 'fas fa-video',
    upcoming: 'fas fa-clock',
    ended: 'fas fa-video-slash'
  }
  return map[status] || 'fas fa-calendar'
}

const getTalkIconBg = (status) => {
  const map = {
    live: 'bg-gradient-to-br from-green-500 to-emerald-500',
    upcoming: 'bg-gradient-to-br from-yellow-500 to-orange-500',
    ended: 'bg-gradient-to-br from-gray-400 to-gray-500'
  }
  return map[status] || 'bg-gradient-to-br from-purple-500 to-indigo-500'
}

const fetchTalks = async () => {
  loading.value = true
  try {
    const res = await companyAPI.getTalks()
    talks.value = res.data || []

    stats.value = {
      total: talks.value.length,
      active: talks.value.filter(t => t.status === 'live' || t.status === 'upcoming').length,
      registered: talks.value.reduce((sum, t) => sum + (t.registration_count || 0), 0),
      checkinRate: 0
    }
  } catch (error) {
    console.error('获取宣讲会列表失败:', error)
    ElMessage.error('获取宣讲会列表失败')
  } finally {
    loading.value = false
  }
}

const openCreateDialog = () => {
  isEditing.value = false
  talkForm.value = {
    id: null,
    title: '',
    start_time: '',
    end_time: '',
    location: '',
    description: ''
  }
  showDialog.value = true
}

const viewTalk = (talk) => {
  ElMessage.info('查看宣讲会：' + talk.title)
}

const editTalk = (talk) => {
  isEditing.value = true
  talkForm.value = {
    id: talk.id,
    title: talk.title,
    start_time: talk.start_time || talk.scheduled_at,
    end_time: talk.end_time,
    location: talk.location || '',
    description: talk.description || ''
  }
  showDialog.value = true
}

const submitTalk = async () => {
  if (!talkForm.value.title || !talkForm.value.start_time || !talkForm.value.end_time || !talkForm.value.location) {
    ElMessage.warning('请填写必填项')
    return
  }

  submitting.value = true
  try {
    const data = { ...talkForm.value }
    if (isEditing.value) {
      await companyAPI.updateTalk(talkForm.value.id, data)
      ElMessage.success('宣讲会已保存')
    } else {
      await companyAPI.createTalk(data)
      ElMessage.success('宣讲会发布成功')
    }
    showDialog.value = false
    fetchTalks()
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error('操作失败')
  } finally {
    submitting.value = false
  }
}

const deleteTalk = async (talk) => {
  try {
    await ElMessageBox.confirm('确定删除该宣讲会吗？', '提示', { type: 'warning' })
    await companyAPI.deleteTalk(talk.id)
    ElMessage.success('删除成功')
    fetchTalks()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  fetchTalks()
})
</script>