<template>
  <div class="p-8 space-y-6">
      <!-- 统计卡片 -->
      <div class="grid grid-cols-4 gap-6">
        <div
          v-for="card in statCards"
          :key="card.label"
          class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex items-center space-x-5"
        >
          <div class="w-16 h-16 rounded-2xl flex items-center justify-center flex-shrink-0" :class="card.iconBg">
            <i :class="[card.icon, card.iconColor, 'text-3xl']" />
          </div>
          <div>
            <p class="text-gray-500 text-base">{{ card.label }}</p>
            <p class="text-4xl font-bold" :class="card.valueClass || 'text-gray-900'">
              {{ typeof card.value === 'number' ? card.value.toLocaleString() : card.value }}
            </p>
          </div>
        </div>
      </div>

      <!-- 过滤栏 -->
      <div class="bg-white rounded-xl shadow-sm p-4 border border-gray-100">
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div class="flex flex-wrap items-center gap-2">
            <button
              v-for="btn in statusButtons"
              :key="btn.value"
              type="button"
              class="px-4 py-2.5 rounded-xl text-sm font-medium transition-colors"
              :class="filterStatus === btn.value 
                ? 'bg-emerald-600 text-white' 
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
              @click="filterStatus = btn.value"
            >
              {{ btn.label }}
            </button>
          </div>
          <div class="flex flex-wrap gap-2">
            <select
              v-model="filterIndustry"
              class="px-4 py-2.5 bg-gray-100 border-0 rounded-xl text-gray-600 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 hover:bg-gray-200 transition-colors"
            >
              <option value="">全部行业</option>
              <option value="it">互联网/IT</option>
              <option value="finance">金融</option>
              <option value="manufacturing">制造业</option>
              <option value="education">教育培训</option>
              <option value="healthcare">医疗健康</option>
              <option value="real_estate">房地产</option>
              <option value="retail">零售/消费品</option>
              <option value="other">其他</option>
            </select>
            <button
              type="button"
              class="px-4 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-600 rounded-xl transition-colors text-sm font-medium relative"
              @click="showExportMenu = !showExportMenu"
            >
              <i class="fas fa-download mr-2" />导出
              <div v-if="showExportMenu" class="absolute right-0 top-full mt-2 bg-white rounded-xl shadow-lg border border-gray-200 py-2 z-50 min-w-32">
                <button type="button" class="w-full px-4 py-2 text-left hover:bg-gray-50 text-sm" @click="exportData('xlsx')">导出 Excel</button>
                <button type="button" class="w-full px-4 py-2 text-left hover:bg-gray-50 text-sm" @click="exportData('csv')">导出 CSV</button>
              </div>
            </button>
          </div>
        </div>
      </div>

      <!-- 表格 -->
      <div class="bg-white rounded-xl shadow-sm overflow-hidden border border-gray-200">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gray-50 border-b border-gray-200">
              <tr>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-700">企业信息</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-700">行业</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-700">规模</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-700">入驻时间</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-700">发布岗位数</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-700">状态</th>
                <th class="px-6 py-4 text-right text-sm font-semibold text-gray-700">操作</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr
                v-for="row in pagedCompanies"
                :key="row.id"
                class="hover:bg-gray-50 transition-colors"
                :class="getRowBgClass(row.status)"
              >
                <td class="px-6 py-4">
                  <div class="flex items-center space-x-4">
                    <img :src="row.logo" alt="企业" class="w-12 h-12 rounded-xl object-cover border border-gray-200">
                    <div>
                      <p class="font-semibold text-gray-900 text-sm">{{ row.name }}</p>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 text-sm text-gray-700">{{ getIndustryText(row.industry) }}</td>
                <td class="px-6 py-4 text-sm text-gray-700">{{ getScaleText(row.scale) }}</td>
                <td class="px-6 py-4 text-sm text-gray-600">{{ row.join_time }}</td>
                <td class="px-6 py-4 text-sm text-gray-700">{{ row.job_count }}</td>
                <td class="px-6 py-4">
                  <span :class="statusBadgeClass(row.status)">{{ statusText(row.status) }}</span>
                </td>
                <td class="px-6 py-4">
                  <div class="flex items-center justify-end space-x-1">
                    <button
                      v-if="row.status === 'pending'"
                      type="button"
                      class="px-3 py-1.5 text-sm bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg transition-colors"
                      @click="onApprove(row)"
                    >
                      审核通过
                    </button>
                    <button
                      v-if="row.status === 'pending'"
                      type="button"
                      class="px-3 py-1.5 text-sm bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
                      @click="onReject(row)"
                    >
                      不通过
                    </button>
                    <button
                      v-if="row.status === 'blacklisted'"
                      type="button"
                      class="p-2 text-gray-400 hover:text-emerald-600 hover:bg-emerald-50 rounded-lg transition-colors"
                      title="撤销拉黑"
                      @click="onUnblacklist(row)"
                    >
                      <i class="fas fa-undo" />
                    </button>
                    <button
                      v-if="row.status === 'approved' && !row.isBlacklisted"
                      type="button"
                      class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                      title="拉黑"
                      @click="onBlacklist(row)"
                    >
                      <i class="fas fa-ban" />
                    </button>
                    <button
                      type="button"
                      class="p-2 text-gray-400 hover:text-emerald-600 hover:bg-emerald-50 rounded-lg transition-colors"
                      title="查看详情"
                      @click="onView(row)"
                    >
                      <i class="fas fa-eye" />
                    </button>
                  </div>
                </td>
              </tr>
              <!-- 无数据提示 -->
              <tr v-if="pagedCompanies.length === 0">
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

        <!-- 分页 -->
        <div class="px-6 py-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-t border-gray-200 bg-white">
          <p class="text-gray-500 text-sm">共 {{ totalCompanies.toLocaleString() }} 条数据</p>
          <div class="flex items-center flex-wrap justify-center gap-1">
            <button
              type="button"
              class="px-3 py-2 bg-white text-gray-600 rounded-lg hover:bg-gray-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-sm border border-gray-200"
              :disabled="currentPage <= 1"
              @click="currentPage--"
              title="上一页"
            >
              <i class="fas fa-chevron-left" />
            </button>
            <template v-for="(p, idx) in visiblePages">
              <span v-if="p === '...'" :key="`ellipsis-${idx}`" class="px-2 text-gray-400 text-sm">...</span>
              <button
                v-else
                :key="`page-btn-${p}`"
                type="button"
                class="px-3 py-2 rounded-lg transition-colors text-sm font-medium"
                :class="p === currentPage ? 'bg-emerald-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-100 border border-gray-200'"
                @click="currentPage = p"
              >
                {{ p }}
              </button>
            </template>
            <button
              type="button"
              class="px-3 py-2 bg-white text-gray-600 rounded-lg hover:bg-gray-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-sm border border-gray-200"
              :disabled="currentPage >= totalPages"
              @click="currentPage++"
              title="下一页"
            >
              <i class="fas fa-chevron-right" />
            </button>
          </div>
        </div>
    </div>

    <el-dialog v-model="showDetailDialog" title="企业详情" width="600px">
      <div class="space-y-4">
        <div class="flex items-center space-x-4">
          <img :src="currentCompany.logo" class="w-20 h-20 rounded-xl object-cover border border-gray-200">
          <div>
            <h3 class="text-xl font-bold text-gray-900">{{ currentCompany.name }}</h3>
            <p class="text-gray-500">{{ currentCompany.short_name || '' }}</p>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <p class="text-sm text-gray-500">行业</p>
            <p class="font-medium">{{ getIndustryText(currentCompany.industry) }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">规模</p>
            <p class="font-medium">{{ getScaleText(currentCompany.scale) }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">入驻时间</p>
            <p class="font-medium">{{ currentCompany.join_time || '-' }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">发布岗位</p>
            <p class="font-medium">{{ currentCompany.job_count || 0 }}</p>
          </div>
          <div class="col-span-2" v-if="currentCompany.job_titles && currentCompany.job_titles.length > 0">
            <p class="text-sm text-gray-500">岗位列表</p>
            <div class="flex flex-wrap gap-2 mt-1">
              <span v-for="title in currentCompany.job_titles" :key="title" class="px-3 py-1 bg-emerald-50 text-emerald-700 text-sm rounded-full">{{ title }}</span>
            </div>
          </div>
          <div>
            <p class="text-sm text-gray-500">联系人</p>
            <p class="font-medium">{{ currentCompany.contact_name || '-' }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">联系电话</p>
            <p class="font-medium">{{ currentCompany.contact_phone || '-' }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">联系邮箱</p>
            <p class="font-medium">{{ currentCompany.contact_email || '-' }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">状态</p>
            <p class="font-medium">{{ statusText(currentCompany.status) }}</p>
          </div>
          <div class="col-span-2">
            <p class="text-sm text-gray-500">地址</p>
            <p class="font-medium">{{ [currentCompany.province, currentCompany.city, currentCompany.district, currentCompany.address].filter(Boolean).join('') || '-' }}</p>
          </div>
          <div class="col-span-2">
            <p class="text-sm text-gray-500">公司简介</p>
            <p class="font-medium text-gray-700">{{ currentCompany.description || '暂无描述' }}</p>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
defineOptions({ name: 'Companies' })
import { computed, ref, watch, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import router from '@/router'
import api, { adminAPI } from '@/api/index'
import * as XLSX from 'xlsx'

const userStore = useUserStore()
const userName = computed(() => userStore.userInfo?.name || '管理员')

const searchKeyword = ref('')
const filterStatus = ref('all')
const filterIndustry = ref('')
const currentPage = ref(1)
const pageSize = ref(10)

const showDetailDialog = ref(false)
const currentCompany = ref({})

const stats = ref({
  totalCompanies: 0,
  pending: 0,
  approved: 0,
  blacklist: 0
})

const companiesRaw = ref([])
const totalCompanies = ref(0)
const loading = ref(false)
const showExportMenu = ref(false)

async function fetchStats() {
  try {
    const [pendingRes, approvedRes, blacklistedRes] = await Promise.all([
      adminAPI.getCompanies({ status: 'pending', page_size: 1 }),
      adminAPI.getCompanies({ status: 'approved', page_size: 1 }),
      adminAPI.getCompanies({ status: 'blacklisted', page_size: 1 })
    ])
    stats.value = {
      totalCompanies: (pendingRes.data.total || 0) + (approvedRes.data.total || 0) + (blacklistedRes.data.total || 0),
      pending: pendingRes.data.total || 0,
      approved: approvedRes.data.total || 0,
      blacklist: blacklistedRes.data.total || 0
    }
  } catch (error) {
    console.error('Failed to fetch stats:', error)
  }
}

async function fetchCompanies() {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }
    if (filterStatus.value && filterStatus.value !== 'all') {
      params.status = filterStatus.value
    }
    if (filterIndustry.value) {
      params.industry = filterIndustry.value
    }
    if (searchKeyword.value.trim()) {
      params.keyword = searchKeyword.value.trim()
    }
    const res = await adminAPI.getCompanies(params)
    if (res.data) {
      companiesRaw.value = res.data.companies || res.data || []
      totalCompanies.value = res.data.total || (Array.isArray(res.data) ? res.data.length : 0)
    }
  } catch (error) {
    console.error('Failed to fetch companies:', error)
  } finally {
    loading.value = false
  }
}

const statCards = computed(() => [
  {
    label: '入驻总数',
    value: stats.value.totalCompanies,
    icon: 'fas fa-building',
    iconBg: 'bg-emerald-50',
    iconColor: 'text-emerald-600'
  },
  {
    label: '待审核',
    value: stats.value.pending,
    icon: 'fas fa-clock',
    iconBg: 'bg-yellow-50',
    iconColor: 'text-yellow-500',
    valueClass: 'text-yellow-600'
  },
  {
    label: '已认证',
    value: stats.value.approved,
    icon: 'fas fa-check-circle',
    iconBg: 'bg-green-50',
    iconColor: 'text-green-600',
    valueClass: 'text-green-600'
  },
  {
    label: '黑名单',
    value: stats.value.blacklist,
    icon: 'fas fa-ban',
    iconBg: 'bg-red-50',
    iconColor: 'text-red-600',
    valueClass: 'text-red-600'
  }
])

const statusButtons = [
  { label: '全部', value: 'all' },
  { label: '待审核', value: 'pending' },
  { label: '已认证', value: 'approved' },
  { label: '黑名单', value: 'blacklisted' }
]

function statusText(status) {
  const map = {
    approved: '已认证',
    pending: '待审核',
    blacklisted: '已拉黑'
  }
  return map[status] || status
}

function statusBadgeClass(status) {
  const base = 'px-3 py-1 text-xs rounded-full font-medium'
  const map = {
    approved: 'bg-green-100 text-green-700',
    pending: 'bg-yellow-100 text-yellow-700',
    blacklisted: 'bg-red-100 text-red-700'
  }
  return `${base} ${map[status] || 'bg-gray-100 text-gray-700'}`
}

function getRowBgClass(status) {
  const map = {
    pending: 'bg-yellow-50/30',
    blacklisted: 'bg-red-50/30',
    approved: ''
  }
  return map[status] || ''
}

function getStatusTextClass(status) {
  const map = {
    approved: 'text-gray-500',
    pending: 'text-gray-500',
    blacklisted: 'text-red-500'
  }
  return map[status] || 'text-gray-500'
}

function getIndustryText(industry) {
  const map = {
    it: '互联网/IT',
    finance: '金融',
    manufacturing: '制造业',
    education: '教育培训',
    healthcare: '医疗健康',
    real_estate: '房地产',
    retail: '零售/消费品',
    other: '其他'
  }
  return map[industry] || industry
}

function getScaleText(scale) {
  const map = {
    small: '小微企业',
    medium: '中型企业',
    large: '大型企业',
    super_large: '超大型企业'
  }
  return map[scale] || scale
}

const filteredCompanies = computed(() => {
  return companiesRaw.value
})

const totalPages = computed(() =>
  Math.max(1, Math.ceil(totalCompanies.value / pageSize.value))
)

watch([totalPages, () => totalCompanies.value], () => {
  if (currentPage.value > totalPages.value) {
    currentPage.value = totalPages.value
  }
})

const pagedCompanies = computed(() => {
  return companiesRaw.value
})

watch([filterStatus, filterIndustry, searchKeyword], () => {
  currentPage.value = 1
  fetchCompanies()
})

watch(currentPage, () => {
  fetchCompanies()
})

onMounted(() => {
  fetchStats()
  fetchCompanies()
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.relative')) {
      showExportMenu.value = false
    }
  })
})

const visiblePages = computed(() => {
  const total = totalPages.value
  const cur = currentPage.value

  if (total <= 9) {
    return Array.from({ length: total }, (_, i) => i + 1)
  }

  const pages = new Set([1, total, cur - 2, cur - 1, cur, cur + 1, cur + 2])
  const sorted = [...pages]
    .filter((n) => n >= 1 && n <= total)
    .sort((a, b) => a - b)

  const result = []
  for (let i = 0; i < sorted.length; i++) {
    if (i > 0 && sorted[i] - sorted[i - 1] > 1) {
      result.push('...')
    }
    result.push(sorted[i])
  }

  return result
})

function exportData(format) {
  showExportMenu.value = false
  const data = companies.value.map(c => ({
    '企业名称': c.name || c.company_name,
    '统一社会信用代码': c.unified_social_credit_code || c.code || '-',
    '行业': c.industry || '-',
    '规模': c.scale || '-',
    '城市': c.city || c.province || '-',
    '联系人': c.contact_person || c.contact_name || '-',
    '联系电话': c.contact_phone || c.phone || '-',
    '邮箱': c.email || '-',
    '状态': c.status === 'approved' ? '已认证' : c.status === 'pending' ? '待审核' : '已拉黑'
  }))

  if (format === 'csv') {
    const ws = XLSX.utils.json_to_sheet(data)
    const csv = XLSX.utils.sheet_to_csv(ws)
    const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `企业数据_${new Date().toISOString().slice(0, 10)}.csv`
    a.click()
    URL.revokeObjectURL(url)
  } else {
    const ws = XLSX.utils.json_to_sheet(data)
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, '企业数据')
    XLSX.writeFile(wb, `企业数据_${new Date().toISOString().slice(0, 10)}.xlsx`)
  }
  ElMessage.success('导出成功')
}

async function onApprove(row) {
  try {
    await adminAPI.approveCompany(row.id)
    ElMessage.success('已通过审核')
    fetchCompanies()
    fetchStats()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

async function onReject(row) {
  try {
    await adminAPI.rejectCompany(row.id)
    ElMessage.info('已拒绝')
    fetchCompanies()
    fetchStats()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

async function onBlacklist(row) {
  try {
    await adminAPI.blacklistCompany(row.id)
    ElMessage.success('已加入黑名单')
    fetchCompanies()
    fetchStats()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

async function onUnblacklist(row) {
  try {
    await adminAPI.removeBlacklistCompany(row.id)
    ElMessage.success('已撤销拉黑')
    fetchCompanies()
    fetchStats()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

function onView(row) {
  currentCompany.value = row
  showDetailDialog.value = true
}
</script>
