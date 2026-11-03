<template>
  <div class="space-y-6">
    <div class="bg-white rounded-2xl p-6 shadow-sm">
      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center space-x-4">
          <h3 class="text-lg font-bold text-gray-900">数据统计</h3>
          <el-select v-model="timeRange" class="w-32">
            <el-option label="近30天" value="30" />
            <el-option label="近90天" value="90" />
            <el-option label="近一年" value="365" />
          </el-select>
        </div>
        <el-button @click="exportReport">
          <i class="fas fa-download mr-2"></i>导出报表
        </el-button>
      </div>

      <div class="grid grid-cols-4 gap-6 mb-6">
        <div class="bg-white rounded-2xl p-6 shadow-sm">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-500 text-sm">简历投递数</p>
              <p class="text-3xl font-bold text-gray-900 mt-1">{{ stats.applications }}</p>
              <p class="text-sm text-green-600 mt-1"><i class="fas fa-arrow-up mr-1"></i>{{ stats.applicationsGrowth }}%</p>
            </div>
            <div class="w-14 h-14 bg-purple-50 rounded-xl flex items-center justify-center">
              <i class="fas fa-file-alt text-purple-500 text-2xl"></i>
            </div>
          </div>
        </div>
        <div class="bg-white rounded-2xl p-6 shadow-sm">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-500 text-sm">简历通过率</p>
              <p class="text-3xl font-bold text-gray-900 mt-1">{{ stats.passRate }}%</p>
              <p class="text-sm text-green-600 mt-1"><i class="fas fa-arrow-up mr-1"></i>{{ stats.passRateGrowth }}%</p>
            </div>
            <div class="w-14 h-14 bg-green-50 rounded-xl flex items-center justify-center">
              <i class="fas fa-check-circle text-green-500 text-2xl"></i>
            </div>
          </div>
        </div>
        <div class="bg-white rounded-2xl p-6 shadow-sm">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-500 text-sm">面试邀请数</p>
              <p class="text-3xl font-bold text-gray-900 mt-1">{{ stats.interviews }}</p>
              <p class="text-sm text-red-600 mt-1"><i class="fas fa-arrow-down mr-1"></i>{{ stats.interviewsGrowth }}%</p>
            </div>
            <div class="w-14 h-14 bg-blue-50 rounded-xl flex items-center justify-center">
              <i class="fas fa-user-check text-blue-500 text-2xl"></i>
            </div>
          </div>
        </div>
        <div class="bg-white rounded-2xl p-6 shadow-sm">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-500 text-sm">发放Offer数</p>
              <p class="text-3xl font-bold text-gray-900 mt-1">{{ stats.offers }}</p>
              <p class="text-sm text-green-600 mt-1"><i class="fas fa-arrow-up mr-1"></i>{{ stats.offersGrowth }}%</p>
            </div>
            <div class="w-14 h-14 bg-yellow-50 rounded-xl flex items-center justify-center">
              <i class="fas fa-handshake text-yellow-500 text-2xl"></i>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-2 gap-6 mb-6">
      <div class="bg-white rounded-2xl p-6 shadow-sm">
        <h3 class="text-lg font-bold text-gray-900 mb-4">招聘漏斗</h3>
        <div ref="funnelChartRef" class="h-72"></div>
      </div>
      <div class="bg-white rounded-2xl p-6 shadow-sm">
        <h3 class="text-lg font-bold text-gray-900 mb-4">投递趋势</h3>
        <div ref="trendChartRef" class="h-72"></div>
      </div>
    </div>

    <div class="grid grid-cols-3 gap-6 mb-6">
      <div class="bg-white rounded-2xl p-6 shadow-sm">
        <h3 class="text-lg font-bold text-gray-900 mb-4">岗位投递分布</h3>
        <div ref="jobDistChartRef" class="h-72"></div>
      </div>
      <div class="bg-white rounded-2xl p-6 shadow-sm">
        <h3 class="text-lg font-bold text-gray-900 mb-4">院校投递排名</h3>
        <div ref="schoolChartRef" class="h-72"></div>
      </div>
      <div class="bg-white rounded-2xl p-6 shadow-sm">
        <h3 class="text-lg font-bold text-gray-900 mb-4">学历分布</h3>
        <div v-if="hasEducationData" ref="educationChartRef" class="h-72"></div>
        <el-empty v-else description="暂无学历分布数据" class="h-72" />
      </div>
    </div>

    <div class="bg-white rounded-2xl p-6 shadow-sm">
      <h3 class="text-lg font-bold text-gray-900 mb-4">岗位效果排行</h3>
      <table class="w-full">
        <thead>
          <tr class="border-b border-gray-100">
            <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">排名</th>
            <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">岗位名称</th>
            <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">投递数</th>
            <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">查看数</th>
            <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">转化率</th>
            <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">状态</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="(job, index) in jobRankings" :key="job.id" class="hover:bg-gray-50">
            <td class="px-4 py-4">
              <span :class="getRankBadgeClass(index)" class="w-6 h-6 text-xs rounded-full flex items-center justify-center">{{ index + 1 }}</span>
            </td>
            <td class="px-4 py-4 font-medium text-gray-900">{{ job.title }}</td>
            <td class="px-4 py-4 text-gray-700">{{ job.applications }}</td>
            <td class="px-4 py-4 text-gray-700">{{ job.views }}</td>
            <td class="px-4 py-4">
              <span :class="getConversionClass(job.conversion)">{{ job.conversion }}%</span>
            </td>
            <td class="px-4 py-4">
              <span :class="job.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'" class="px-2 py-1 text-xs rounded-full">{{ job.status === 'active' ? '招聘中' : '已暂停' }}</span>
            </td>
          </tr>
          <tr v-if="jobRankings.length === 0">
            <td colspan="6" class="px-4 py-8 text-center text-gray-500">暂无数据</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'
import { ElMessage } from 'element-plus'
import { companyAPI } from '@/api'

const timeRange = ref('30')
const funnelChartRef = ref(null)
const trendChartRef = ref(null)
const jobDistChartRef = ref(null)
const schoolChartRef = ref(null)
const educationChartRef = ref(null)

let funnelChart = null
let trendChart = null
let jobDistChart = null
let schoolChart = null
let educationChart = null

const stats = ref({
  applications: 0,
  applicationsGrowth: 0,
  passRate: 0,
  passRateGrowth: 0,
  interviews: 0,
  interviewsGrowth: 0,
  offers: 0,
  offersGrowth: 0
})

const jobRankings = ref([])
const hasEducationData = ref(false)

const getRankBadgeClass = (index) => {
  const classes = [
    'bg-yellow-500 text-white',
    'bg-gray-400 text-white',
    'bg-orange-500 text-white',
    'bg-gray-300 text-gray-600',
    'bg-gray-300 text-gray-600'
  ]
  return classes[index] || classes[3]
}

const getConversionClass = (conversion) => {
  if (conversion >= 17) return 'text-green-600 font-medium'
  if (conversion >= 15) return 'text-yellow-600 font-medium'
  return 'text-gray-600 font-medium'
}

const initCharts = (data) => {
  if (funnelChartRef.value) {
    funnelChart = echarts.init(funnelChartRef.value)
    funnelChart.setOption({
      color: ['#8b5cf6', '#a78bfa', '#c4b5fd', '#ddd6fe', '#ede9fe'],
      tooltip: { trigger: 'item' },
      legend: { bottom: 0 },
      series: [{
        name: '招聘漏斗',
        type: 'funnel',
        left: '10%',
        top: 20,
        bottom: 40,
        width: '80%',
        min: 0,
        max: data.funnel_max || 100,
        minSize: '0%',
        maxSize: '100%',
        gap: 4,
        label: { show: true, position: 'inside', formatter: '{b}: {c}', color: '#fff', fontSize: 12 },
        labelLine: { show: false },
        itemStyle: { borderColor: '#fff', borderWidth: 1 },
        data: data.funnel || [
          { value: 0, name: '简历投递' },
          { value: 0, name: '简历筛选' },
          { value: 0, name: '笔试/面试' },
          { value: 0, name: '发放Offer' },
          { value: 0, name: '签约入职' }
        ]
      }]
    })
  }

  if (trendChartRef.value) {
    trendChart = echarts.init(trendChartRef.value)
    trendChart.setOption({
      tooltip: { trigger: 'axis' },
      legend: { data: ['投递数', '面试邀请'], bottom: 0 },
      grid: { left: '3%', right: '4%', bottom: '15%', top: '10%', containLabel: true },
      xAxis: { type: 'category', boundaryGap: false, data: data.trend_labels || ['暂无数据'] },
      yAxis: { type: 'value' },
      series: [
        { name: '投递数', type: 'line', smooth: true, areaStyle: { color: 'rgba(139, 92, 246, 0.1)' }, lineStyle: { color: '#8b5cf6', width: 3 }, itemStyle: { color: '#8b5cf6' }, data: data.applications_trend || [0] },
        { name: '面试邀请', type: 'line', smooth: true, areaStyle: { color: 'rgba(59, 130, 246, 0.1)' }, lineStyle: { color: '#3b82f6', width: 3 }, itemStyle: { color: '#3b82f6' }, data: data.interviews_trend || [0] }
      ]
    })
  }

  if (jobDistChartRef.value) {
    jobDistChart = echarts.init(jobDistChartRef.value)
    const jobColors = ['#6366f1', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#3b82f6', '#ef4444', '#14b8a6']
    jobDistChart.setOption({
      tooltip: { trigger: 'item' },
      legend: { bottom: 0, left: 'center' },
      series: [{
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: { borderRadius: 8, borderColor: '#fff', borderWidth: 2 },
        label: { show: false },
        emphasis: { label: { show: true, fontSize: 14, fontWeight: 'bold' } },
        data: (data.job_distribution || []).map((item, index) => ({
          ...item,
          itemStyle: { color: jobColors[index % jobColors.length] }
        }))
      }]
    })
  }

  if (schoolChartRef.value) {
    schoolChart = echarts.init(schoolChartRef.value)
    schoolChart.setOption({
      tooltip: { trigger: 'axis' },
      grid: { left: '3%', right: '4%', bottom: '3%', top: '3%', containLabel: true },
      xAxis: { type: 'value' },
      yAxis: { type: 'category', data: data.school_labels || ['暂无数据'] },
      series: [{
        type: 'bar',
        data: data.school_data || [0],
        itemStyle: { color: '#8b5cf6', borderRadius: [0, 4, 4, 0] }
      }]
    })
  }

  if (educationChartRef.value) {
    educationChart = echarts.init(educationChartRef.value)
    educationChart.setOption({
      tooltip: { trigger: 'item' },
      legend: { bottom: 0, left: 'center' },
      series: [{
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: { borderRadius: 8, borderColor: '#fff', borderWidth: 2 },
        label: { show: false },
        emphasis: { label: { show: true, fontSize: 14, fontWeight: 'bold' } },
        data: data.education_distribution || []
      }]
    })
  }

  window.addEventListener('resize', handleResize)
}

const handleResize = () => {
  funnelChart?.resize()
  trendChart?.resize()
  jobDistChart?.resize()
  schoolChart?.resize()
  educationChart?.resize()
}

const fetchAnalytics = async () => {
  try {
    const res = await companyAPI.getAnalytics({ days: timeRange.value })
    const data = res.data

    stats.value = {
      applications: data.total_applications || 0,
      applicationsGrowth: data.applications_growth || 0,
      passRate: data.pass_rate || 0,
      passRateGrowth: data.pass_rate_growth || 0,
      interviews: data.total_interviews || 0,
      interviewsGrowth: data.interviews_growth || 0,
      offers: data.total_offers || 0,
      offersGrowth: data.offers_growth || 0
    }

    jobRankings.value = data.job_rankings || []

    if (funnelChart) {
      funnelChart.setOption({
        series: [{
          data: data.funnel || []
        }]
      })
    }

    if (trendChart) {
      trendChart.setOption({
        xAxis: { data: data.trend_labels || [] },
        series: [
          { data: data.applications_trend || [] },
          { data: data.interviews_trend || [] }
        ]
      })
    }

    if (jobDistChart) {
      const jobColors = ['#6366f1', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#3b82f6', '#ef4444', '#14b8a6']
      jobDistChart.setOption({
        series: [{
          data: (data.job_distribution || []).map((item, index) => ({
            ...item,
            itemStyle: { color: jobColors[index % jobColors.length] }
          }))
        }]
      })
    }

    if (schoolChart) {
      schoolChart.setOption({
        yAxis: { data: data.school_labels || [] },
        series: [{ data: data.school_data || [] }]
      })
    }

    hasEducationData.value = (data.education_distribution || []).length > 0
    if (hasEducationData.value) {
      await nextTick()
      if (educationChartRef.value) {
        if (!educationChart) {
          educationChart = echarts.init(educationChartRef.value)
        }
        educationChart.setOption({
          tooltip: { trigger: 'item' },
          legend: { bottom: 0, left: 'center' },
          series: [{
            type: 'pie',
            radius: ['40%', '70%'],
            data: data.education_distribution || []
          }]
        })
      }
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
    ElMessage.error('获取统计数据失败')
  }
}

watch(timeRange, () => {
  fetchAnalytics()
})

const exportReport = () => {
  ElMessage.success('报表导出中...')
}

onMounted(() => {
  initCharts({})
  fetchAnalytics()
})
</script>