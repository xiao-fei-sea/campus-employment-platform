<template>
  <div class="p-8">
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-900">我的收藏</h2>
      <p class="text-gray-500 mt-1">收藏感兴趣的岗位，方便随时查看和投递</p>
    </div>

    <div class="grid grid-cols-3 gap-6 mb-8">
      <div class="bg-white rounded-2xl p-6 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">收藏总数</p>
            <p class="text-3xl font-bold text-gray-900 mt-1">{{ stats.total }}</p>
          </div>
          <div class="w-14 h-14 bg-yellow-50 rounded-xl flex items-center justify-center">
            <i class="fas fa-star text-yellow-500 text-2xl"></i>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-2xl p-6 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">已投递</p>
            <p class="text-3xl font-bold text-gray-900 mt-1">{{ stats.applied }}</p>
          </div>
          <div class="w-14 h-14 bg-green-50 rounded-xl flex items-center justify-center">
            <i class="fas fa-paper-plane text-green-500 text-2xl"></i>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-2xl p-6 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">等待回复</p>
            <p class="text-3xl font-bold text-gray-900 mt-1">{{ stats.waiting }}</p>
          </div>
          <div class="w-14 h-14 bg-blue-50 rounded-xl flex items-center justify-center">
            <i class="fas fa-clock text-blue-500 text-2xl"></i>
          </div>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-2xl shadow-sm mb-6">
      <div class="flex border-b border-gray-100">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          @click="activeTab = tab.key"
          :class="[
            'px-6 py-4 transition-colors',
            activeTab === tab.key
              ? 'text-blue-600 border-b-2 border-blue-600 font-medium'
              : 'text-gray-500 hover:text-gray-700'
          ]"
        >
          {{ tab.label }} ({{ tab.count }})
        </button>
      </div>
    </div>

    <div class="space-y-4">
      <div
        v-for="job in filteredJobs"
        :key="job.id"
        class="bg-white rounded-2xl p-6 shadow-sm hover:shadow-md transition-all"
      >
        <div class="flex items-start justify-between">
          <div class="flex items-start space-x-4">
            <div v-if="job.logo" class="w-16 h-16 rounded-xl object-cover overflow-hidden">
              <img :src="job.logo" @error="job.logo = ''" class="w-full h-full object-cover">
            </div>
            <div v-else class="w-16 h-16 rounded-xl bg-blue-600 flex items-center justify-center text-white font-bold text-xl">
              {{ job.company?.charAt(0) || '企' }}
            </div>
            <div>
              <div class="flex items-center space-x-3 mb-1">
                <router-link :to="`/student/jobs/${job.id}`" class="text-lg font-bold text-gray-900 hover:text-blue-600">
                  {{ job.title }}
                </router-link>
                <span :class="[job.isApplied ? 'bg-green-100 text-green-700' : 'bg-blue-100 text-blue-700', 'px-2 py-0.5 text-xs rounded-full']">
                  {{ job.isApplied ? '已投递' : '未投递' }}
                </span>
              </div>
              <p class="text-gray-600 mb-2">{{ job.company }}</p>
              <div class="flex items-center space-x-4 text-sm text-gray-500">
                <span><i class="fas fa-map-marker-alt mr-1"></i>{{ job.location }}</span>
                <span><i class="fas fa-money-bill mr-1"></i>{{ job.salary }}</span>
                <span><i class="fas fa-clock mr-1"></i>{{ job.favoriteDaysAgo }}</span>
              </div>
              <div class="flex items-center space-x-2 mt-3">
                <span v-for="skill in job.skills" :key="skill" class="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded">
                  {{ skill }}
                </span>
              </div>
            </div>
          </div>
          <div class="flex flex-col items-end space-y-3">
            <button @click="toggleFavorite(job.id)" class="text-gray-400 hover:text-yellow-500 transition-colors">
              <i class="fas fa-star text-xl text-yellow-500"></i>
            </button>
            <button
              v-if="!job.isApplied"
              @click="applyJob(job.id)"
              class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded-xl transition-colors"
            >
              投递简历
            </button>
            <button
              v-else
              @click="viewApplication(job.id)"
              class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white text-sm rounded-xl transition-colors"
            >
              查看投递
            </button>
          </div>
        </div>
      </div>

      <div v-if="filteredJobs.length === 0" class="text-center py-12">
        <i class="fas fa-star text-gray-300 text-5xl mb-4"></i>
        <p class="text-gray-500">暂无收藏的岗位</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { studentAPI } from '@/api'

const activeTab = ref('all')
const loading = ref(false)

const tabs = ref([
  { key: 'all', label: '全部收藏', count: 0 },
  { key: 'applied', label: '已投递', count: 0 },
  { key: 'unapplied', label: '未投递', count: 0 }
])

const stats = ref({
  total: 0,
  applied: 0,
  waiting: 0
})

const jobs = ref([])

const fetchFavorites = async () => {
  try {
    loading.value = true
    const res = await studentAPI.getFavorites({ page: 1, page_size: 100 })
    const favoriteList = res.data?.data || res.data || []
    jobs.value = favoriteList.map(job => ({
      id: job.id,
      title: job.title,
      company: job.company_name,
      logo: job.company_logo || '/placeholder-logo.png',
      salary: job.salary_show || `${(job.salary_min || 0) / 1000}-${(job.salary_max || 0) / 1000}K`,
      location: job.city || job.province || '未知',
      favoriteDaysAgo: getFavoriteDaysAgo(job.favorited_at),
      isApplied: job.has_applied || false,
      skills: job.skills ? job.skills.split(',').slice(0, 4) : []
    }))

    stats.value.total = jobs.value.length
    stats.value.applied = jobs.value.filter(j => j.isApplied).length
    stats.value.waiting = jobs.value.filter(j => !j.isApplied).length

    tabs.value = [
      { key: 'all', label: '全部收藏', count: stats.value.total },
      { key: 'applied', label: '已投递', count: stats.value.applied },
      { key: 'unapplied', label: '未投递', count: stats.value.waiting }
    ]
  } catch (error) {
    console.error('获取收藏列表失败:', error)
    jobs.value = []
  } finally {
    loading.value = false
  }
}

const getFavoriteDaysAgo = (dateStr) => {
  if (!dateStr) return '最近收藏'
  const date = new Date(dateStr)
  const now = new Date()
  const diff = Math.floor((now - date) / (1000 * 60 * 60 * 24))
  if (diff === 0) return '今天收藏'
  if (diff === 1) return '1天前收藏'
  if (diff < 7) return `${diff}天前收藏`
  if (diff < 30) return `${Math.floor(diff / 7)}周前收藏`
  return `${Math.floor(diff / 30)}月前收藏`
}

const filteredJobs = computed(() => {
  if (activeTab.value === 'all') return jobs.value
  if (activeTab.value === 'applied') return jobs.value.filter(job => job.isApplied)
  return jobs.value.filter(job => !job.isApplied)
})

const applyJob = async (id) => {
  try {
    await studentAPI.applyJob(id, {})
    const job = jobs.value.find(j => j.id === id)
    if (job) job.isApplied = true
    ElMessage.success('投递成功')
    fetchFavorites()
  } catch (error) {
    ElMessage.error('投递失败，请重试')
  }
}

const viewApplication = (id) => {
  ElMessage.info('查看投递详情')
}

const toggleFavorite = async (id) => {
  try {
    await ElMessageBox.confirm('确定要取消收藏该岗位吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await studentAPI.cancelCollect(id)
    ElMessage.success('已取消收藏')
    fetchFavorites()
  } catch {
    // Cancelled
  }
}

onMounted(() => {
  fetchFavorites()
})
</script>
