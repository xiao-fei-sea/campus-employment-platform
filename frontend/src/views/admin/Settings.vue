<template>
  <div class="p-8 space-y-6">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="bg-white rounded-2xl shadow-sm p-6 cursor-pointer hover:shadow-md transition-shadow" @click="activeTab = 'account'">
        <div class="flex items-center space-x-4">
          <div class="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
            <i class="fas fa-user-shield text-blue-600 text-xl"></i>
          </div>
          <div>
            <h3 class="font-bold text-gray-900">账号管理</h3>
            <p class="text-sm text-gray-500">{{ users.length }} 个账号</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-2xl shadow-sm p-6 cursor-pointer hover:shadow-md transition-shadow" @click="activeTab = 'roles'">
        <div class="flex items-center space-x-4">
          <div class="w-12 h-12 bg-emerald-100 rounded-xl flex items-center justify-center">
            <i class="fas fa-user-cog text-emerald-600 text-xl"></i>
          </div>
          <div>
            <h3 class="font-bold text-gray-900">角色权限</h3>
            <p class="text-sm text-gray-500">{{ roles.length }} 个角色</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-2xl shadow-sm p-6 cursor-pointer hover:shadow-md transition-shadow" @click="activeTab = 'logs'">
        <div class="flex items-center space-x-4">
          <div class="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center">
            <i class="fas fa-history text-purple-600 text-xl"></i>
          </div>
          <div>
            <h3 class="font-bold text-gray-900">操作日志</h3>
            <p class="text-sm text-gray-500">查看系统操作</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-2xl shadow-sm p-6 cursor-pointer hover:shadow-md transition-shadow" @click="activeTab = 'notifications'">
        <div class="flex items-center space-x-4">
          <div class="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center">
            <i class="fas fa-bell text-orange-600 text-xl"></i>
          </div>
          <div>
            <h3 class="font-bold text-gray-900">通知配置</h3>
            <p class="text-sm text-gray-500">系统消息设置</p>
          </div>
        </div>
      </div>
    </div>

    <div v-show="activeTab === 'account'" class="bg-white rounded-2xl shadow-sm p-8">
      <div class="flex items-center justify-between mb-6">
        <h3 class="text-lg font-bold text-gray-900">账号管理</h3>
        <el-button type="primary" @click="showAddDialog = true">
          <i class="fas fa-plus mr-2"></i>添加账号
        </el-button>
      </div>

      <el-table :data="pagedUsers" stripe class="mb-6">
        <el-table-column label="账号信息" min-width="200">
          <template #default="{ row }">
            <div class="flex items-center space-x-3">
              <img :src="row.avatar || '/placeholder-logo.png'" class="w-10 h-10 rounded-full">
              <div>
                <p class="font-medium text-gray-900">{{ row.name || row.username }}</p>
                <p class="text-sm text-gray-500">{{ row.email }}</p>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="角色" width="120">
          <template #default="{ row }">
            <span :class="getRoleClass(row.role)" class="px-2 py-1 text-xs rounded-full">
              {{ getRoleText(row.role) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="最后登录" width="180">
          <template #default="{ row }">
            {{ row.lastLogin || row.last_login || '从未登录' }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <span :class="row.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'" class="px-2 py-1 text-xs rounded-full">
              {{ row.is_active ? '正常' : '禁用' }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" align="center">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="editUser(row)">
              <i class="fas fa-edit"></i>
            </el-button>
            <el-button size="small" @click="resetPassword(row)">
              <i class="fas fa-key"></i>
            </el-button>
            <el-button size="small" type="danger" @click="removeUser(row)">
              <i class="fas fa-trash"></i>
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="px-6 py-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-t border-gray-200 bg-white">
        <p class="text-gray-500 text-sm">共 {{ totalUsers }} 条数据</p>
        <div class="flex items-center flex-wrap justify-center gap-1">
          <button type="button" class="px-3 py-2 bg-white text-gray-600 rounded-lg hover:bg-gray-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-sm border border-gray-200" :disabled="currentPage <= 1" @click="currentPage--" title="上一页">
            <i class="fas fa-chevron-left" />
          </button>
          <template v-for="(p, idx) in visiblePages">
            <span v-if="p === '...'" :key="`ellipsis-${idx}`" class="px-2 text-gray-400 text-sm">...</span>
            <button v-else :key="`page-btn-${p}`" type="button" class="px-3 py-2 rounded-lg transition-colors text-sm font-medium" :class="p === currentPage ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-100 border border-gray-200'" @click="currentPage = p">
              {{ p }}
            </button>
          </template>
          <button type="button" class="px-3 py-2 bg-white text-gray-600 rounded-lg hover:bg-gray-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-sm border border-gray-200" :disabled="currentPage >= totalPages" @click="currentPage++" title="下一页">
            <i class="fas fa-chevron-right" />
          </button>
        </div>
      </div>
    </div>

    <div v-show="activeTab === 'roles'" class="bg-white rounded-2xl shadow-sm p-8">
      <h3 class="text-lg font-bold text-gray-900 mb-6">角色权限配置</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="role in roles" :key="role.id" class="border border-gray-200 rounded-xl p-6 hover:border-emerald-300 transition-colors">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center space-x-3">
              <div :class="['w-10 h-10 rounded-xl flex items-center justify-center', role.iconBg || 'bg-emerald-100']">
                <i :class="[role.icon || 'fas fa-user', role.iconColor || 'text-emerald-600']"></i>
              </div>
              <div>
                <h4 class="font-medium text-gray-900">{{ role.name }}</h4>
                <p class="text-xs text-gray-500">{{ role.count || 0 }}人</p>
              </div>
            </div>
          </div>
          <div class="space-y-2 text-sm text-gray-600">
            <div v-for="perm in (role.permissions || [])" :key="perm" class="flex items-center">
              <i class="fas fa-check text-green-500 mr-2"></i>
              <span>{{ perm }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-show="activeTab === 'logs'" class="bg-white rounded-2xl shadow-sm p-8">
      <div class="flex items-center justify-between mb-6">
        <h3 class="text-lg font-bold text-gray-900">操作日志</h3>
        <el-button @click="exportLogs">导出日志</el-button>
      </div>
      <el-table :data="logs" stripe>
        <el-table-column label="操作人" prop="operator" width="120" />
        <el-table-column label="操作类型" prop="action" width="150" />
        <el-table-column label="操作内容" prop="content" />
        <el-table-column label="IP地址" prop="ip" width="140" />
        <el-table-column label="操作时间" prop="time" width="180" />
      </el-table>
    </div>

    <div v-show="activeTab === 'notifications'" class="bg-white rounded-2xl shadow-sm p-8">
      <h3 class="text-lg font-bold text-gray-900 mb-6">通知配置</h3>
      <div class="space-y-4">
        <div class="flex items-center justify-between py-4 border-b border-gray-100">
          <div>
            <h4 class="font-medium text-gray-900">系统通知</h4>
            <p class="text-sm text-gray-500">系统重要消息推送</p>
          </div>
          <el-switch v-model="notificationSettings.system" />
        </div>
        <div class="flex items-center justify-between py-4 border-b border-gray-100">
          <div>
            <h4 class="font-medium text-gray-900">岗位审核通知</h4>
            <p class="text-sm text-gray-500">新岗位提交审核时邮件提醒</p>
          </div>
          <el-switch v-model="notificationSettings.jobReview" />
        </div>
        <div class="flex items-center justify-between py-4 border-b border-gray-100">
          <div>
            <h4 class="font-medium text-gray-900">活动开始提醒</h4>
            <p class="text-sm text-gray-500">活动开始前24小时提醒报名学生</p>
          </div>
          <el-switch v-model="notificationSettings.activityReminder" />
        </div>
        <div class="flex items-center justify-between py-4">
          <div>
            <h4 class="font-medium text-gray-900">邮件通知</h4>
            <p class="text-sm text-gray-500">重要信息通过邮件发送</p>
          </div>
          <el-switch v-model="notificationSettings.email" />
        </div>
      </div>
      <div class="mt-6 pt-6 border-t border-gray-100">
        <el-button type="primary" @click="saveNotificationSettings">保存配置</el-button>
      </div>
    </div>

    <div v-show="activeTab === 'backup'" class="bg-white rounded-2xl shadow-sm p-8">
      <h3 class="text-lg font-bold text-gray-900 mb-6">数据备份</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div class="border border-gray-200 rounded-xl p-6">
          <div class="flex items-center justify-between mb-4">
            <h4 class="font-bold text-gray-900">自动备份</h4>
            <span class="px-3 py-1 text-sm rounded-full" :class="backupConfig.frequency === 'none' ? 'bg-gray-100 text-gray-600' : 'bg-green-100 text-green-700'">
              {{ backupConfig.frequency === 'none' ? '已关闭' : '已启用' }}
            </span>
          </div>
          <p class="text-sm text-gray-600 mb-4">{{ backupConfig.frequency === 'none' ? '当前不会自动执行备份' : '按所选周期自动执行全量备份' }}</p>
          <el-select v-model="backupConfig.frequency" class="w-full">
            <el-option label="每天" value="daily" />
            <el-option label="每周" value="weekly" />
            <el-option label="每月" value="monthly" />
            <el-option label="关闭自动备份" value="none" />
          </el-select>
          <el-button class="mt-4 w-full" @click="saveBackupConfig">保存备份配置</el-button>
        </div>
        <div class="border border-gray-200 rounded-xl p-6">
          <div class="flex items-center justify-between mb-4">
            <h4 class="font-bold text-gray-900">备份存储</h4>
            <span class="px-3 py-1 bg-blue-100 text-blue-700 text-sm rounded-full">本地</span>
          </div>
          <p class="text-sm text-gray-600 mb-2">共 {{ backupRecords.length }} 个备份文件</p>
          <p class="text-sm text-gray-600">备份文件保存在服务器 backups 目录</p>
        </div>
      </div>
      <div class="space-y-4">
        <h4 class="font-bold text-gray-900">最近备份记录</h4>
        <el-table :data="backupRecords" stripe row-key="filename">
          <el-table-column label="备份时间" prop="time" width="180" />
          <el-table-column label="备份类型" prop="type" width="120" />
          <el-table-column label="文件大小" prop="size" width="120" />
          <el-table-column label="状态" width="100">
            <template #default="{ row }">
              <span :class="row.status === 'success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'" class="px-2 py-1 text-xs rounded-full">
                {{ row.status === 'success' ? '成功' : '失败' }}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template #default="{ row }">
              <el-button size="small" type="primary" @click="downloadBackupFile(row)">下载</el-button>
              <el-button size="small" type="danger" @click="removeBackup(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div class="mt-6 pt-6 border-t border-gray-100">
        <el-button type="primary" @click="createBackup">立即备份</el-button>
      </div>
    </div>

    <el-dialog v-model="showAddDialog" title="添加账号" width="500px">
      <el-form :model="adminForm" label-position="top">
        <el-form-item label="登录名">
          <el-input v-model="adminForm.username" placeholder="请输入登录名" />
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="adminForm.name" placeholder="请输入管理员姓名" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="adminForm.email" placeholder="请输入管理员邮箱" />
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="adminForm.role" class="w-full">
            <el-option label="超级管理员" value="admin" />
            <el-option label="辅导员" value="counselor" />
          </el-select>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="adminForm.password" type="password" placeholder="请输入初始密码" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="addAdminAccount">添加</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showEditDialog" title="编辑账号" width="500px">
      <el-form :model="editForm" label-position="top">
        <el-form-item label="邮箱">
          <el-input v-model="editForm.email" />
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="editForm.role" class="w-full">
            <el-option label="超级管理员" value="admin" />
            <el-option label="辅导员" value="counselor" />
          </el-select>
        </el-form-item>
        <el-form-item label="账号状态">
          <el-switch v-model="editForm.is_active" active-text="正常" inactive-text="禁用" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" @click="saveUser">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
defineOptions({ name: 'Settings' })
import { ref, computed, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { adminAPI } from '@/api/index'
import * as XLSX from 'xlsx'

const activeTab = ref('account')
const showAddDialog = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)

const tabs = [
  { key: 'account', label: '账号管理', icon: 'fas fa-user-shield' },
  { key: 'roles', label: '角色权限', icon: 'fas fa-user-cog' },
  { key: 'logs', label: '操作日志', icon: 'fas fa-history' },
  { key: 'notifications', label: '通知配置', icon: 'fas fa-bell' },
  { key: 'backup', label: '数据备份', icon: 'fas fa-database' }
]

const adminForm = ref({ username: '', name: '', email: '', role: 'counselor', password: '' })
const showEditDialog = ref(false)
const editForm = reactive({ id: null, email: '', role: 'counselor', is_active: true })

const users = ref([])
const totalUsers = computed(() => users.value.length)
const totalPages = computed(() => Math.ceil(totalUsers.value / pageSize.value) || 1)
const pagedUsers = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return users.value.slice(start, end)
})
const visiblePages = computed(() => {
  const pages = []
  const total = totalPages.value
  const current = currentPage.value
  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i)
  } else {
    pages.push(1)
    if (current > 3) pages.push('...')
    for (let i = Math.max(2, current - 1); i <= Math.min(total - 1, current + 1); i++) pages.push(i)
    if (current < total - 2) pages.push('...')
    pages.push(total)
  }
  return pages
})

const roles = ref([
  { id: 'admin', name: '管理员', description: '系统管理员', iconBg: 'bg-red-100', iconColor: 'text-red-600', permissions: ['全部权限'] },
  { id: 'counselor', name: '就业顾问', description: '就业指导顾问', iconBg: 'bg-blue-100', iconColor: 'text-blue-600', permissions: ['学生管理', '统计分析', '企业管理'] },
  { id: 'teacher', name: '教师', description: '就业指导教师', iconBg: 'bg-green-100', iconColor: 'text-green-600', permissions: ['学生管理', '统计分析'] }
])
const logs = ref([])
const loading = ref(false)

async function fetchUsers() {
  loading.value = true
  try {
    const res = await adminAPI.getAdminUsers()
    if (res.data) {
      users.value = Array.isArray(res.data) ? res.data : res.data.users || []
    } else {
      users.value = []
    }
  } catch (error) {
    console.error('Failed to fetch users:', error)
    ElMessage.error('获取账号列表失败')
    users.value = []
  } finally {
    loading.value = false
  }
}

async function fetchRoles() {
  try {
    const res = await adminAPI.getRoles()
    if (res.data) {
      roles.value = Array.isArray(res.data) ? res.data : res.data.roles || []
    }
  } catch (error) {
    console.error('Failed to fetch roles:', error)
    ElMessage.error('获取角色列表失败')
  }
}

async function fetchLogs() {
  try {
    const res = await adminAPI.getOperationLogs({ page: 1, page_size: 20 })
    console.log('Logs response:', res.data)
    if (res.data) {
      const data = Array.isArray(res.data) ? res.data : res.data.data || res.data.logs || []
      logs.value = data
    } else {
      logs.value = []
    }
  } catch (error) {
    console.error('Failed to fetch logs:', error)
    ElMessage.error('获取操作日志失败')
    logs.value = []
  }
}

function exportLogs() {
  if (logs.value.length === 0) {
    ElMessage.warning('暂无数据可导出')
    return
  }
  const data = logs.value.map(log => ({
    '操作人': log.operator,
    '操作类型': log.action,
    '操作内容': log.content,
    'IP地址': log.ip,
    '操作时间': log.time
  }))
  const ws = XLSX.utils.json_to_sheet(data)
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, '操作日志')
  XLSX.writeFile(wb, `操作日志_${new Date().toISOString().slice(0, 10)}.xlsx`)
  ElMessage.success('导出成功')
}

async function addAdminAccount() {
  if (!adminForm.value.username || !adminForm.value.email || !adminForm.value.password) {
    ElMessage.warning('请填写登录名、邮箱和密码')
    return
  }
  try {
    await adminAPI.createAdminUser({
      username: adminForm.value.username,
      email: adminForm.value.email,
      role: adminForm.value.role,
      password: adminForm.value.password
    })
    ElMessage.success('添加成功')
    showAddDialog.value = false
    adminForm.value = { username: '', name: '', email: '', role: 'counselor', password: '' }
    fetchUsers()
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '添加失败')
  }
}

async function editUser(user) {
  editForm.id = user.id
  editForm.email = user.email
  editForm.role = user.role
  editForm.is_active = user.is_active
  showEditDialog.value = true
}

async function saveUser() {
  try {
    await adminAPI.updateAdminUser(editForm.id, {
      email: editForm.email,
      role: editForm.role,
      is_active: editForm.is_active
    })
    ElMessage.success('保存成功')
    showEditDialog.value = false
    fetchUsers()
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '保存失败')
  }
}

async function resetPassword(user) {
  try {
    const { value } = await ElMessageBox.prompt('请输入新的登录密码（至少6位）', '重置密码', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      inputPattern: /^.{6,}$/,
      inputErrorMessage: '密码至少6位'
    })
    await adminAPI.updateAdminUser(user.id, { password: value })
    ElMessage.success('密码已重置')
  } catch (error) {
    if (error !== 'cancel' && error !== 'close') {
      ElMessage.error(error.response?.data?.detail || '重置密码失败')
    }
  }
}

async function removeUser(user) {
  try {
    await ElMessageBox.confirm(`确定删除账号「${user.username}」吗？`, '提示', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await adminAPI.deleteAdminUser(user.id)
    ElMessage.success('删除成功')
    fetchUsers()
  } catch (error) {
    if (error !== 'cancel' && error !== 'close') {
      ElMessage.error(error.response?.data?.detail || '删除失败')
    }
  }
}

const getRoleClass = (role) => {
  const map = {
    admin: 'bg-emerald-100 text-emerald-700',
    staff: 'bg-blue-100 text-blue-700',
    counselor: 'bg-purple-100 text-purple-700'
  }
  return map[role] || ''
}

const getRoleText = (role) => {
  const map = {
    admin: '超级管理员',
    staff: '就业专员',
    counselor: '辅导员'
  }
  return map[role] || ''
}

const notificationSettings = reactive({
  system: true,
  jobReview: true,
  activityReminder: true,
  email: false
})

const backupConfig = ref({
  frequency: 'weekly'
})

const backupRecords = ref([])

async function loadSystemSettings() {
  try {
    const res = await adminAPI.getSettings()
    if (res.data?.notifications) {
      Object.assign(notificationSettings, res.data.notifications)
    }
    if (res.data?.backup?.frequency) {
      backupConfig.value.frequency = res.data.backup.frequency
    }
  } catch (error) {
    console.error('Failed to load system settings:', error)
  }
}

async function fetchBackups() {
  try {
    const res = await adminAPI.getBackups()
    backupRecords.value = Array.isArray(res.data) ? res.data : []
  } catch (error) {
    console.error('Failed to fetch backups:', error)
  }
}

const saveNotificationSettings = async () => {
  try {
    await adminAPI.updateSettings({ notifications: notificationSettings })
    ElMessage.success('保存成功')
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

const saveBackupConfig = async () => {
  try {
    await adminAPI.updateSettings({ backup: backupConfig.value })
    ElMessage.success('备份配置已保存')
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

const createBackup = async () => {
  try {
    await adminAPI.createBackup()
    ElMessage.success('备份已完成')
    await fetchBackups()
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '备份失败')
  }
}

const downloadBackupFile = async (row) => {
  try {
    const res = await adminAPI.downloadBackup(row.filename)
    const url = window.URL.createObjectURL(new Blob([res.data]))
    const link = document.createElement('a')
    link.href = url
    link.download = row.filename
    link.click()
    window.URL.revokeObjectURL(url)
  } catch (error) {
    ElMessage.error('下载失败')
  }
}

const removeBackup = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除该备份文件吗？', '提示', { type: 'warning' })
    await adminAPI.deleteBackup(row.filename)
    ElMessage.success('删除成功')
    await fetchBackups()
  } catch (error) {
    if (error !== 'cancel' && error !== 'close') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  fetchUsers()
  fetchRoles()
  fetchLogs()
  loadSystemSettings()
  fetchBackups()
})
</script>
