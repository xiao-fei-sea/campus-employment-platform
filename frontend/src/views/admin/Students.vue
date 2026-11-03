<template>
  <div class="p-8 space-y-6">
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6">
      <div v-for="card in statCards" :key="card.label" class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex items-center space-x-5">
        <div class="w-16 h-16 rounded-2xl flex items-center justify-center flex-shrink-0" :class="card.iconBg">
          <i :class="[card.icon, card.iconColor, 'text-3xl']" />
        </div>
        <div>
          <p class="text-gray-500 text-base">{{ card.label }}</p>
          <p class="text-4xl font-bold text-gray-900">{{ typeof card.value === 'number' ? card.value.toLocaleString() : card.value }}</p>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-2xl shadow-sm p-6 flex flex-wrap items-center gap-4">
      <input v-model="filterCollege" type="text" placeholder="搜索学院..." class="px-5 py-3 bg-gray-100 border-0 rounded-xl text-gray-600 text-base focus:outline-none focus:ring-2 focus:ring-blue-500 hover:bg-gray-200 transition-colors w-52" />
      <input v-model="filterMajor" type="text" placeholder="搜索专业..." class="px-5 py-3 bg-gray-100 border-0 rounded-xl text-gray-600 text-base focus:outline-none focus:ring-2 focus:ring-blue-500 hover:bg-gray-200 transition-colors w-52" />
      <select v-model="filterStatus" class="px-5 py-3 bg-gray-100 border-0 rounded-xl text-gray-600 text-base focus:outline-none focus:ring-2 focus:ring-blue-500 hover:bg-gray-200 transition-colors">
        <option value="">全部状态</option>
        <option value="signed">已签约</option>
        <option value="searching">求职中</option>
        <option value="further_study">升学深造</option>
        <option value="offered">已录取</option>
        <option value="unemployed">未就业</option>
        <option value="startup">创业</option>
      </select>
      <select v-model="filterDegree" class="px-5 py-3 bg-gray-100 border-0 rounded-xl text-gray-600 text-base focus:outline-none focus:ring-2 focus:ring-blue-500 hover:bg-gray-200 transition-colors">
        <option value="">全部学历</option>
        <option value="博士">博士</option>
        <option value="硕士">硕士</option>
        <option value="本科">本科</option>
      </select>
      <select v-model="filterAssistance" class="px-5 py-3 bg-gray-100 border-0 rounded-xl text-gray-600 text-base focus:outline-none focus:ring-2 focus:ring-blue-500 hover:bg-gray-200 transition-colors">
        <option value="">全部学生</option>
        <option value="true">重点帮扶</option>
      </select>
      <div class="flex gap-3 ml-auto">
        <button type="button" class="px-5 py-3 bg-gray-100 hover:bg-gray-200 text-gray-600 rounded-xl transition-colors text-base font-medium" @click="onResetFilters">
          <i class="fas fa-redo mr-2" />重置
        </button>
        <button type="button" class="px-5 py-3 bg-gray-100 hover:bg-gray-200 text-gray-600 rounded-xl transition-colors text-base font-medium relative" @click="showExportMenu = !showExportMenu">
          <i class="fas fa-download mr-2" />导出
          <div v-if="showExportMenu" class="absolute right-0 top-full mt-2 bg-white rounded-xl shadow-lg border border-gray-200 py-2 z-50 min-w-32">
            <button type="button" class="w-full px-4 py-2 text-left hover:bg-gray-50 text-sm" @click="exportData('xlsx')">导出 Excel</button>
            <button type="button" class="w-full px-4 py-2 text-left hover:bg-gray-50 text-sm" @click="exportData('csv')">导出 CSV</button>
          </div>
        </button>
        <button type="button" class="px-5 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-xl transition-colors text-base font-medium" @click="onAddStudent">
          <i class="fas fa-plus mr-2" />添加学生
        </button>
      </div>
    </div>

    <div class="bg-white rounded-xl shadow-sm overflow-hidden border border-gray-200">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="px-6 py-4 text-left text-sm font-semibold text-gray-700">学生信息</th>
              <th class="px-6 py-4 text-left text-sm font-semibold text-gray-700">学院/专业</th>
              <th class="px-6 py-4 text-left text-sm font-semibold text-gray-700">学历</th>
              <th class="px-6 py-4 text-left text-sm font-semibold text-gray-700">就业状态</th>
              <th class="px-6 py-4 text-left text-sm font-semibold text-gray-700">签约单位</th>
              <th class="px-6 py-4 text-left text-sm font-semibold text-gray-700">薪资</th>
              <th class="px-6 py-4 text-right text-sm font-semibold text-gray-700">操作</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="row in pagedStudents" :key="row.id" class="hover:bg-gray-50 transition-colors">
              <td class="px-6 py-4">
                <div class="flex items-center space-x-4">
                  <img :src="row.avatar || 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=60&h=60&fit=crop&crop=face'" alt="头像" class="w-10 h-10 rounded-full object-cover border border-gray-200" />
                  <div>
                    <p class="font-semibold text-gray-900 text-sm">{{ row.name }}</p>
                    <p class="text-xs text-gray-500">{{ row.student_no }}</p>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4">
                <p class="text-sm text-gray-900">{{ row.college || '-' }}</p>
                <p class="text-xs text-gray-500">{{ row.major || '-' }}</p>
              </td>
              <td class="px-6 py-4 text-sm text-gray-600">{{ row.education_degree || '-' }}</td>
              <td class="px-6 py-4">
                <span :class="statusBadgeClass(row.employment_status)">{{ statusText(row.employment_status) }}</span>
              </td>
              <td class="px-6 py-4">
                <span class="text-sm text-gray-900">{{ row.company_name || '-' }}</span>
              </td>
              <td class="px-6 py-4">
                <span class="text-sm text-gray-900">{{ row.salary ? row.salary.toLocaleString() + '元/月' : '-' }}</span>
              </td>
              <td class="px-6 py-4">
                <div class="flex items-center justify-end space-x-1">
                  <button type="button" class="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors" title="查看详情" @click="onView(row)">
                    <i class="fas fa-eye" />
                  </button>
                  <button type="button" class="p-2 text-gray-400 hover:text-purple-600 hover:bg-purple-50 rounded-lg transition-colors" title="编辑" @click="onEdit(row)">
                    <i class="fas fa-edit" />
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="pagedStudents.length === 0">
              <td colspan="7" class="px-6 py-12 text-center">
                <div class="flex flex-col items-center justify-center space-y-3">
                  <i class="fas fa-inbox text-gray-300 text-4xl" />
                  <p class="text-gray-500">暂无匹配数据</p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="px-6 py-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-t border-gray-200 bg-white">
        <p class="text-gray-500 text-sm">共 {{ totalStudents.toLocaleString() }} 条数据</p>
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

    <el-dialog v-model="showDetailDialog" title="学生详情" width="600px">
      <div class="space-y-4" v-if="currentStudent">
        <div class="flex items-center space-x-4">
          <img :src="currentStudent.avatar || 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=60&h=60&fit=crop&crop=face'" class="w-16 h-16 rounded-full object-cover border border-gray-200" />
          <div>
            <h3 class="text-xl font-bold text-gray-900">{{ currentStudent.name }}</h3>
            <p class="text-gray-500">{{ currentStudent.student_no }}</p>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <p class="text-sm text-gray-500">学院</p>
            <p class="font-medium">{{ currentStudent.college || '-' }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">专业</p>
            <p class="font-medium">{{ currentStudent.major || '-' }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">班级</p>
            <p class="font-medium">{{ currentStudent.class_name || '-' }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">学历</p>
            <p class="font-medium">{{ currentStudent.education_degree || '-' }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">手机号</p>
            <p class="font-medium">{{ currentStudent.phone || '-' }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">就业状态</p>
            <p class="font-medium">{{ statusText(currentStudent.employment_status) }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">签约单位</p>
            <p class="font-medium">{{ currentStudent.company_name || '-' }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">薪资</p>
            <p class="font-medium">{{ currentStudent.salary ? currentStudent.salary.toLocaleString() + '元/月' : '-' }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">毕业年份</p>
            <p class="font-medium">{{ currentStudent.graduation_year || '-' }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">重点帮扶</p>
            <el-switch v-model="currentStudent.is_key_assistance" @change="onSaveHelp" />
          </div>
        </div>
        <div class="mt-4">
          <p class="text-sm text-gray-500 mb-2">帮扶备注</p>
          <el-input v-model="currentStudent.assistance_note" type="textarea" :rows="3" placeholder="请输入帮扶备注" @blur="onSaveHelp" />
        </div>
      </div>
    </el-dialog>

    <el-dialog v-model="showEditDialog" title="编辑学生信息" width="500px">
      <el-form :model="editForm" label-width="100px" class="space-y-4">
        <el-form-item label="就业状态">
          <el-select v-model="editForm.employment_status" class="w-full">
            <el-option value="signed" label="已签约" />
            <el-option value="searching" label="求职中" />
            <el-option value="further_study" label="升学深造" />
            <el-option value="offered" label="已录取" />
            <el-option value="unemployed" label="未就业" />
            <el-option value="startup" label="创业" />
          </el-select>
        </el-form-item>
        <el-form-item label="重点帮扶">
          <el-switch v-model="editForm.is_key_assistance" />
        </el-form-item>
        <el-form-item label="帮扶备注">
          <el-input v-model="editForm.assistance_note" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" @click="onSaveEdit">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showAddDialog" title="添加学生" width="600px">
      <el-form :model="addForm" label-width="90px">
        <div class="grid grid-cols-2 gap-4">
          <el-form-item label="学号" required>
            <el-input v-model="addForm.student_no" placeholder="请输入学号" />
          </el-form-item>
          <el-form-item label="姓名" required>
            <el-input v-model="addForm.name" placeholder="请输入姓名" />
          </el-form-item>
          <el-form-item label="学院">
            <el-input v-model="addForm.college" placeholder="请输入学院" />
          </el-form-item>
          <el-form-item label="专业">
            <el-input v-model="addForm.major" placeholder="请输入专业" />
          </el-form-item>
          <el-form-item label="班级">
            <el-input v-model="addForm.class_name" placeholder="请输入班级" />
          </el-form-item>
          <el-form-item label="毕业年份">
            <el-input-number v-model="addForm.graduation_year" :min="2020" :max="2035" class="w-full" />
          </el-form-item>
          <el-form-item label="手机号">
            <el-input v-model="addForm.phone" placeholder="请输入手机号" />
          </el-form-item>
          <el-form-item label="登录密码">
            <el-input v-model="addForm.password" type="password" show-password />
          </el-form-item>
        </div>
      </el-form>
      <p class="text-xs text-gray-500">登录名默认使用学号，邮箱默认使用“学号@campus.edu.cn”。</p>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="submitAddStudent">添加</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
defineOptions({ name: 'Students' })
import { computed, ref, watch, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import router from '@/router'
import api, { adminAPI } from '@/api/index'
import * as XLSX from 'xlsx'

const userStore = useUserStore()
const userName = computed(() => userStore.userInfo?.name || '管理员')

const searchKeyword = ref('')
const filterCollege = ref('')
const filterMajor = ref('')
const filterStatus = ref('')
const filterDegree = ref('')
const filterAssistance = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const showExportMenu = ref(false)
const showDetailDialog = ref(false)
const currentStudent = ref({})
const showEditDialog = ref(false)
const showAddDialog = ref(false)
const addForm = ref({
  student_no: '',
  name: '',
  college: '',
  major: '',
  class_name: '',
  graduation_year: new Date().getFullYear() + 1,
  phone: '',
  password: '123456'
})
const editForm = ref({
  employment_status: '',
  is_key_assistance: false,
  assistance_note: ''
})

const stats = ref({
  total: 0,
  signed: 0,
  searching: 0,
  further_study: 0,
  offered: 0,
  unemployed: 0,
  startup: 0
})

const students = ref([])
const filteredStudents = computed(() => {
  return students.value.filter(s => {
    if (filterCollege.value && !s.college?.toLowerCase().includes(filterCollege.value.toLowerCase())) return false
    if (filterMajor.value && !s.major?.toLowerCase().includes(filterMajor.value.toLowerCase())) return false
    if (filterStatus.value && s.employment_status !== filterStatus.value) return false
    if (filterDegree.value && s.education_degree !== filterDegree.value) return false
    if (filterAssistance.value === 'true' && !s.is_key_assistance) return false
    return true
  })
})

const totalStudents = computed(() => filteredStudents.value.length)
const totalPages = computed(() => Math.ceil(totalStudents.value / pageSize.value) || 1)

const pagedStudents = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredStudents.value.slice(start, end)
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

const statCards = computed(() => [
  { label: '学生总数', value: stats.value.total, icon: 'fas fa-users', iconBg: 'bg-blue-50', iconColor: 'text-blue-500' },
  { label: '已签约', value: stats.value.signed, icon: 'fas fa-file-signature', iconBg: 'bg-green-50', iconColor: 'text-green-500' },
  { label: '求职中', value: stats.value.searching, icon: 'fas fa-search', iconBg: 'bg-yellow-50', iconColor: 'text-yellow-500' },
  { label: '升学深造', value: stats.value.further_study, icon: 'fas fa-graduation-cap', iconBg: 'bg-purple-50', iconColor: 'text-purple-500' },
  { label: '未就业', value: stats.value.unemployed, icon: 'fas fa-user-slash', iconBg: 'bg-red-50', iconColor: 'text-red-500' }
])

function statusText(status) {
  const map = {
    signed: '已签约',
    searching: '求职中',
    further_study: '升学深造',
    offered: '已录取',
    unemployed: '未就业',
    startup: '创业'
  }
  return map[status] || status
}

function statusBadgeClass(status) {
  const map = {
    signed: 'px-2 py-1 text-xs font-medium rounded-full bg-green-100 text-green-700',
    searching: 'px-2 py-1 text-xs font-medium rounded-full bg-yellow-100 text-yellow-700',
    further_study: 'px-2 py-1 text-xs font-medium rounded-full bg-purple-100 text-purple-700',
    offered: 'px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-700',
    unemployed: 'px-2 py-1 text-xs font-medium rounded-full bg-red-100 text-red-700',
    startup: 'px-2 py-1 text-xs font-medium rounded-full bg-orange-100 text-orange-700'
  }
  return map[status] || 'px-2 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-700'
}

async function fetchStudents() {
  try {
    const res = await adminAPI.getStudents({ page: 1, page_size: 10000 })
    const raw = res.data
    const data = raw.data || raw
    students.value = Array.isArray(data) ? data : (data.students || [])
  } catch (err) {
    console.error('获取学生列表失败', err)
  }
}

async function fetchStats() {
  try {
    const res = await adminAPI.get('/admin/statistics/stats')
    const data = res.data.data || res.data
    stats.value = {
      total: data.total_students || 0,
      signed: data.employed_count || 0,
      searching: data.searching_count || 0,
      further_study: data.further_study_count || 0,
      offered: data.offered_count || 0,
      unemployed: data.unemployed_count || 0,
      startup: data.startup_count || 0
    }
  } catch (err) {
    console.error('获取统计数据失败', err)
  }
}

function onView(row) {
  currentStudent.value = { ...row }
  showDetailDialog.value = true
}

async function onSaveHelp() {
  try {
    await adminAPI.updateStudent(currentStudent.value.id, {
      is_key_assistance: currentStudent.value.is_key_assistance,
      assistance_note: currentStudent.value.assistance_note
    })
    ElMessage.success('帮扶信息已保存')
    fetchStudents()
    fetchStats()
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

function onEdit(row) {
  currentStudent.value = row
  editForm.value = {
    employment_status: row.employment_status || '',
    is_key_assistance: row.is_key_assistance || false,
    assistance_note: row.assistance_note || ''
  }
  showEditDialog.value = true
}

async function onSaveEdit() {
  try {
    await adminAPI.updateStudent(currentStudent.value.id, {
      employment_status: editForm.value.employment_status,
      is_key_assistance: editForm.value.is_key_assistance,
      assistance_note: editForm.value.assistance_note
    })
    ElMessage.success('保存成功')
    showEditDialog.value = false
    fetchStudents()
    fetchStats()
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

function onResetFilters() {
  filterCollege.value = ''
  filterMajor.value = ''
  filterStatus.value = ''
  filterDegree.value = ''
  filterAssistance.value = ''
  currentPage.value = 1
}

function exportData(format) {
  showExportMenu.value = false
  const data = filteredStudents.value.map(s => ({
    '学号': s.student_id || s.id,
    '姓名': s.name || s.username,
    '学院': s.college || '-',
    '专业': s.major || '-',
    '学历': s.education_degree || '-',
    '就业状态': s.employment_status || '-',
    '签约单位': s.employment_company || '-',
    '联系电话': s.phone || '-',
    '邮箱': s.email || '-'
  }))

  if (format === 'csv') {
    const ws = XLSX.utils.json_to_sheet(data)
    const csv = XLSX.utils.sheet_to_csv(ws)
    const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `学生数据_${new Date().toISOString().slice(0, 10)}.csv`
    a.click()
    URL.revokeObjectURL(url)
  } else {
    const ws = XLSX.utils.json_to_sheet(data)
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, '学生数据')
    XLSX.writeFile(wb, `学生数据_${new Date().toISOString().slice(0, 10)}.xlsx`)
  }
  ElMessage.success('导出成功')
}

function onAddStudent() {
  addForm.value = {
    student_no: '',
    name: '',
    college: '',
    major: '',
    class_name: '',
    graduation_year: new Date().getFullYear() + 1,
    phone: '',
    password: '123456'
  }
  showAddDialog.value = true
}

async function submitAddStudent() {
  if (!addForm.value.student_no || !addForm.value.name) {
    ElMessage.warning('请填写学号和姓名')
    return
  }
  try {
    await adminAPI.createStudent(addForm.value)
    ElMessage.success('添加成功')
    showAddDialog.value = false
    fetchStudents()
    fetchStats()
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '添加失败')
  }
}

watch([filterCollege, filterMajor, filterStatus, filterDegree, filterAssistance], () => {
  currentPage.value = 1
})

watch(currentPage, () => {
  fetchStudents()
})

onMounted(() => {
  fetchStudents()
  fetchStats()
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.relative')) {
      showExportMenu.value = false
    }
  })
})
</script>
