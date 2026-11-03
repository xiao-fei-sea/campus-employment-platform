<template>
  <div class="min-h-screen bg-gray-100 p-6 relative">
    <!-- ✅ 加载中遮罩 -->
    <div v-if="isLoading && !allData" class="absolute inset-0 bg-white/60 backdrop-blur-sm z-50 flex items-center justify-center">
      <div class="flex flex-col items-center space-y-3">
        <i class="fas fa-spinner fa-spin text-4xl text-emerald-500"></i>
        <p class="text-gray-600">正在加载数据...</p>
      </div>
    </div>

    <main>
      <!-- ✅ 顶部工具栏：手动刷新 + 最后加载时间 -->
      <div class="flex items-center justify-between mb-4">
        <div class="text-sm text-gray-500">
          <i class="fas fa-clock mr-1"></i>最后更新：<span class="font-medium text-gray-700">{{ lastUpdateTime || '加载中...' }}</span>
        </div>
        <button
          @click="loadAllData(true)"
          class="inline-flex items-center px-4 py-2 bg-white border border-gray-200 rounded-lg text-sm text-gray-700 hover:bg-gray-50 hover:border-emerald-300 transition-colors shadow-sm"
        >
          <i class="fas fa-sync-alt mr-2 text-emerald-500"></i>刷新数据
        </button>
      </div>
      <div class="grid grid-cols-4 gap-6 mb-6">
        <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex items-center space-x-5">
          <div class="w-16 h-16 bg-blue-100 rounded-2xl flex items-center justify-center flex-shrink-0">
            <i class="fas fa-user-graduate text-blue-600 text-3xl"></i>
          </div>
          <div>
            <p class="text-gray-500 text-base">应届毕业生总数</p>
            <p class="text-4xl font-bold text-gray-900">{{ stats.totalStudents.toLocaleString() }}</p>
          </div>
        </div>
        <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex items-center space-x-5">
          <div class="w-16 h-16 bg-emerald-100 rounded-2xl flex items-center justify-center flex-shrink-0">
            <i class="fas fa-chart-pie text-emerald-600 text-3xl"></i>
          </div>
          <div>
            <p class="text-gray-500 text-base">当前就业率</p>
            <p class="text-4xl font-bold bg-gradient-to-r from-blue-600 to-emerald-500 bg-clip-text text-transparent">{{ stats.employmentRate }}%</p>
            <p class="text-gray-400 text-base">已就业 {{ stats.employedStudents.toLocaleString() }} 人</p>
          </div>
        </div>
        <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex items-center space-x-5">
          <div class="w-16 h-16 bg-purple-100 rounded-2xl flex items-center justify-center flex-shrink-0">
            <i class="fas fa-briefcase text-purple-600 text-3xl"></i>
          </div>
          <div>
            <p class="text-gray-500 text-base">岗位总数</p>
            <p class="text-4xl font-bold text-gray-900">{{ stats.totalJobs.toLocaleString() }}</p>
            <p class="text-gray-400 text-base">入驻 {{ stats.totalCompanies.toLocaleString() }} 家企业</p>
          </div>
        </div>
        <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex items-center space-x-5">
          <div class="w-16 h-16 bg-orange-100 rounded-2xl flex items-center justify-center flex-shrink-0">
            <i class="fas fa-building text-orange-600 text-3xl"></i>
          </div>
          <div>
            <p class="text-gray-500 text-base">入驻企业总数</p>
            <p class="text-4xl font-bold text-gray-900">{{ stats.totalCompanies.toLocaleString() }}</p>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-3 gap-6 mb-6">
        <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <div class="flex items-center space-x-3 mb-5">
            <div class="w-14 h-14 bg-blue-100 rounded-2xl flex items-center justify-center flex-shrink-0">
              <i class="fas fa-chart-pie text-blue-600 text-2xl"></i>
            </div>
            <h3 class="text-lg font-bold text-gray-900">实时就业率</h3>
          </div>
          <div class="flex items-center space-x-6">
            <div class="relative w-32 h-32 flex-shrink-0">
              <svg class="w-full h-full transform -rotate-90">
                <defs>
                  <linearGradient id="progressGradientLight" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#34d399"/>
                    <stop offset="100%" stop-color="#10b981"/>
                  </linearGradient>
                </defs>
                <circle cx="64" cy="64" r="52" stroke="#f3f4f6" stroke-width="10" fill="none"/>
                <circle cx="64" cy="64" r="52" stroke="url(#progressGradientLight)" stroke-width="10" fill="none"
                  :stroke-dasharray="circumference" :stroke-dashoffset="progressOffset" stroke-linecap="round"/>
              </svg>
              <div class="absolute inset-0 flex flex-col items-center justify-center">
                <span class="text-3xl font-bold text-gray-900">{{ stats.employmentRate }}%</span>
              </div>
            </div>
            <div class="flex-1 space-y-4 text-base">
              <div class="flex items-center justify-between">
                <span class="text-gray-500">已就业</span>
                <span class="text-emerald-600 font-bold">{{ stats.employedStudents }}人</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-500">未就业</span>
                <span class="text-red-500 font-bold">{{ stats.totalStudents - stats.employedStudents }}人</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-500">目标</span>
                <span class="text-blue-600 font-bold">95%</span>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <div class="flex items-center space-x-3 mb-5">
            <div class="w-14 h-14 bg-emerald-100 rounded-2xl flex items-center justify-center flex-shrink-0">
              <i class="fas fa-chart-bar text-emerald-600 text-2xl"></i>
            </div>
            <h3 class="text-lg font-bold text-gray-900">就业状态构成</h3>
          </div>
          <div class="space-y-4">
            <div class="flex items-center">
              <div class="w-16 text-gray-600 text-base">已签约</div>
              <div class="flex-1 mx-2">
                <div class="h-7 bg-gray-100 rounded overflow-hidden">
                  <div class="h-full bg-emerald-500 rounded" :style="{ width: employmentStatus.signed + '%' }"></div>
                </div>
              </div>
              <div class="w-14 text-right"><span class="text-emerald-600 font-bold text-base">{{ employmentStatus.signed }}%</span></div>
            </div>
            <div class="flex items-center">
              <div class="w-16 text-gray-600 text-base">已OFFER</div>
              <div class="flex-1 mx-2">
                <div class="h-7 bg-gray-100 rounded overflow-hidden">
                  <div class="h-full bg-blue-500 rounded" :style="{ width: employmentStatus.offer + '%' }"></div>
                </div>
              </div>
              <div class="w-14 text-right"><span class="text-blue-600 font-bold text-base">{{ employmentStatus.offer }}%</span></div>
            </div>
            <div class="flex items-center">
              <div class="w-16 text-gray-600 text-base">求职中</div>
              <div class="flex-1 mx-2">
                <div class="h-7 bg-gray-100 rounded overflow-hidden">
                  <div class="h-full bg-amber-500 rounded" :style="{ width: employmentStatus.jobHunting + '%' }"></div>
                </div>
              </div>
              <div class="w-14 text-right"><span class="text-amber-600 font-bold text-base">{{ employmentStatus.jobHunting }}%</span></div>
            </div>
            <div class="flex items-center">
              <div class="w-16 text-gray-600 text-base">待帮扶</div>
              <div class="flex-1 mx-2">
                <div class="h-7 bg-gray-100 rounded overflow-hidden">
                  <div class="h-full bg-red-500 rounded" :style="{ width: employmentStatus.needsHelp + '%' }"></div>
                </div>
              </div>
              <div class="w-14 text-right"><span class="text-red-600 font-bold text-base">{{ employmentStatus.needsHelp }}%</span></div>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <div class="flex items-center space-x-3 mb-5">
            <div class="w-14 h-14 bg-purple-100 rounded-2xl flex items-center justify-center flex-shrink-0">
              <i class="fas fa-building text-purple-600 text-2xl"></i>
            </div>
            <h3 class="text-lg font-bold text-gray-900">重点关注</h3>
          </div>
          <div class="space-y-3">
            <div class="flex items-center p-4 bg-red-50 border border-red-100 rounded-2xl">
              <i class="fas fa-exclamation-circle text-red-500 mr-3 text-xl"></i>
              <span class="text-gray-700 text-base">待帮扶学生</span>
              <span class="ml-auto text-red-600 font-bold text-base">{{ alerts.pendingStudents }}人</span>
            </div>
            <div class="flex items-center p-4 bg-yellow-50 border border-yellow-100 rounded-2xl">
              <i class="fas fa-clock text-yellow-500 mr-3 text-xl"></i>
              <span class="text-gray-700 text-base">待审核岗位</span>
              <span class="ml-auto text-yellow-600 font-bold text-base">{{ alerts.pendingJobs }}个</span>
            </div>
            <div class="flex items-center p-4 bg-blue-50 border border-blue-100 rounded-2xl">
              <i class="fas fa-building text-blue-500 mr-3 text-xl"></i>
              <span class="text-gray-700 text-base">新注册企业</span>
              <span class="ml-auto text-blue-600 font-bold text-base">{{ alerts.newCompanies }}家</span>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-4 gap-6 mb-6">
        <div class="col-span-2 bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <div class="flex items-center space-x-3 mb-5">
            <div class="w-14 h-14 bg-indigo-100 rounded-2xl flex items-center justify-center flex-shrink-0">
              <i class="fas fa-chart-bar text-indigo-600 text-2xl"></i>
            </div>
            <h3 class="text-lg font-bold text-gray-900">各学院就业数</h3>
          </div>
          <div ref="collegeChartRef" class="w-full" style="height: 260px"></div>
        </div>

        <div class="col-span-2 bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <div class="flex items-center space-x-3 mb-5">
            <div class="w-14 h-14 bg-cyan-100 rounded-2xl flex items-center justify-center flex-shrink-0">
              <i class="fas fa-filter text-cyan-600 text-2xl"></i>
            </div>
            <h3 class="text-lg font-bold text-gray-900">求职转化漏斗</h3>
          </div>
          <div ref="funnelChartRef" class="w-full" style="height: 240px"></div>
        </div>

      </div>

      <div class="grid grid-cols-3 gap-6 mb-6">
        <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <div class="flex items-center space-x-3 mb-5">
            <div class="w-14 h-14 bg-blue-100 rounded-2xl flex items-center justify-center flex-shrink-0">
              <i class="fas fa-building text-blue-600 text-2xl"></i>
            </div>
            <h3 class="text-lg font-bold text-gray-900">企业性质</h3>
          </div>
          <div ref="companyTypeChartRef" class="w-full" style="height: 280px"></div>
        </div>
        <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <div class="flex items-center space-x-3 mb-5">
            <div class="w-14 h-14 bg-green-100 rounded-2xl flex items-center justify-center flex-shrink-0">
              <i class="fas fa-money-bill text-green-600 text-2xl"></i>
            </div>
            <h3 class="text-lg font-bold text-gray-900">薪资区间</h3>
          </div>
          <div ref="salaryChartRef" class="w-full" style="height: 280px"></div>
        </div>
        <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <div class="flex items-center space-x-3 mb-5">
            <div class="w-14 h-14 bg-purple-100 rounded-2xl flex items-center justify-center flex-shrink-0">
              <i class="fas fa-calendar-alt text-purple-600 text-2xl"></i>
            </div>
            <h3 class="text-lg font-bold text-gray-900">招聘活动</h3>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div class="bg-blue-50 rounded-2xl p-4 text-center">
              <p class="text-3xl font-bold text-blue-600">{{ activityStats.careerTalks }}</p>
              <p class="text-gray-500 text-base">宣讲会</p>
            </div>
            <div class="bg-purple-50 rounded-2xl p-4 text-center">
              <p class="text-3xl font-bold text-purple-600">{{ activityStats.jobFairs }}</p>
              <p class="text-gray-500 text-base">招聘会</p>
            </div>
            <div class="bg-emerald-50 rounded-2xl p-4 text-center">
              <p class="text-3xl font-bold text-emerald-600">{{ activityStats.participants.toLocaleString() }}</p>
              <p class="text-gray-500 text-base">参会人次</p>
            </div>
            <div class="bg-orange-50 rounded-2xl p-4 text-center">
              <p class="text-3xl font-bold text-orange-600">{{ activityStats.companies.toLocaleString() }}</p>
              <p class="text-gray-500 text-base">入驻企业</p>
            </div>
          </div>
        </div>

      </div>

      <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
        <div class="flex items-center space-x-3 mb-4">
          <div class="w-12 h-12 bg-indigo-100 rounded-xl flex items-center justify-center">
            <i class="fas fa-map-marked-alt text-indigo-600 text-xl"></i>
          </div>
          <h3 class="text-lg font-bold text-gray-900">就业区域分布</h3>
        </div>
        <div ref="chinaMapRef" class="w-full" style="height: 600px"></div>
        <div class="flex items-center justify-center flex-wrap gap-4 mt-4">
          <div v-for="city in chinaCityData" :key="city.name" class="flex items-center space-x-2">
            <div class="w-4 h-4 rounded-full border-2 border-white shadow" :style="{ background: city.color }"></div>
            <span class="text-base text-gray-600">{{ city.name }} {{ city.percent }}%</span>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
// ✅ 给组件命名，配合 keep-alive 的 include 使用
defineOptions({ name: 'Dashboard' })

import { ref, reactive, computed, onMounted, onActivated, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { adminAPI } from '@/api/index'

const currentTime = ref('')
let timer = null
const lastUpdateTime = ref('')
const chinaMapRef = ref(null)
let chinaMapChart = null
const collegeChartRef = ref(null)
let collegeChart = null
const companyTypeChartRef = ref(null)
let companyTypeChart = null
const salaryChartRef = ref(null)
let salaryChart = null
const funnelChartRef = ref(null)
let funnelChart = null

const stats = ref({
  totalStudents: 0,
  employmentRate: 0,
  employedStudents: 0,
  totalJobs: 0,
  totalCompanies: 0
})

const employmentStatus = reactive({
  signed: 0,
  offer: 0,
  jobHunting: 0,
  needsHelp: 0
})

const collegeEmployment = reactive([])

const regionFlow = reactive([])

const CITY_COORDS = {
  '北京': [116.46, 39.92], '上海': [121.48, 31.22], '深圳': [114.07, 22.62],
  '杭州': [120.19, 30.26], '广州': [113.23, 23.16], '成都': [104.06, 30.67],
  '武汉': [114.31, 30.52], '南京': [118.78, 32.04], '西安': [108.95, 34.27],
  '天津': [117.2, 39.13], '重庆': [106.54, 29.59], '青岛': [120.38, 36.07],
  '厦门': [118.11, 24.49], '苏州': [120.62, 31.32], '郑州': [113.65, 34.76],
  '长沙': [112.94, 28.23], '大连': [121.62, 38.92]
}
const PROVINCE_COORDS = {
  '广东': [113.27, 23.13], '江苏': [118.78, 32.06], '山东': [118.4, 36.26],
  '浙江': [120.15, 30.28], '广西': [108.33, 22.84], '四川': [104.07, 30.67],
  '河北': [114.52, 38.05], '安徽': [117.28, 31.86], '辽宁': [123.43, 41.8],
  '河南': [113.65, 34.76], '湖北': [114.31, 30.58], '湖南': [112.94, 28.24],
  '陕西': [108.95, 34.27], '福建': [119.3, 26.08], '黑龙江': [126.53, 45.8],
  '吉林': [125.32, 43.82], '山西': [112.53, 37.87], '云南': [102.71, 25.04],
  '贵州': [106.71, 26.57], '甘肃': [103.84, 36.07], '江西': [115.89, 28.68],
  '内蒙古': [111.77, 40.84], '新疆': [87.62, 43.83], '海南': [110.35, 20.02],
  '青海': [101.78, 36.62], '宁夏': [106.26, 38.47], '西藏': [91.12, 29.66],
  '北京': [116.46, 39.92], '天津': [117.2, 39.13], '上海': [121.48, 31.22],
  '重庆': [106.54, 29.59]
}
const MAP_COLORS = ['#10b981', '#3b82f6', '#8b5cf6', '#06b6d4', '#f97316', '#a855f7', '#ec4899']

const chinaCityData = reactive([])
const funnelSteps = ref([])
const companyScaleChartData = ref([])

const salaryRanges = reactive([])

const activityStats = reactive({
  careerTalks: 0,
  jobFairs: 0,
  participants: 0,
  companies: 0
})

const alerts = reactive({
  pendingStudents: 0,
  pendingJobs: 0,
  newCompanies: 0
})

const circumference = 2 * Math.PI * 52
const progressOffset = computed(() => {
  const progress = stats.employmentRate / 100
  return circumference * (1 - progress)
})

function updateTime() {
  const now = new Date()
  currentTime.value = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')} ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`
}

async function fetchDashboardData() {
  try {
    const res = await adminAPI.getStatistics()
    if (res?.data) {
      const d = res.data
      stats.value.totalStudents = d.total_students ?? 0
      stats.value.employedStudents = d.employed_count ?? 0
      stats.value.employmentRate = d.employment_rate ?? 0
      stats.value.totalJobs = d.total_jobs ?? 0
      stats.value.totalCompanies = d.total_companies ?? 0

      const total = d.total_students || 1
      employmentStatus.signed = d.signed_count ? Math.round(d.signed_count / total * 1000) / 10 : 0
      employmentStatus.offer = d.offered_count ? Math.round(d.offered_count / total * 1000) / 10 : 0
      employmentStatus.jobHunting = d.searching_count ? Math.round(d.searching_count / total * 1000) / 10 : 0
      employmentStatus.needsHelp = d.need_help_count ? Math.round(d.need_help_count / total * 1000) / 10 : 0

      alerts.pendingStudents = d.need_help_count ?? 0
      alerts.pendingJobs = d.pending_job_count ?? 0
      alerts.newCompanies = d.pending_company_count ?? 0
      activityStats.companies = d.total_companies ?? 0
    }
  } catch (error) {
    console.error('Failed to fetch dashboard data:', error)
  }
}

async function fetchDepartmentStats() {
  try {
    const res = await adminAPI.getDepartmentStats()
    console.log('Department stats response:', res.data)
    if (res?.data && Array.isArray(res.data)) {
      const colors = ['emerald', 'blue', 'purple', 'cyan', 'orange', 'pink', 'indigo', 'teal']
      collegeEmployment.length = 0
      res.data.slice(0, 6).forEach((item, i) => {
        console.log('Department item:', item)
        const rate = item.employment_rate ?? (item.total > 0 ? Math.round(item.employed / item.total * 100 * 10) / 10 : 0)
        collegeEmployment.push({
          name: item.department || '未知学院',
          rate,
          employed: item.employed || 0,
          change: 0,
          bgClass: `from-${colors[i % colors.length]}-50 to-${colors[i % colors.length]}-100 border-${colors[i % colors.length]}-200`,
          textClass: `text-${colors[i % colors.length]}-600`
        })
      })
      console.log('collegeEmployment:', collegeEmployment)
      if (collegeChart) {
        collegeChart.dispose()
        collegeChart = null
      }
      initCollegeChart()
    }
  } catch (error) {
    console.error('Failed to fetch department stats:', error)
  }
}

async function fetchConversionFunnel() {
  try {
    const res = await adminAPI.getConversionFunnel()
    if (res?.data && Array.isArray(res.data)) {
      funnelSteps.value = res.data
      if (funnelChart) {
        funnelChart.dispose()
        funnelChart = null
      }
      initFunnelChart()
    }
  } catch (error) {
    console.error('Failed to fetch conversion funnel:', error)
  }
}

async function fetchCompanyScale() {
  try {
    const res = await adminAPI.getCompanyScaleDistribution()
    if (res?.data && Array.isArray(res.data)) {
      const total = res.data.reduce((s, i) => s + (i.value || 0), 0) || 1
      companyScaleChartData.value = res.data.map((item, i) => ({
        name: item.name,
        value: item.value,
        percent: Math.round((item.value / total) * 1000) / 10
      }))
      if (companyTypeChart) {
        companyTypeChart.dispose()
        companyTypeChart = null
      }
      initCompanyTypeChart()
    }
  } catch (error) {
    console.error('Failed to fetch company scale:', error)
  }
}

async function fetchActivityStats() {
  try {
    const res = await adminAPI.getActivityStats()
    if (res?.data) {
      const d = res.data
      activityStats.careerTalks = d.total_talks ?? 0
      activityStats.jobFairs = d.pending_talks ?? 0
      activityStats.participants = d.total_registrations ?? 0
      activityStats.companies = stats.value.totalCompanies
    }
  } catch (error) {
    console.error('Failed to fetch activity stats:', error)
  }
}

async function fetchRegionForMap() {
  try {
    const res = await adminAPI.getRegionDistribution()
    if (res?.data && Array.isArray(res.data)) {
      chinaCityData.length = 0
      res.data.slice(0, 10).forEach((item, i) => {
        const name = (item.region || '').replace('市', '').trim()
        if (name && name !== '未就业' && name !== '未知') {
          chinaCityData.push({
            name,
            percent: item.percentage || 0,
            color: MAP_COLORS[i % MAP_COLORS.length]
          })
        }
      })
      regionFlow.length = 0
      chinaCityData.forEach((city, i) => {
        regionFlow.push({
          name: city.name,
          percent: city.percent,
          style: {
            top: `${20 + (i % 3) * 15}%`,
            left: `${50 + (i % 4) * 8}%`,
            width: `${32 + city.percent}px`,
            height: `${32 + city.percent}px`,
            background: `linear-gradient(135deg, ${city.color}99, ${city.color})`
          }
        })
      })
      if (chinaMapChart) {
        chinaMapChart.dispose()
        chinaMapChart = null
      }
      initChinaMap()
    }
  } catch (error) {
    console.error('Failed to fetch region distribution:', error)
  }
}

async function fetchSalaryDistribution() {
  try {
    const res = await adminAPI.getSalaryDistribution()
    if (res?.data && Array.isArray(res.data) && res.data.length > 0) {
      const total = res.data.reduce((sum, item) => sum + (item.count || 0), 0) || 1
      salaryRanges.length = 0
      res.data.forEach(item => {
        salaryRanges.push({
          range: item.range,
          percent: Math.round((item.count || 0) / total * 100 * 10) / 10
        })
      })
      if (salaryChart) {
        salaryChart.dispose()
        salaryChart = null
      }
      initSalaryChart()
    }
  } catch (error) {
    console.error('Failed to fetch salary distribution:', error)
  }
}

async function initChinaMap() {
  if (!chinaMapRef.value) return
  try {
    // ✅ 优先用预加载的 GeoJSON
    let geoJson = window.__chinaGeoJson
    if (!geoJson) {
      const resp = await fetch('/china.json')
      geoJson = await resp.json()
    }
    echarts.registerMap('china', geoJson)
    chinaMapChart = echarts.init(chinaMapRef.value)

    const scatterData = chinaCityData.map((city) => {
      let coords = CITY_COORDS[city.name]
      if (!coords) {
        coords = PROVINCE_COORDS[city.name]
      }
      if (!coords) {
        const altNames = {
          '北京': [116.46, 39.92], '上海': [121.48, 31.22], '深圳': [114.07, 22.62],
          '广州': [113.23, 23.16], '成都': [104.06, 30.67], '武汉': [114.31, 30.52],
          '南京': [118.78, 32.04], '西安': [108.95, 34.27], '天津': [117.2, 39.13],
          '重庆': [106.54, 29.59], '青岛': [120.38, 36.07], '苏州': [120.62, 31.32],
          '郑州': [113.65, 34.76], '长沙': [112.94, 28.23], '大连': [121.62, 38.92],
          '沈阳': [123.43, 41.8], '济南': [116.98, 36.67], '福州': [119.3, 26.08],
          '南昌': [115.89, 28.68], '昆明': [102.71, 25.04], '哈尔滨': [126.63, 45.75],
          '长春': [125.32, 43.82], '石家庄': [114.48, 38.03], '太原': [112.53, 37.87],
          '兰州': [103.84, 36.13], '贵阳': [106.71, 26.57], '南宁': [108.33, 22.84],
          '合肥': [117.28, 31.86], '杭州': [120.19, 30.26], '宁波': [121.55, 29.87],
          '厦门': [118.11, 24.49], '东莞': [113.75, 23.04], '佛山': [113.12, 23.02]
        }
        coords = altNames[city.name] || altNames[city.name.replace('市', '')]
        if (!coords) coords = [105, 35]
      }
      return {
        name: city.name,
        value: [...coords, city.percent],
        symbolSize: Math.max(city.percent * 0.8, 12),
        itemStyle: { color: city.color }
      }
    })

    if (scatterData.length === 0) {
      return
    }

    const effectScatterData = scatterData.filter(d => d.value[2] >= 18)
    const scatterOnlyData = scatterData.filter(d => d.value[2] < 18)

    const option = {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'item',
        formatter: function(params) {
          if (params.seriesType === 'effectScatter' || params.seriesType === 'scatter') {
            return params.name + '<br/>就业占比：' + params.value[2] + '%'
          }
          return params.name
        }
      },
      geo: {
        map: 'china',
        roam: false,
        zoom: 1.6,
        center: [105, 36],
        label: { show: false },
        itemStyle: {
          areaColor: '#e8e8e8',
          borderColor: '#999',
          borderWidth: 0.5
        },
        emphasis: {
          label: { show: false },
          itemStyle: {
            areaColor: '#d0d0d0',
            borderColor: '#666',
            borderWidth: 1
          }
        }
      },
      series: [
        {
          type: 'effectScatter',
          coordinateSystem: 'geo',
          data: effectScatterData,
          symbolSize: function(val) { return Math.max(val[2] * 1.5, 15) },
          showEffectOn: 'render',
          rippleEffect: {
            brushType: 'stroke',
            scale: 3,
            period: 6
          },
          label: {
            show: true,
            position: 'right',
            formatter: '{b}',
            fontSize: 12,
            fontWeight: 'bold',
            color: '#374151',
            offset: [5, 0]
          },
          itemStyle: { shadowBlur: 10, shadowColor: 'rgba(0,0,0,0.3)' }
        },
        {
          type: 'scatter',
          coordinateSystem: 'geo',
          data: scatterOnlyData,
          symbolSize: function(val) { return Math.max(val[2] + 12, 15) },
          label: {
            show: true,
            position: 'right',
            formatter: '{b}',
            fontSize: 11,
            color: '#6b7280',
            offset: [5, 0]
          },
          itemStyle: { shadowBlur: 10, shadowColor: 'rgba(0,0,0,0.3)' }
        }
      ]
    }

    chinaMapChart.setOption(option)
    window.addEventListener('resize', handleChinaMapResize)
  } catch (error) {
    console.error('Failed to load China map:', error)
  }
}

function handleChinaMapResize() {
  chinaMapChart?.resize()
}

// ✅ 单个大对象存所有 dashboard 数据（一次请求拿到）
const allData = ref(null)
const isLoading = ref(true)

// ✅ 只发一个请求：/admin/statistics/all
async function loadAllData(force = false) {
  isLoading.value = true
  try {
    const res = await adminAPI.get('/admin/statistics/all')
    if (res?.data) {
      const isFirstLoad = !allData.value
      allData.value = res.data
      // 首次加载或数据变化才分发到 UI（force 刷新时也强制重绘）
      if (isFirstLoad || force) {
        applyDataToUI(res.data)
      }
    }
  } catch (error) {
    console.error('加载 dashboard 数据失败:', error)
  } finally {
    isLoading.value = false
    const now = new Date()
    lastUpdateTime.value = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`
  }
}

// 把聚合数据分发到各个 UI 用的 ref
function applyDataToUI(d) {
  // 基础统计
  stats.value.totalStudents = d.total_students ?? 0
  stats.value.employedStudents = d.employed_count ?? 0
  stats.value.employmentRate = d.employment_rate ?? 0
  stats.value.totalJobs = d.total_jobs ?? 0
  stats.value.totalCompanies = d.total_companies ?? 0
  stats.value.totalApplications = d.total_applications ?? 0
  stats.value.avgOfferSalary = d.avg_offer_salary ?? 0

  // 就业状态百分比
  const total = d.total_students || 1
  employmentStatus.signed = total ? Math.round((d.signed_count || 0) / total * 1000) / 10 : 0
  employmentStatus.offer = total ? Math.round((d.offered_count || 0) / total * 1000) / 10 : 0
  employmentStatus.jobHunting = total ? Math.round((d.searching_count || 0) / total * 1000) / 10 : 0
  employmentStatus.furtherStudy = total ? Math.round((d.further_study_count || 0) / total * 1000) / 10 : 0
  employmentStatus.unemployed = total ? Math.round((d.unemployed_count || 0) / total * 1000) / 10 : 0
  employmentStatus.startup = total ? Math.round((d.startup_count || 0) / total * 1000) / 10 : 0
  employmentStatus.needsHelp = total ? Math.round((d.need_help_count || 0) / total * 1000) / 10 : 0

  // 预警
  alerts.pendingStudents = d.need_help_count ?? 0
  alerts.pendingJobs = d.pending_job_count ?? 0
  alerts.newCompanies = d.pending_company_count ?? 0

  // 活动
  const ac = d.activity_stats || {}
  activityStats.careerTalks = ac.total_talks ?? 0
  activityStats.jobFairs = ac.pending_talks ?? 0
  activityStats.participants = ac.total_registrations ?? 0
  activityStats.companies = d.total_companies ?? 0

  // 学院就业率
  collegeEmployment.length = 0
  const colors = ['emerald', 'blue', 'purple', 'cyan', 'orange', 'pink', 'indigo', 'teal']
  ;(d.department_stats || []).slice(0, 6).forEach((item, i) => {
    collegeEmployment.push({
      name: item.department || '未知学院',
      rate: item.employment_rate ?? 0,
      employed: item.employed || 0,
      change: 0,
      bgClass: `from-${colors[i % colors.length]}-50 to-${colors[i % colors.length]}-100 border-${colors[i % colors.length]}-200`,
      textClass: `text-${colors[i % colors.length]}-600`
    })
  })

  // 转化漏斗
  funnelSteps.value = d.funnel_steps || []
  if (funnelChart) { funnelChart.dispose(); funnelChart = null }
  initFunnelChart()

  // 企业规模
  const scaleTotal = (d.company_scale_distribution || []).reduce((s, i) => s + (i.value || 0), 0) || 1
  companyScaleChartData.value = (d.company_scale_distribution || []).map((item, i) => ({
    name: item.name, value: item.value,
    percent: Math.round((item.value / scaleTotal) * 1000) / 10
  }))
  if (companyTypeChart) { companyTypeChart.dispose(); companyTypeChart = null }
  initCompanyTypeChart()

  // 地区分布
  chinaCityData.length = 0
  ;(d.region_distribution || []).slice(0, 10).forEach((item, i) => {
    const name = (item.region || '').replace('市', '').trim()
    if (name && name !== '未就业' && name !== '未知') {
      chinaCityData.push({ name, percent: item.percentage || 0, color: MAP_COLORS[i % MAP_COLORS.length] })
    }
  })
  regionFlow.length = 0
  chinaCityData.forEach((city, i) => {
    regionFlow.push({
      name: city.name, percent: city.percent,
      style: {
        top: `${20 + (i % 3) * 15}%`, left: `${50 + (i % 4) * 8}%`,
        width: `${32 + city.percent}px`, height: `${32 + city.percent}px`,
        background: `linear-gradient(135deg, ${city.color}99, ${city.color})`
      }
    })
  })
  if (chinaMapChart) { chinaMapChart.dispose(); chinaMapChart = null }
  initChinaMap()

  // 薪资分布
  const salaryTotal = (d.salary_distribution || []).reduce((s, i) => s + (i.count || 0), 0) || 1
  salaryRanges.length = 0
  ;(d.salary_distribution || []).forEach(item => {
    salaryRanges.push({
      range: item.range,
      percent: Math.round((item.count || 0) / salaryTotal * 100 * 10) / 10
    })
  })
  if (salaryChart) { salaryChart.dispose(); salaryChart = null }
  initSalaryChart()
}

// ✅ 首次挂载时加载（先拿数据再 init 图表，避免空数据闪一下再重绘）
onMounted(async () => {
  updateTime()
  timer = setInterval(updateTime, 1000)
  // 并行：拉数据 + 预加载 china.json（节省 200-500ms）
  await Promise.all([
    loadAllData(),
    fetch('/china.json').then(r => r.json()).then(g => { window.__chinaGeoJson = g }).catch(() => {}),
  ])
  // 数据回来后统一初始化所有图表
  initCollegeChart()
  initCompanyTypeChart()
  initSalaryChart()
  initFunnelChart()
  initChinaMap()
})

// ✅ 组件被 keep-alive 激活时（从其他页面切回来），如果超过 30 秒才重新加载
let lastLoadTimestamp = 0
onActivated(() => {
  const now = Date.now()
  if (now - lastLoadTimestamp > 30000) {  // 30 秒内不重复加载
    loadAllData(true)  // 强制刷新
  }
  lastLoadTimestamp = now
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
  if (chinaMapChart) {
    chinaMapChart.dispose()
    chinaMapChart = null
  }
  if (collegeChart) {
    collegeChart.dispose()
    collegeChart = null
  }
  if (companyTypeChart) {
    companyTypeChart.dispose()
    companyTypeChart = null
  }
  if (salaryChart) {
    salaryChart.dispose()
    salaryChart = null
  }
  if (funnelChart) {
    funnelChart.dispose()
    funnelChart = null
  }
  window.removeEventListener('resize', handleChinaMapResize)
})

function initCollegeChart() {
  if (!collegeChartRef.value) return
  collegeChart = echarts.init(collegeChartRef.value)

  const chartData = collegeEmployment.map(c => ({
    name: c.name,
    value: c.employed || 0
  }))

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      formatter: '{b}: {c}人'
    },
    grid: { left: '3%', right: '4%', bottom: '3%', top: '8%', containLabel: true },
    xAxis: {
      type: 'category',
      data: chartData.map(d => d.name),
      axisLabel: { fontSize: 12, color: '#6b7280', rotate: 30 }
    },
    yAxis: { type: 'value', axisLabel: { fontSize: 12, color: '#6b7280' } },
    series: [{
      type: 'bar',
      data: chartData.map((d, i) => ({
        value: d.value,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: ['#818cf8', '#6366f1', '#4f46e5'][i % 3] },
            { offset: 1, color: ['#a5b4fc', '#93c5fd', '#67e8f9'][i % 3] }
          ])
        }
      })),
      barWidth: '50%',
      label: { show: true, position: 'top', fontSize: 12, color: '#374151' }
    }]
  }

  collegeChart.setOption(option)

  window.addEventListener('resize', () => collegeChart?.resize())
}

function initCompanyTypeChart() {
  if (!companyTypeChartRef.value) return
  companyTypeChart = echarts.init(companyTypeChartRef.value)

  const chartData = (companyScaleChartData.value.length ? companyScaleChartData.value : [{ name: '暂无', value: 1, percent: 100 }]).map(c => ({
    name: c.name,
    value: c.percent
  }))

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c}%'
    },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: true,
      itemStyle: {
        borderRadius: 8,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: true,
        formatter: '{b}\n{c}%',
        fontSize: 12,
        color: '#374151'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 14,
          fontWeight: 'bold'
        }
      },
      data: chartData.map((d, i) => ({
        ...d,
        itemStyle: {
          color: ['#3b82f6', '#10b981', '#8b5cf6', '#f97316'][i % 4]
        }
      }))
    }]
  }

  companyTypeChart.setOption(option)
  window.addEventListener('resize', () => companyTypeChart?.resize())
}

function initSalaryChart() {
  if (!salaryChartRef.value) return
  salaryChart = echarts.init(salaryChartRef.value)

  const chartData = salaryRanges.map(c => ({
    name: c.range,
    value: c.percent
  }))

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      formatter: '{b}: {c}%'
    },
    grid: { left: '8%', right: '4%', bottom: '3%', top: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: chartData.map(d => d.name),
      axisLabel: { fontSize: 11, color: '#6b7280' }
    },
    yAxis: {
      type: 'value',
      max: 60,
      axisLabel: { fontSize: 11, color: '#6b7280', formatter: (value) => value + '%' },
      splitLine: { lineStyle: { color: '#f0f0f0' } }
    },
    series: [{
      type: 'bar',
      data: chartData.map((d, i) => ({
        value: d.value,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#10b981' },
            { offset: 1, color: '#34d399' }
          ]),
          borderRadius: [4, 4, 0, 0]
        }
      })),
      barWidth: '50%',
      label: { show: true, position: 'top', fontSize: 11, color: '#374151', formatter: '{c}%' }
    }]
  }

  salaryChart.setOption(option)
  window.addEventListener('resize', () => salaryChart?.resize())
}

function initFunnelChart() {
  if (!funnelChartRef.value) return
  funnelChart = echarts.init(funnelChartRef.value)

  const chartData = funnelSteps.value.length
    ? funnelSteps.value.map(s => ({ name: s.name, value: s.value }))
    : [{ name: '暂无数据', value: 0 }]

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c}人'
    },
    series: [{
      type: 'funnel',
      left: '10%',
      top: '10%',
      bottom: '10%',
      width: '80%',
      min: 0,
      max: Math.max(...chartData.map(d => d.value), 1),
      minSize: '20%',
      maxSize: '100%',
      sort: 'descending',
      gap: 4,
      label: {
        show: true,
        position: 'inside',
        formatter: '{b}\n{c}人',
        fontSize: 13,
        color: '#fff'
      },
      itemStyle: {
        borderColor: '#fff',
        borderWidth: 2
      },
      data: chartData.map((d, i) => ({
        ...d,
        itemStyle: {
          color: ['#3b82f6', '#8b5cf6', '#10b981', '#22c55e'][i]
        }
      }))
    }]
  }

  funnelChart.setOption(option)
  window.addEventListener('resize', () => funnelChart?.resize())
}
</script>

<style scoped>
.gradient-text {
  background: linear-gradient(135deg, #60a5fa, #34d399);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  color: transparent;
}
</style>