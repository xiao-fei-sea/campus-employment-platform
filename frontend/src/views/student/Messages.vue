<template>
  <div class="bg-white rounded-lg shadow-sm">
    <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200">
      <div>
        <h2 class="text-lg font-bold text-gray-900">消息中心</h2>
        <p class="text-sm text-gray-500 mt-1">共 {{ total }} 条消息，{{ unreadCount }} 条未读</p>
      </div>
      <div class="flex items-center space-x-3">
        <el-radio-group v-model="filter" size="small" @change="loadMessages">
          <el-radio-button label="all">全部</el-radio-button>
          <el-radio-button label="unread">未读</el-radio-button>
          <el-radio-button label="application">投递反馈</el-radio-button>
          <el-radio-button label="system">系统通知</el-radio-button>
        </el-radio-group>
        <el-button size="small" :disabled="unreadCount === 0" @click="markAllRead">全部已读</el-button>
      </div>
    </div>

    <div v-if="loading" class="py-16 text-center text-gray-400">加载中...</div>

    <div v-else-if="messages.length === 0" class="py-16 text-center text-gray-400">
      <i class="fas fa-bell-slash text-4xl mb-3"></i>
      <p>暂无消息</p>
    </div>

    <div v-else class="divide-y divide-gray-100">
      <div
        v-for="msg in messages"
        :key="msg.id"
        @click="openMessage(msg)"
        class="px-6 py-4 flex items-start space-x-4 cursor-pointer hover:bg-gray-50 transition-colors"
        :class="{ 'bg-emerald-50/50': !msg.is_read }"
      >
        <div
          class="w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0"
          :class="iconClass(msg.type)"
        >
          <i :class="iconName(msg.type)"></i>
        </div>
        <div class="flex-1 min-w-0">
          <div class="flex items-center justify-between">
            <span class="font-medium text-gray-900" :class="{ 'font-bold': !msg.is_read }">{{ msg.title }}</span>
            <span class="text-xs text-gray-400">{{ msg.created_at ? formatTime(msg.created_at) : '' }}</span>
          </div>
          <p class="text-sm text-gray-500 mt-1 truncate">{{ msg.content }}</p>
        </div>
        <el-button v-if="msg.is_read" text size="small" @click.stop="removeMessage(msg)">
          <i class="fas fa-trash text-gray-400"></i>
        </el-button>
        <span v-else class="w-2 h-2 bg-red-500 rounded-full mt-2"></span>
      </div>
    </div>

    <div v-if="total > pageSize" class="px-6 py-4 flex justify-end border-t border-gray-100">
      <el-pagination
        v-model:current-page="page"
        :page-size="pageSize"
        :total="total"
        layout="prev, pager, next"
        @current-change="loadMessages"
      />
    </div>

    <el-dialog v-model="detailVisible" title="消息详情" width="520px">
      <div class="space-y-2">
        <h3 class="text-base font-bold text-gray-900">{{ currentMessage.title }}</h3>
        <p class="text-xs text-gray-400">{{ currentMessage.created_at ? formatTime(currentMessage.created_at) : '' }}</p>
        <p class="text-sm text-gray-600 leading-relaxed whitespace-pre-wrap">{{ currentMessage.content }}</p>
      </div>
      <template #footer>
        <el-button @click="detailVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { studentAPI } from '@/api'

const messages = ref([])
const total = ref(0)
const unreadCount = ref(0)
const loading = ref(false)
const filter = ref('all')
const page = ref(1)
const pageSize = ref(20)
const detailVisible = ref(false)
const currentMessage = ref({})

const iconName = (type) => {
  if (type === 'application') return 'fas fa-file-alt'
  if (type === 'activity') return 'fas fa-calendar-alt'
  return 'fas fa-bullhorn'
}

const iconClass = (type) => {
  if (type === 'application') return 'bg-blue-100 text-blue-600'
  if (type === 'activity') return 'bg-amber-100 text-amber-600'
  return 'bg-emerald-100 text-emerald-600'
}

const formatTime = (value) => {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleString('zh-CN', { hour12: false })
}

const loadUnreadCount = async () => {
  try {
    const res = await studentAPI.getUnreadMessageCount()
    unreadCount.value = res.data.count
  } catch (error) {
    console.error('加载未读消息数失败', error)
  }
}

const loadMessages = async () => {
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize.value }
    if (filter.value === 'unread') {
      params.is_read = false
    } else if (filter.value !== 'all') {
      params.type = filter.value
    }
    const res = await studentAPI.getMessages(params)
    messages.value = res.data.data
    total.value = res.data.total
    await loadUnreadCount()
  } catch (error) {
    console.error('加载消息失败', error)
    ElMessage.error('加载消息失败')
  } finally {
    loading.value = false
  }
}

const openMessage = async (msg) => {
  currentMessage.value = msg
  detailVisible.value = true
  if (!msg.is_read) {
    try {
      await studentAPI.markMessageRead(msg.id)
      msg.is_read = true
      await loadUnreadCount()
    } catch (error) {
      console.error('标记已读失败', error)
    }
  }
}

const markAllRead = async () => {
  try {
    await studentAPI.markAllMessagesRead()
    ElMessage.success('已全部标为已读')
    await loadMessages()
  } catch (error) {
    console.error('全部已读失败', error)
    ElMessage.error('操作失败')
  }
}

const removeMessage = async (msg) => {
  try {
    await ElMessageBox.confirm('确定删除这条消息吗？', '提示', { type: 'warning' })
    await studentAPI.deleteMessage(msg.id)
    ElMessage.success('删除成功')
    await loadMessages()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除消息失败', error)
      ElMessage.error('删除失败')
    }
  }
}

onMounted(loadMessages)
</script>
