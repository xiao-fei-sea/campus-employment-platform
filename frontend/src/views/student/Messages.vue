<template>
  <div class="flex h-[calc(100vh-140px)]">
    <!-- Conversation List -->
    <div class="w-80 bg-white border-r border-gray-200 flex flex-col">
      <div class="p-4 border-b border-gray-200">
        <el-input v-model="searchKeyword" placeholder="搜索消息" prefix-icon="Search" />
      </div>
      <div class="flex-1 overflow-y-auto">
        <div
          v-for="conv in conversations"
          :key="conv.id"
          @click="selectConversation(conv.id)"
          class="p-4 border-b border-gray-100 cursor-pointer hover:bg-gray-50 transition-colors"
          :class="{ 'bg-emerald-50': selectedId === conv.id }"
        >
          <div class="flex items-center space-x-3">
            <img :src="conv.avatar" class="w-12 h-12 rounded-full">
            <div class="flex-1 min-w-0">
              <div class="flex items-center justify-between">
                <span class="font-medium text-gray-900">{{ conv.name }}</span>
                <span class="text-xs text-gray-400">{{ conv.time }}</span>
              </div>
              <p class="text-sm text-gray-500 truncate mt-1">{{ conv.lastMessage }}</p>
            </div>
            <span v-if="conv.unread" class="w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
              {{ conv.unread }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Chat Area -->
    <div class="flex-1 flex flex-col bg-gray-50">
      <template v-if="selectedConversation">
        <!-- Chat Header -->
        <div class="p-4 bg-white border-b border-gray-200 flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <img :src="selectedConversation.avatar" class="w-10 h-10 rounded-full">
            <div>
              <p class="font-medium text-gray-900">{{ selectedConversation.name }}</p>
              <p class="text-xs text-gray-500">{{ selectedConversation.company }}</p>
            </div>
          </div>
          <el-button>查看简历</el-button>
        </div>

        <!-- Messages -->
        <div class="flex-1 overflow-y-auto p-4 space-y-4">
          <div v-for="msg in messages" :key="msg.id" :class="msg.isMine ? 'flex justify-end' : 'flex'">
            <div class="max-w-md" :class="msg.isMine ? 'order-2' : 'order-1'">
              <div
                class="px-4 py-3 rounded-2xl"
                :class="msg.isMine ? 'bg-emerald-600 text-white rounded-tr-sm' : 'bg-white text-gray-900 rounded-tl-sm'"
              >
                <p>{{ msg.content }}</p>
              </div>
              <p class="text-xs text-gray-400 mt-1" :class="msg.isMine ? 'text-right' : ''">{{ msg.time }}</p>
            </div>
          </div>
        </div>

        <!-- Input -->
        <div class="p-4 bg-white border-t border-gray-200">
          <div class="flex items-center space-x-3">
            <el-input v-model="inputMessage" placeholder="输入消息..." @keyup.enter="sendMessage" />
            <el-button type="primary" @click="sendMessage">发送</el-button>
          </div>
        </div>
      </template>

      <div v-else class="flex-1 flex items-center justify-center text-gray-400">
        <div class="text-center">
          <i class="fas fa-comments text-6xl mb-4"></i>
          <p>选择会话开始聊天</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'

const searchKeyword = ref('')
const selectedId = ref(1)
const inputMessage = ref('')

const conversations = ref([
  {
    id: 1,
    name: '字节跳动HR-李经理',
    avatar: 'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=100&h=100&fit=crop&crop=face',
    company: '字节跳动',
    lastMessage: '您好，恭喜您通过简历筛选...',
    time: '刚刚',
    unread: 2
  },
  {
    id: 2,
    name: '阿里巴巴HR-王经理',
    avatar: 'https://images.unsplash.com/photo-1580489944761-15a19d654956?w=100&h=100&fit=crop&crop=face',
    company: '阿里巴巴',
    lastMessage: '面试安排在明天下午3点',
    time: '10:30',
    unread: 0
  },
  {
    id: 3,
    name: '腾讯HR-张经理',
    avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop&crop=face',
    company: '腾讯',
    lastMessage: '感谢您参加面试，请等待通知',
    time: '昨天',
    unread: 0
  }
])

const selectedConversation = computed(() => conversations.value.find(c => c.id === selectedId.value))

const messages = ref([
  { id: 1, isMine: false, content: '您好，我是字节跳动的HR，看到了您的简历...', time: '10:00' },
  { id: 2, isMine: true, content: '您好，很高兴收到您的消息', time: '10:02' },
  { id: 3, isMine: false, content: '我们正在招聘前端开发工程师岗位，请问您有兴趣吗？', time: '10:05' },
  { id: 4, isMine: true, content: '有的，请问岗位的具体要求是什么？', time: '10:08' },
  { id: 5, isMine: false, content: '您好，恭喜您通过简历筛选，请准备参加面试...', time: '刚刚' }
])

const selectConversation = (id) => {
  selectedId.value = id
  const conv = conversations.value.find(c => c.id === id)
  if (conv) conv.unread = 0
}

const sendMessage = () => {
  if (!inputMessage.value.trim()) return
  messages.value.push({
    id: Date.now(),
    isMine: true,
    content: inputMessage.value,
    time: '刚刚'
  })
  inputMessage.value = ''
}
</script>
