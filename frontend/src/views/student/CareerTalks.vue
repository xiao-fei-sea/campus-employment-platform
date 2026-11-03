<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <el-select v-model="filterStatus" class="w-40">
        <el-option label="全部" value="all" />
        <el-option label="报名中" value="approved" />
        <el-option label="已结束" value="ended" />
      </el-select>
      <div class="flex items-center space-x-4">
        <el-input v-model="searchKeyword" placeholder="搜索宣讲会名称" class="w-64" clearable @keyup.enter="handleSearch" />
        <el-button type="primary" @click="handleSearch">搜索宣讲会</el-button>
      </div>
    </div>

    <div class="grid grid-cols-3 gap-6">
      <div v-for="talk in filteredTalks" :key="talk.id" class="card overflow-hidden cursor-pointer hover:shadow-lg transition-shadow" @click="goToDetail(talk.id)">
        <div class="relative">
          <div v-if="talk.cover" class="w-full h-40 overflow-hidden">
            <img :src="talk.cover" @error="($event.target.parentElement.style.display='none')" class="w-full h-40 object-cover">
          </div>
          <div v-else-if="talk.logo" class="w-full h-40 overflow-hidden">
            <img :src="talk.logo" @error="($event.target.parentElement.style.display='none')" class="w-full h-40 object-cover opacity-80">
          </div>
          <div v-else class="w-full h-40 bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center px-4">
            <span class="text-white text-xl font-bold text-center truncate">{{ talk.companyName || '宣讲会' }}</span>
          </div>
          <div class="absolute top-3 right-3 flex space-x-2">
            <span v-if="talk.status === 'approved'" class="px-2 py-1 bg-emerald-500 text-white text-xs rounded">
              报名中
            </span>
            <span v-else class="px-2 py-1 bg-gray-500 text-white text-xs rounded">
              已结束
            </span>
          </div>
        </div>
        <div class="p-4">
          <h3 class="font-bold text-gray-900">{{ talk.companyName }}</h3>
          <p class="text-gray-500 text-sm mt-1">{{ talk.title }}</p>
          <div class="mt-4 space-y-2 text-sm text-gray-600">
            <p><i class="far fa-calendar mr-2"></i>{{ talk.date }}</p>
            <p><i class="far fa-clock mr-2"></i>{{ talk.time }}</p>
            <p><i class="fas fa-map-marker-alt mr-2"></i>{{ talk.location }}</p>
          </div>
          <div class="flex items-center justify-between mt-4">
            <div class="flex items-center space-x-2">
              <span class="text-xs text-gray-500">{{ talk.currentAttendees }}人已报名</span>
            </div>
            <el-button v-if="talk.status === 'approved'" type="primary" size="small" @click.stop="register(talk.id)">
              {{ talk.isRegistered ? '已报名' : '立即报名' }}
            </el-button>
            <el-button v-else size="small" disabled>查看回放</el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'
import { studentAPI } from '@/api'

const router = useRouter()

const searchKeyword = ref('')
const goToDetail = (id) => {
  router.push(`/student/career-talks/${id}`)
}

const filterStatus = ref('all')

const talks = ref([])

const handleSearch = () => {
  fetchTalks()
}

const filteredTalks = computed(() => {
  let result = talks.value
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    result = result.filter(t => t.companyName.toLowerCase().includes(keyword) || t.title.toLowerCase().includes(keyword))
  }
  if (filterStatus.value !== 'all') {
    result = result.filter(t => t.status === filterStatus.value)
  }
  return result
})

const formatDate = (dateStr) => {
  if (!dateStr) return '暂无'
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' })
}

const formatTime = (dateStr) => {
  if (!dateStr) return '暂无'
  const date = new Date(dateStr)
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

const fetchTalks = async () => {
  try {
    const res = await studentAPI.getCareerTalks()
    const data = res.data?.data || res.data
    talks.value = data.map(talk => ({
      id: talk.id,
      companyName: talk.company_name || '',
      title: talk.title || '',
      cover: talk.poster_url || '',
      logo: talk.company_logo || '',
      date: formatDate(talk.start_time),
      time: `${formatTime(talk.start_time)} - ${formatTime(talk.end_time)}`,
      location: talk.location || '',
      status: talk.status || '',
      isRegistered: talk.is_registered || false,
      currentAttendees: talk.current_attendees || 0
    }))
  } catch (error) {
    console.error('获取宣讲会列表失败:', error)
    ElMessage.error('获取宣讲会列表失败')
  }
}

const register = async (id) => {
  const talk = talks.value.find(t => t.id === id)
  if (!talk) return
  
  try {
    if (talk.isRegistered) {
      await ElMessageBox.confirm('确定要取消报名吗？', '取消报名', {
        confirmButtonText: '确定取消',
        cancelButtonText: '取消',
        type: 'warning'
      })
      await studentAPI.cancelCareerTalk(id)
      talk.isRegistered = false
      talk.currentAttendees = Math.max(0, talk.currentAttendees - 1)
      ElMessage.success('已取消报名')
    } else {
      await studentAPI.registerCareerTalk(id)
      talk.isRegistered = true
      talk.currentAttendees += 1
      ElMessage.success('报名成功')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.detail || '操作失败，请重试')
    }
  }
}

onMounted(() => {
  fetchTalks()
})
</script>