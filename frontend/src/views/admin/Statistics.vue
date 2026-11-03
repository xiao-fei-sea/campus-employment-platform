<template>
  <div class="space-y-6">
    <div class="grid grid-cols-4 gap-6">
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex items-center space-x-5">
        <div class="w-16 h-16 bg-blue-100 rounded-2xl flex items-center justify-center flex-shrink-0">
          <i class="fas fa-chart-pie text-blue-600 text-3xl"></i>
        </div>
        <div>
          <p class="text-gray-500 text-base">就业率</p>
          <p class="text-4xl font-bold text-gray-900">{{ statsData.employmentRate.toFixed(1) }}%</p>
        </div>
      </div>
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex items-center space-x-5">
        <div class="w-16 h-16 bg-emerald-100 rounded-2xl flex items-center justify-center flex-shrink-0">
          <i class="fas fa-handshake text-emerald-600 text-3xl"></i>
        </div>
        <div>
          <p class="text-gray-500 text-base">签约人数</p>
          <p class="text-4xl font-bold text-gray-900">{{ statsData.signedCount.toLocaleString() }}</p>
        </div>
      </div>
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex items-center space-x-5">
        <div class="w-16 h-16 bg-purple-100 rounded-2xl flex items-center justify-center flex-shrink-0">
          <i class="fas fa-briefcase text-purple-600 text-3xl"></i>
        </div>
        <div>
          <p class="text-gray-500 text-base">岗位供需比</p>
          <p class="text-4xl font-bold text-gray-900">{{ statsData.jobSupplyDemand.toLocaleString() }}</p>
        </div>
      </div>
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex items-center space-x-5">
        <div class="w-16 h-16 bg-orange-100 rounded-2xl flex items-center justify-center flex-shrink-0">
          <i class="fas fa-coins text-orange-600 text-3xl"></i>
        </div>
        <div>
          <p class="text-gray-500 text-base">平均薪资</p>
          <p class="text-4xl font-bold text-gray-900">{{ statsData.averageSalary > 0 ? `¥${statsData.averageSalary.toLocaleString()}` : '样本不足' }}</p>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-2 gap-6">
      <div class="bg-white rounded-xl shadow-sm p-6">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-bold text-gray-900">就业状态分布</h3>
        </div>
        <div ref="statusChartRef" class="w-full h-72"></div>
      </div>

      <div class="bg-white rounded-xl shadow-sm p-6">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-bold text-gray-900">各学院就业率对比</h3>
          <el-select v-model="selectedGraduationYear" size="small" class="w-32" @change="onFilterChange">
            <el-option label="全部届别" :value="null" />
            <el-option label="2024届" :value="2024" />
            <el-option label="2025届" :value="2025" />
            <el-option label="2026届" :value="2026" />
          </el-select>
        </div>
        <div ref="majorChartRef" class="w-full h-72"></div>
      </div>
    </div>

    <div class="grid grid-cols-3 gap-6">
      <div class="bg-white rounded-xl shadow-sm p-6">
        <h3 class="text-lg font-bold text-gray-900 mb-6">行业分布</h3>
        <div ref="industryChartRef" class="w-full h-72"></div>
      </div>

      <div class="bg-white rounded-xl shadow-sm p-6">
        <h3 class="text-lg font-bold text-gray-900 mb-6">薪资区间分布</h3>
        <div ref="salaryChartRef" class="w-full h-72"></div>
      </div>

      <div class="bg-white rounded-xl shadow-sm p-6">
        <h3 class="text-lg font-bold text-gray-900 mb-6">就业区域热力图</h3>
        <div ref="regionChartRef" class="w-full h-80"></div>
      </div>
    </div>

    <div class="bg-white rounded-xl shadow-sm p-6">
      <h3 class="text-lg font-bold text-gray-900 mb-4">就业趋势（近30日）</h3>
      <div ref="trendChartRef" class="w-full h-80 mb-6"></div>
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-bold text-gray-900">就业数据明细</h3>
        <el-button type="primary" @click="exportReport">
          <i class="fas fa-download mr-2"></i>导出报表
        </el-button>
      </div>
      <el-table :data="tableData" stripe>
        <el-table-column label="院系" prop="department" />
        <el-table-column label="专业" prop="major" />
        <el-table-column label="毕业生数" prop="total" align="center" />
        <el-table-column label="已就业" prop="employed" align="center" />
        <el-table-column label="就业率" prop="rate" align="center">
          <template #default="{ row }">
            <span class="text-emerald-600 font-medium">{{ row.rate }}%</span>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
defineOptions({ name: 'Statistics' })
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import { ElMessage } from 'element-plus'
import { adminAPI } from '@/api/index'

let chinaMapData = null

async function loadChinaMap() {
  if (chinaMapData) return chinaMapData
  try {
    const response = await fetch('https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json')
    chinaMapData = await response.json()
    echarts.registerMap('china', chinaMapData)
    return chinaMapData
  } catch (error) {
    console.error('加载中国地图失败:', error)
    return null
  }
}

const statusChartRef = ref(null)
const majorChartRef = ref(null)
const industryChartRef = ref(null)
const salaryChartRef = ref(null)
const regionChartRef = ref(null)
const trendChartRef = ref(null)

const selectedGraduationYear = ref(null)
let trendChart = null

const statsData = ref({
  employmentRate: 0,
  change: 0,
  signedCount: 0,
  jobSupplyDemand: 0,
  averageSalary: 0
})

const employmentStatusData = ref([])
const majorData = ref([])
const industryData = ref([])
const salaryData = ref([])
const regionData = ref([])
const regionDetailData = ref(null)
const currentProvince = ref(null)
const cityData = ref([])
let regionChart = null
let chinaMap = null

const colors = [
  { color: 'bg-blue-500', barColor: 'bg-blue-500' },
  { color: 'bg-purple-500', barColor: 'bg-purple-500' },
  { color: 'bg-emerald-500', barColor: 'bg-emerald-500' },
  { color: 'bg-orange-500', barColor: 'bg-orange-500' },
  { color: 'bg-pink-500', barColor: 'bg-pink-500' },
  { color: 'bg-red-500', barColor: 'bg-red-500' },
  { color: 'bg-indigo-500', barColor: 'bg-indigo-500' },
  { color: 'bg-cyan-500', barColor: 'bg-cyan-500' },
  { color: 'bg-yellow-500', barColor: 'bg-yellow-500' },
  { color: 'bg-teal-500', barColor: 'bg-teal-500' }
]

const industryColors = ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#6b7280', '#ef4444', '#14b8a6', '#f97316']

async function fetchEmploymentStatusData() {
  try {
    console.log('正在获取就业状态分布...')
    const res = await adminAPI.getEmploymentStatusDistribution()
    console.log('就业状态分布响应:', res)
    if (res.data) {
      const data = Array.isArray(res.data) ? res.data : res.data.data || []
      employmentStatusData.value = data.map(item => ({
        name: item.name || '',
        value: item.value || 0,
        percentage: item.percentage || 0
      }))
      console.log('就业状态分布已设置:', employmentStatusData.value)
    }
  } catch (error) {
    console.error('获取就业状态分布失败:', error)
    ElMessage.error('获取就业状态数据失败')
  }
}

async function fetchMajorData() {
  try {
    console.log('正在获取学院就业率...')
    const res = await adminAPI.get('/admin/statistics/department-stats')
    console.log('学院就业率响应:', res)
    if (res.data) {
      const data = Array.isArray(res.data) ? res.data : res.data.data || []
      majorData.value = data.map(item => ({
        name: item.department || item.name || '',
        value: item.total > 0 ? Math.round((item.employed / item.total) * 100) : 0
      }))
      console.log('学院就业率已设置:', majorData.value)
    }
  } catch (error) {
    console.error('获取学院就业率失败:', error)
    ElMessage.error('获取学院就业率失败')
  }
}

async function fetchIndustryData() {
  try {
    console.log('正在获取行业数据...')
    const res = await adminAPI.get('/admin/statistics/stats')
    console.log('行业数据响应:', res)
    if (res.data) {
      const distribution = res.data.company_industry_distribution || []
      if (distribution.length > 0) {
        industryData.value = distribution.slice(0, 8).map((item, index) => ({
          name: item.industry || '其他',
          value: item.count || 0
        }))
      } else {
        industryData.value = []
      }
    }
  } catch (error) {
    console.error('获取行业数据失败:', error)
    ElMessage.error('获取行业数据失败')
  }
}

async function fetchSalaryData() {
  try {
    console.log('正在获取薪资数据...')
    const res = await adminAPI.get('/admin/statistics/salary-distribution')
    console.log('薪资数据响应:', res)
    
    if (res.data) {
      const rawData = Array.isArray(res.data) ? res.data : res.data.data || []
      salaryData.value = rawData.map(item => ({
        range: item.range || '',
        count: item.count || 0
      }))
      console.log('薪资数据已设置:', salaryData.value)
    } else {
      console.log('薪资数据为空')
    }
  } catch (error) {
    console.error('获取薪资数据失败:', error)
    ElMessage.error('获取薪资数据失败')
  }
}

async function fetchRegionData() {
  try {
    console.log('正在获取区域数据...')
    const res = await adminAPI.getRegionDistribution()
    console.log('区域分布响应:', res)
    
    if (res.data) {
      const data = Array.isArray(res.data) ? res.data : res.data.data || []
      console.log('正在映射区域数据，长度:', data.length)
      regionData.value = data.slice(0, 15).map((item, index) => ({
        city: item.region || '未知',
        percent: item.percentage || 0,
        count: item.count || 0,
        color: colors[index % colors.length].color,
        barColor: colors[index % colors.length].barColor
      }))
      regionDetailData.value = data.slice(0, 15)

      const cityToProvince = {
        '北京': '北京', '天津': '天津', '上海': '上海', '重庆': '重庆',
        '石家庄': '河北', '太原': '山西', '呼和浩特': '内蒙古', '沈阳': '辽宁',
        '长春': '吉林', '哈尔滨': '黑龙江', '南京': '江苏', '杭州': '浙江',
        '合肥': '安徽', '福州': '福建', '南昌': '江西', '济南': '山东',
        '郑州': '河南', '武汉': '湖北', '长沙': '湖南', '广州': '广东',
        '南宁': '广西', '海口': '海南', '成都': '四川', '贵阳': '贵州',
        '昆明': '云南', '拉萨': '西藏', '西安': '陕西', '兰州': '甘肃',
        '西宁': '青海', '银川': '宁夏', '乌鲁木齐': '新疆', '深圳': '广东',
        '青岛': '山东', '大连': '辽宁', '苏州': '江苏', '厦门': '福建',
        '宁波': '浙江', '无锡': '江苏', '佛山': '广东', '东莞': '广东',
        '珠海': '广东'
      }

      const provinceMap = {}
      regionData.value.forEach(item => {
        const province = cityToProvince[item.city] || item.city
        if (!provinceMap[province]) {
          provinceMap[province] = { count: 0, percent: 0, cities: [] }
        }
        provinceMap[province].count += item.count
        provinceMap[province].percent += item.percent
        provinceMap[province].cities.push(item)
      })

      cityData.value = provinceMap
      console.log('城市数据映射:', regionData.value)
      console.log('省份聚合:', provinceMap)
    } else {
      console.log('没有区域数据或不是数组，res.data类型:', typeof res.data, res.data)
    }
  } catch (error) {
    console.error('获取区域数据失败:', error)
    ElMessage.error('获取区域数据失败')
  }
}

const tableData = ref([])

async function fetchMajorStatsTable() {
  try {
    const params = {}
    if (selectedGraduationYear.value) {
      params.graduation_year = selectedGraduationYear.value
    }
    const res = await adminAPI.getMajorStats(params)
    if (res.data && Array.isArray(res.data)) {
      tableData.value = res.data.map(item => ({
        department: item.college || item.department,
        major: item.major,
        total: item.total,
        employed: item.employed,
        rate: item.employment_rate ?? (item.total > 0 ? ((item.employed / item.total) * 100).toFixed(1) : '0.0')
      }))
    }
  } catch (error) {
    console.error('获取专业统计失败:', error)
  }
}

async function fetchEmploymentTrend() {
  try {
    const res = await adminAPI.getEmploymentTrend({ days: 30 })
    if (!trendChartRef.value || !res.data) return
    if (!trendChart) trendChart = echarts.init(trendChartRef.value)
    const data = Array.isArray(res.data) ? res.data : []
    trendChart.setOption({
      tooltip: { trigger: 'axis' },
      legend: { data: ['新增投递', '新增签约'] },
      grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
      xAxis: { type: 'category', data: data.map(d => d.date) },
      yAxis: { type: 'value' },
      series: [
        { name: '新增投递', type: 'line', smooth: true, data: data.map(d => d.applications), itemStyle: { color: '#3b82f6' } },
        { name: '新增签约', type: 'line', smooth: true, data: data.map(d => d.signed), itemStyle: { color: '#10b981' } }
      ]
    })
  } catch (error) {
    console.error('获取就业趋势失败:', error)
  }
}

function onFilterChange() {
  fetchMajorStatsTable()
}

async function fetchStatistics() {
  try {
    console.log('正在获取统计数据...')
    const res = await adminAPI.get('/admin/statistics/stats')
    console.log('统计数据响应:', res)
    if (res.data) {
      const data = res.data
      statsData.value = {
        employmentRate: data.employment_rate || 0,
        change: 0,
        signedCount: data.signed_count || 0,
        jobSupplyDemand: data.job_supply_demand_ratio || 0,
        averageSalary: data.avg_offer_salary || 0
      }
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

const exportReport = async () => {
  try {
    const res = await adminAPI.exportReport()
    const url = window.URL.createObjectURL(new Blob([res.data], { type: 'text/csv;charset=utf-8' }))
    const link = document.createElement('a')
    link.href = url
    link.download = `students_${new Date().toISOString().slice(0, 10)}.csv`
    link.click()
    window.URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (error) {
    console.error('导出报表失败:', error)
    ElMessage.error('导出失败')
  }
}

onMounted(async () => {
  await Promise.all([
    fetchStatistics(),
    fetchMajorStatsTable(),
    fetchEmploymentStatusData(),
    fetchMajorData(),
    fetchIndustryData(),
    fetchSalaryData(),
    fetchRegionData(),
    fetchEmploymentTrend()
  ])
  initStatusChart()
  initMajorChart()
  initIndustryChart()
  initSalaryChart()
  initRegionChart()

  window.addEventListener('resize', () => {
    statusChart && statusChart.resize()
    majorChart && majorChart.resize()
    industryChart && industryChart.resize()
    salaryChart && salaryChart.resize()
    regionChart && regionChart.resize()
  })
})

function initStatusChart() {
  if (!statusChartRef.value) return
  const statusChart = echarts.init(statusChartRef.value)
  const data = employmentStatusData.value.length > 0 ? employmentStatusData.value : []

  if (data.length === 0) {
    statusChart.setOption({
      title: {
        text: '暂无就业状态数据',
        left: 'center',
        top: 'center',
        textStyle: { color: '#9ca3af', fontSize: 14 }
      }
    })
    return
  }

  const pieColors = ['#10b981', '#f59e0b', '#8b5cf6', '#3b82f6', '#ef4444', '#6b7280']

  statusChart.setOption({
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c}人 ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: '5%',
      top: 'center',
      textStyle: { color: '#374151' }
    },
    series: [{
      name: '就业状态',
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['35%', '50%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 8,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: true,
        position: 'outside',
        formatter: '{b}\n{d}%',
        fontSize: 11
      },
      labelLine: {
        show: true,
        lineStyle: { color: '#9ca3af' }
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 14,
          fontWeight: 'bold'
        },
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.3)'
        }
      },
      data: data.map((item, index) => ({
        name: item.name,
        value: item.value,
        itemStyle: { color: pieColors[index % pieColors.length] }
      }))
    }]
  })
}

function initMajorChart() {
  if (!majorChartRef.value) return
  const majorChart = echarts.init(majorChartRef.value)
  const data = majorData.value.length > 0 ? majorData.value : [{ name: '暂无数据', value: 0 }]
  majorChart.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: data.map(item => item.name)
    },
    yAxis: {
      type: 'value',
      max: 100,
      axisLabel: { formatter: '{value}%' }
    },
    series: [{
      type: 'bar',
      data: data.map((item, index) => ({
        value: item.value,
        itemStyle: {
          color: item.value >= 90 ? '#10b981' : (item.value >= 80 ? '#f59e0b' : '#ef4444'),
          borderRadius: [4, 4, 0, 0]
        }
      })),
      barWidth: '40%'
    }]
  })
}

function initIndustryChart() {
  if (!industryChartRef.value) return
  const industryChart = echarts.init(industryChartRef.value)
  console.log('行业图表数据:', industryData.value)
  const data = industryData.value.length > 0 ? industryData.value : []
  
  if (data.length === 0) {
    industryChart.setOption({
      title: {
        text: '暂无行业分布数据',
        left: 'center',
        top: 'center',
        textStyle: { color: '#9ca3af', fontSize: 14 }
      }
    })
    return
  }
  
  industryChart.setOption({
    tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
    series: [{
      type: 'pie',
      radius: ['45%', '70%'],
      center: ['50%', '50%'],
      avoidLabelOverlap: true,
      itemStyle: { borderRadius: 8, borderColor: '#fff', borderWidth: 2 },
      label: { show: true, formatter: '{b}\n{d}%' },
      data: data.map((item, index) => ({
        value: item.value,
        name: item.name,
        itemStyle: { color: industryColors[index % industryColors.length] }
      }))
    }]
  })
}

function initSalaryChart() {
  if (!salaryChartRef.value) {
    console.log('薪资图表容器不存在')
    return
  }
  
  console.log('初始化薪资图表, salaryData:', salaryData.value)
  const salaryChart = echarts.init(salaryChartRef.value)
  const data = salaryData.value && salaryData.value.length > 0 ? salaryData.value : []
  console.log('薪资图表数据:', data)
  
  if (data.length === 0) {
    salaryChart.setOption({
      title: {
        text: '暂无薪资分布数据',
        left: 'center',
        top: 'center',
        textStyle: { color: '#9ca3af', fontSize: 14 }
      }
    })
    console.log('显示暂无薪资分布数据')
    return
  }
  console.log('渲染薪资图表')
  console.log('薪资区间数量:', data.length)
  salaryChart.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '10%', containLabel: true },
    xAxis: {
      type: 'category',
      data: data.map(item => item.range),
      axisLabel: { rotate: 0 }
    },
    yAxis: { type: 'value', axisLabel: { formatter: '{value}人' } },
    series: [{
      type: 'bar',
      data: data.map((item, index) => ({
        value: item.count,
        itemStyle: {
          color: industryColors[index % industryColors.length],
          borderRadius: [4, 4, 0, 0]
        }
      })),
      barWidth: '50%',
      label: { show: true, position: 'top', formatter: '{c}' }
    }]
  })
}

function initRegionChart() {
  if (!regionChartRef.value) return
  regionChart = echarts.init(regionChartRef.value)

  const cityCoords = {
    '北京': [116.46, 39.92], '天津': [117.2, 39.13], '上海': [121.48, 31.22],
    '重庆': [106.54, 29.59], '石家庄': [114.48, 38.03], '太原': [112.53, 37.87],
    '呼和浩特': [111.65, 40.82], '沈阳': [123.38, 41.8], '长春': [125.35, 43.88],
    '哈尔滨': [126.63, 45.75], '南京': [118.78, 32.04], '杭州': [120.19, 30.26],
    '合肥': [117.27, 31.86], '福州': [119.3, 26.08], '南昌': [115.89, 28.68],
    '济南': [116.99, 36.67], '郑州': [113.65, 34.76], '武汉': [114.31, 30.52],
    '长沙': [113, 28.21], '广州': [113.23, 23.16], '南宁': [108.33, 22.84],
    '海口': [110.35, 20.02], '成都': [104.06, 30.67], '贵阳': [106.71, 26.57],
    '昆明': [102.73, 25.04], '拉萨': [91.11, 29.97], '西安': [108.95, 34.27],
    '兰州': [103.73, 36.03], '西宁': [101.74, 36.56], '银川': [106.27, 38.47],
    '乌鲁木齐': [87.68, 43.77], '深圳': [114.07, 22.62], '青岛': [120.38, 36.07],
    '大连': [121.62, 38.92], '苏州': [120.62, 31.3], '厦门': [118.1, 24.46],
    '宁波': [121.56, 29.86], '无锡': [120.29, 31.59], '佛山': [113.11, 23.05],
    '东莞': [113.75, 23.04], '珠海': [113.55, 22.24]
  }

  const provinceCityMap = {
    '北京': ['北京'], '天津': ['天津'], '上海': ['上海'], '重庆': ['重庆'],
    '河北': ['石家庄', '唐山', '秦皇岛', '邯郸', '邢台', '保定', '张家口', '承德', '沧州', '廊坊', '衡水'],
    '山西': ['太原', '大同', '阳泉', '长治', '晋城', '朔州', '晋中', '运城', '忻州', '临汾', '吕梁'],
    '内蒙古': ['呼和浩特', '包头', '乌海', '赤峰', '通辽', '鄂尔多斯', '呼伦贝尔', '巴彦淖尔', '乌兰察布'],
    '辽宁': ['沈阳', '大连', '鞍山', '抚顺', '本溪', '丹东', '锦州', '营口', '阜新', '辽阳', '盘锦', '铁岭', '朝阳', '葫芦岛'],
    '吉林': ['长春', '吉林', '四平', '辽源', '通化', '白山', '松原', '白城', '延边'],
    '黑龙江': ['哈尔滨', '齐齐哈尔', '鸡西', '鹤岗', '双鸭山', '大庆', '伊春', '佳木斯', '七台河', '牡丹江', '黑河', '绥化'],
    '江苏': ['南京', '无锡', '徐州', '常州', '苏州', '南通', '连云港', '淮安', '盐城', '扬州', '镇江', '泰州', '宿迁'],
    '浙江': ['杭州', '宁波', '温州', '嘉兴', '湖州', '绍兴', '金华', '衢州', '舟山', '台州', '丽水'],
    '安徽': ['合肥', '芜湖', '蚌埠', '淮南', '马鞍山', '淮北', '铜陵', '安庆', '黄山', '滁州', '阜阳', '宿州', '六安', '亳州', '池州', '宣城'],
    '福建': ['福州', '厦门', '莆田', '三明', '泉州', '漳州', '南平', '龙岩', '宁德'],
    '江西': ['南昌', '景德镇', '萍乡', '九江', '新余', '鹰潭', '赣州', '吉安', '宜春', '抚州', '上饶'],
    '山东': ['济南', '青岛', '淄博', '枣庄', '东营', '烟台', '潍坊', '济宁', '泰安', '威海', '日照', '临沂', '德州', '聊城', '滨州', '菏泽'],
    '河南': ['郑州', '开封', '洛阳', '平顶山', '安阳', '鹤壁', '新乡', '焦作', '濮阳', '许昌', '漯河', '三门峡', '南阳', '商丘', '信阳', '周口', '驻马店'],
    '湖北': ['武汉', '黄石', '十堰', '宜昌', '襄阳', '鄂州', '荆门', '孝感', '荆州', '黄冈', '咸宁', '随州', '恩施'],
    '湖南': ['长沙', '株洲', '湘潭', '衡阳', '邵阳', '岳阳', '常德', '张家界', '益阳', '郴州', '永州', '怀化', '娄底', '湘西'],
    '广东': ['广州', '深圳', '珠海', '汕头', '佛山', '韶关', '湛江', '肇庆', '江门', '茂名', '惠州', '梅州', '汕尾', '河源', '阳江', '清远', '东莞', '中山', '潮州', '揭阳', '云浮'],
    '广西': ['南宁', '柳州', '桂林', '梧州', '北海', '防城港', '钦州', '贵港', '玉林', '百色', '贺州', '河池', '来宾', '崇左'],
    '海南': ['海口', '三亚', '三沙', '儋州'],
    '四川': ['成都', '自贡', '攀枝花', '泸州', '德阳', '绵阳', '广元', '遂宁', '内江', '乐山', '南充', '眉山', '宜宾', '广安', '达州', '雅安', '巴中', '资阳', '阿坝', '甘孜', '凉山'],
    '贵州': ['贵阳', '六盘水', '遵义', '安顺', '毕节', '铜仁', '黔西南', '黔东南', '黔南'],
    '云南': ['昆明', '曲靖', '玉溪', '保山', '昭通', '丽江', '普洱', '临沧', '楚雄', '红河', '文山', '西双版纳', '大理', '德宏', '怒江', '迪庆'],
    '西藏': ['拉萨', '日喀则', '昌都', '林芝', '山南', '那曲', '阿里'],
    '陕西': ['西安', '铜川', '宝鸡', '咸阳', '渭南', '延安', '汉中', '榆林', '安康', '商洛'],
    '甘肃': ['兰州', '嘉峪关', '金昌', '白银', '天水', '武威', '张掖', '平凉', '酒泉', '庆阳', '定西', '陇南', '临夏', '甘南'],
    '青海': ['西宁', '海东', '海北', '黄南', '海南', '果洛', '玉树', '海西'],
    '宁夏': ['银川', '石嘴山', '吴忠', '固原', '中卫'],
    '新疆': ['乌鲁木齐', '克拉玛依', '吐鲁番', '哈密', '昌吉', '博州', '巴州', '阿克苏', '克州', '喀什', '和田', '伊犁', '塔城', '阿勒泰']
  }

  const cityDataMap = {}
  regionData.value.forEach(item => {
    cityDataMap[item.city] = item
  })

  function buildProvinceData() {
    const provinceData = []
    Object.entries(cityData.value).forEach(([province, data]) => {
      provinceData.push({
        name: province,
        value: data.percent,
        count: data.count
      })
    })
    return provinceData
  }

  function buildCityData(province) {
    const cities = provinceCityMap[province] || []
    const cityList = []
    cities.forEach(city => {
      if (cityDataMap[city]) {
        const coord = cityCoords[city] || [0, 0]
        cityList.push({
          name: city,
          value: [...coord, cityDataMap[city].percent],
          count: cityDataMap[city].count,
          percent: cityDataMap[city].percent
        })
      }
    })
    return cityList
  }

  function renderChinaMap() {
    const data = buildProvinceData()
    if (data.length === 0) {
      regionChart.setOption({
        title: { text: '暂无区域分布数据', left: 'center', top: 'center', textStyle: { color: '#9ca3af', fontSize: 14 } }
      })
      return
    }

    const maxValue = Math.max(...data.map(item => item.value || 0))

    regionChart.setOption({
      title: {
        text: '点击省份查看城市分布',
        left: 'center',
        top: 10,
        textStyle: { fontSize: 14, color: '#666' }
      },
      tooltip: {
        trigger: 'item',
        formatter: (params) => {
          if (!params.name) return ''
          const item = data.find(d => d.name === params.name)
          return `<div style="font-weight:bold;margin-bottom:5px">${params.name}</div>
                  <div>就业人数: <span style="color:#b2182b;font-weight:bold">${item ? item.count : 0}</span> 人</div>
                  <div>占比: <span style="color:#ef8a62;font-weight:bold">${params.value.toFixed(1)}%</span></div>
                  <div style="margin-top:5px;font-size:11px;color:#666">点击查看详情</div>`
        },
        backgroundColor: 'rgba(255,255,255,0.98)',
        borderColor: '#ddd',
        borderWidth: 1,
        padding: [12, 16],
        textStyle: { color: '#333' }
      },
      visualMap: {
        show: true,
        min: 0,
        max: maxValue,
        left: 20,
        bottom: 20,
        text: ['高', '低'],
        textStyle: { color: '#333', fontSize: 12 },
        inRange: {
          color: ['#2166ac', '#67a9cf', '#d1e5f0', '#f7f7f7', '#fddbc7', '#ef8a62', '#b2182b']
        },
        calculable: true
      },
      series: [{
        name: '就业流向',
        type: 'map',
        map: 'china',
        roam: true,
        scaleLimit: { min: 1, max: 8 },
        zoom: 1.2,
        center: [105, 36],
        label: {
          show: false,
          formatter: '{b}',
          fontSize: 10
        },
        emphasis: {
          label: { show: true, color: '#fff', fontSize: 12 },
          itemStyle: { areaColor: '#ffd700' }
        },
        itemStyle: {
          areaColor: '#e8f5e9',
          borderColor: '#bdbdbd',
          borderWidth: 0.5
        },
        select: {
          itemStyle: { areaColor: '#a5d6a7' },
          label: { show: true }
        },
        data: data,
        zlevel: 1
      }]
    })
  }

  function renderCityMap(province) {
    const data = buildCityData(province)
    if (data.length === 0) {
      ElMessage({ message: `${province} 暂无城市级数据`, type: 'warning' })
      return
    }
    const maxValue = Math.max(...data.map(item => item.percent || 0), 1)

    regionChart.setOption({
      title: {
        text: `${province} - 点击返回全国`,
        left: 'center',
        top: 10,
        textStyle: { fontSize: 14, color: '#666' }
      },
      tooltip: {
        trigger: 'item',
        formatter: (params) => {
          if (!params.name) return ''
          const item = data.find(d => d.name === params.name)
          return `<div style="font-weight:bold;margin-bottom:5px">${params.name}</div>
                  <div>就业人数: <span style="color:#b2182b;font-weight:bold">${item ? item.count : 0}</span> 人</div>
                  <div>占比: <span style="color:#ef8a62;font-weight:bold">${params.value[2].toFixed(1)}%</span></div>`
        },
        backgroundColor: 'rgba(255,255,255,0.98)',
        borderColor: '#ddd',
        borderWidth: 1,
        padding: [12, 16],
        textStyle: { color: '#333' }
      },
      visualMap: {
        show: true,
        min: 0,
        max: maxValue,
        left: 20,
        bottom: 20,
        text: ['高', '低'],
        textStyle: { color: '#333', fontSize: 12 },
        inRange: {
          color: ['#2166ac', '#67a9cf', '#d1e5f0', '#f7f7f7', '#fddbc7', '#ef8a62', '#b2182b']
        },
        calculable: true
      },
      series: [{
        name: '城市就业分布',
        type: 'effectScatter',
        coordinateSystem: 'geo',
        data: data,
        symbolSize: (val) => Math.max(15, (val[2] / maxValue) * 40 + 10),
        showEffectOn: 'render',
        rippleEffect: { brushType: 'stroke', scale: 2 },
        itemStyle: {
          color: (params) => {
            const ratio = params.value[2] / maxValue
            const colorList = ['#2166ac', '#67a9cf', '#d1e5f0', '#f7f7f7', '#fddbc7', '#ef8a62', '#b2182b']
            const idx = Math.min(Math.floor(ratio * colorList.length), colorList.length - 1)
            return colorList[colorList.length - 1 - idx]
          },
          borderColor: '#fff',
          borderWidth: 2,
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.3)'
        },
        label: {
          show: true,
          formatter: (params) => params.data.name,
          position: 'right',
          fontSize: 11,
          color: '#333'
        },
        emphasis: {
          scale: 1.5,
          label: { show: true, fontSize: 14, fontWeight: 'bold' }
        }
      }]
    })
  }

  regionChart.off('click')
  regionChart.on('click', (params) => {
    if (!params.name) return

    if (currentProvince.value) {
      currentProvince.value = null
      renderChinaMap()
    } else {
      const province = params.name
      if (provinceCityMap[province] && cityData.value[province]) {
        currentProvince.value = province
        renderCityMap(province)
        ElMessage({
          message: `正在显示 <strong>${province}</strong> 各城市就业分布`,
          type: 'info',
          duration: 2000,
          dangerouslyUseHTMLString: true
        })
      } else {
        const rank = buildProvinceData().sort((a, b) => b.value - a.value).findIndex(d => d.name === province) + 1
        ElMessage({
          message: `<strong>${province}</strong><br/>
                    就业人数: <strong>${params.data.count || 0}</strong> 人<br/>
                    占比: <strong>${params.value.toFixed(1)}%</strong><br/>
                    排名: <strong>第${rank}名</strong>`,
          type: 'info',
          duration: 3000,
          dangerouslyUseHTMLString: true
        })
      }
    }
  })

  loadChinaMap().then(mapData => {
    if (mapData) {
      renderChinaMap()
    } else {
      regionChart.setOption({
        title: { text: '地图加载失败，请刷新重试', left: 'center', top: 'center', textStyle: { color: '#9ca3af', fontSize: 14 } }
      })
    }
  })
}
</script>
