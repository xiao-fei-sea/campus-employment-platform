<template>
  <div class="max-w-3xl mx-auto">
    <div class="flex items-center space-x-4 mb-6">
      <button @click="goBack" class="p-2 hover:bg-gray-100 rounded-lg transition-colors">
        <i class="fas fa-arrow-left text-gray-600"></i>
      </button>
      <h1 class="text-2xl font-bold text-gray-900">{{ talk.title }}</h1>
    </div>

    <div class="card overflow-hidden mb-6 relative">
      <div v-if="talk.cover" class="w-full h-64 overflow-hidden">
        <img :src="talk.cover" @error="($event.target.parentElement.style.display='none')" class="w-full h-64 object-cover">
      </div>
      <div v-else-if="talk.companyLogo" class="w-full h-64 overflow-hidden">
        <img :src="talk.companyLogo" @error="($event.target.parentElement.style.display='none')" class="w-full h-64 object-cover opacity-80">
      </div>
      <div v-else class="w-full h-64 bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
        <span class="text-white text-3xl font-bold">{{ talk.companyName || '宣讲会' }}</span>
      </div>
      <div class="absolute top-4 left-4 flex space-x-2">
        <span v-if="talk.status === 'approved'" class="px-3 py-1 bg-emerald-500 text-white text-sm rounded-full">
          报名中
        </span>
        <span v-else class="px-3 py-1 bg-gray-500 text-white text-sm rounded-full">
          已结束
        </span>
      </div>
    </div>

    <div class="card p-6">
      <div class="flex items-center space-x-4 mb-6">
        <div v-if="talk.companyLogo" class="w-16 h-16 rounded-xl overflow-hidden">
          <img :src="talk.companyLogo" @error="talk.companyLogo = ''" class="w-full h-full object-cover">
        </div>
        <div v-else class="w-16 h-16 rounded-xl bg-blue-600 flex items-center justify-center text-white font-bold text-xl">
          {{ talk.companyName?.charAt(0) || '企' }}
        </div>
        <div>
          <h2 class="text-xl font-bold text-gray-900">{{ talk.companyName }}</h2>
          <p class="text-gray-500 text-sm">{{ talk.title }}</p>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-6 mb-6">
        <div class="flex items-center space-x-3">
          <div class="p-3 bg-blue-50 rounded-xl">
            <i class="fas fa-calendar-alt text-blue-600"></i>
          </div>
          <div>
            <p class="text-sm text-gray-500">举办日期</p>
            <p class="font-medium text-gray-900">{{ talk.date }}</p>
          </div>
        </div>
        <div class="flex items-center space-x-3">
          <div class="p-3 bg-green-50 rounded-xl">
            <i class="fas fa-clock text-green-600"></i>
          </div>
          <div>
            <p class="text-sm text-gray-500">活动时间</p>
            <p class="font-medium text-gray-900">{{ talk.time }}</p>
          </div>
        </div>
        <div class="flex items-center space-x-3">
          <div class="p-3 bg-purple-50 rounded-xl">
            <i class="fas fa-map-marker-alt text-purple-600"></i>
          </div>
          <div>
            <p class="text-sm text-gray-500">活动地点</p>
            <p class="font-medium text-gray-900">{{ talk.location }}</p>
          </div>
        </div>
        <div class="flex items-center space-x-3">
          <div class="p-3 bg-orange-50 rounded-xl">
            <i class="fas fa-users text-orange-600"></i>
          </div>
          <div>
            <p class="text-sm text-gray-500">报名人数</p>
            <p class="font-medium text-gray-900">{{ talk.currentAttendees }}/{{ talk.maxAttendees }}</p>
          </div>
        </div>
      </div>

      <div class="mb-6">
        <h3 class="font-bold text-gray-900 mb-3">活动介绍</h3>
        <p class="text-gray-600 leading-relaxed">{{ talk.description || '暂无介绍' }}</p>
      </div>

      <div class="mb-6">
        <h3 class="font-bold text-gray-900 mb-3">活动议程</h3>
        <div class="space-y-3">
          <div v-for="(agenda, index) in talk.agendas" :key="index" class="flex items-start space-x-3">
            <span class="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-sm font-medium">
              {{ index + 1 }}
            </span>
            <div>
              <p class="font-medium text-gray-900">{{ agenda.time }} - {{ agenda.title }}</p>
              <p class="text-sm text-gray-500">{{ agenda.description }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="flex items-center justify-between pt-4 border-t border-gray-100">
        <div class="flex items-center space-x-2">
          <span class="text-sm text-gray-500">{{ talk.currentAttendees }} 人已报名</span>
        </div>
        <el-button 
          v-if="talk.status === 'approved'" 
          :type="talk.isRegistered ? 'default' : 'primary'" 
          size="large" 
          @click="toggleRegister"
        >
          {{ talk.isRegistered ? '取消报名' : '立即报名' }}
        </el-button>
        <el-button v-else size="large" disabled>活动已结束</el-button>
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

const talk = ref({
  id: 0,
  companyName: '',
  companyLogo: '',
  title: '',
  cover: '',
  date: '',
  time: '',
  location: '',
  status: '',
  isRegistered: false,
  currentAttendees: 0,
  maxAttendees: 0,
  description: '',
  agendas: []
})

const goBack = () => {
  router.push('/student/career-talks')
}

const parseAgenda = (agendaStr) => {
  if (!agendaStr) return []
  try {
    return JSON.parse(agendaStr)
  } catch {
    return agendaStr.split('\n').filter(line => line.trim()).map((line, index) => {
      const parts = line.split('-')
      return {
        time: parts[0]?.trim() || `${9 + index * 30}:00`,
        title: parts.slice(1).join('-')?.trim() || '议程项目',
        description: ''
      }
    })
  }
}

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

const fetchTalkDetail = async () => {
  try {
    const res = await studentAPI.getCareerTalk(route.params.id)
    const data = res.data?.data || res.data
    if (data) {
      talk.value = {
        id: data.id,
        companyName: data.company_name || '',
        companyLogo: data.company_logo || '',
        title: data.title || '',
        cover: data.poster_url || '',
        date: formatDate(data.start_time),
        time: `${formatTime(data.start_time)} - ${formatTime(data.end_time)}`,
        location: data.location || '',
        status: data.status || '',
        isRegistered: data.is_registered || false,
        currentAttendees: data.current_attendees || 0,
        maxAttendees: data.max_attendees || 100,
        description: data.description || '',
        agendas: parseAgenda(data.agenda)
      }
    }
  } catch (error) {
    console.error('获取宣讲会详情失败:', error)
    ElMessage.error('获取宣讲会详情失败')
  }
}

const toggleRegister = async () => {
  try {
    if (talk.value.isRegistered) {
      await ElMessageBox.confirm('确定要取消报名吗？', '取消报名', {
        confirmButtonText: '确定取消',
        cancelButtonText: '取消',
        type: 'warning'
      })
      await studentAPI.cancelCareerTalk(talk.value.id)
      talk.value.isRegistered = false
      talk.value.currentAttendees = Math.max(0, talk.value.currentAttendees - 1)
      ElMessage.success('已取消报名')
    } else {
      await studentAPI.registerCareerTalk(talk.value.id)
      talk.value.isRegistered = true
      talk.value.currentAttendees += 1
      ElMessage.success('报名成功')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.detail || '操作失败，请重试')
    }
  }
}

onMounted(() => {
  fetchTalkDetail()
})
</script>