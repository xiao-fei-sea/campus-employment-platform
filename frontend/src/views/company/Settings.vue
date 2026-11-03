<template>
  <div class="max-w-5xl">
    <div class="bg-white rounded-2xl shadow-sm p-8 mb-6">
      <div class="flex items-start space-x-8">
        <div class="relative">
          <img :src="company.logo || `https://ui-avatars.com/api/?name=${encodeURIComponent(company.name || '企业')}&background=6366f1&color=fff&size=112`" :alt="company.name" class="w-28 h-28 rounded-2xl object-cover ring-4 ring-purple-100">
          <input type="file" ref="logoInput" accept="image/*" class="hidden" @change="handleLogoUpload">
          <button @click="triggerLogoUpload" class="absolute bottom-0 right-0 w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center hover:bg-purple-700 transition-colors">
            <i class="fas fa-camera text-sm"></i>
          </button>
        </div>
        <div class="flex-1">
          <div class="flex items-center space-x-3 mb-2">
            <h3 class="text-2xl font-bold text-gray-900">{{ company.name || '企业用户' }}</h3>
            <span v-if="company.status === 'approved'" class="px-3 py-1 bg-green-100 text-green-700 text-sm rounded-full">
              <i class="fas fa-check-circle mr-1"></i>已认证
            </span>
            <span v-else class="px-3 py-1 bg-yellow-100 text-yellow-700 text-sm rounded-full">
              <i class="fas fa-clock mr-1"></i>待审核
            </span>
          </div>
          <p class="text-gray-500 mb-4">{{ company.description || '暂无简介' }}</p>
          <div class="grid grid-cols-4 gap-4">
            <div class="text-center">
              <p class="text-2xl font-bold text-gray-900">{{ formatScale(company.scale) }}</p>
              <p class="text-sm text-gray-500">企业规模</p>
            </div>
            <div class="text-center">
              <p class="text-2xl font-bold text-gray-900">{{ formatIndustry(company.industry) }}</p>
              <p class="text-sm text-gray-500">行业领域</p>
            </div>
            <div class="text-center">
              <p class="text-2xl font-bold text-gray-900">{{ company.city || '-' }}</p>
              <p class="text-sm text-gray-500">所在城市</p>
            </div>
            <div class="text-center">
              <p class="text-2xl font-bold text-gray-900">{{ company.created_at ? new Date(company.created_at).getFullYear() : '-' }}</p>
              <p class="text-sm text-gray-500">入驻年份</p>
            </div>
          </div>
        </div>
        <button @click="editCompany" class="px-6 py-2 border border-gray-200 text-gray-700 rounded-xl hover:bg-gray-50 transition-colors">
          <i class="fas fa-edit mr-2"></i>编辑
        </button>
      </div>
    </div>

    <div class="bg-white rounded-2xl shadow-sm">
      <div class="flex border-b border-gray-100">
        <button v-for="tab in tabs" :key="tab.value" :class="activeTab === tab.value ? 'text-purple-600 border-b-2 border-purple-600' : 'text-gray-500 hover:text-gray-700'" class="px-8 py-4 font-medium transition-colors" @click="activeTab = tab.value">
          <i :class="tab.icon" class="mr-2"></i>{{ tab.label }}
        </button>
      </div>

      <div class="p-8">
        <form v-if="activeTab === 'company'" class="space-y-6">
          <div class="grid grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">企业名称</label>
              <el-input :model-value="company.name" disabled />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">企业简称</label>
              <el-input v-model="form.short_name" />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">所在城市</label>
              <el-select v-model="form.city" class="w-full">
                <el-option label="北京市" value="北京市" />
                <el-option label="上海市" value="上海市" />
                <el-option label="深圳市" value="深圳市" />
                <el-option label="杭州市" value="杭州市" />
                <el-option label="广州市" value="广州市" />
                <el-option label="南京市" value="南京市" />
                <el-option label="成都市" value="成都市" />
                <el-option label="武汉市" value="武汉市" />
              </el-select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">详细地址</label>
              <el-input v-model="form.address" />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">所属行业</label>
              <el-select v-model="form.industry" class="w-full">
                <el-option label="互联网/IT" value="it" />
                <el-option label="金融" value="finance" />
                <el-option label="制造业" value="manufacturing" />
                <el-option label="教育培训" value="education" />
                <el-option label="医疗健康" value="healthcare" />
                <el-option label="房地产" value="real_estate" />
                <el-option label="其他" value="other" />
              </el-select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">企业规模</label>
              <el-select v-model="form.scale" class="w-full">
                <el-option label="0-20人" value="small" />
                <el-option label="20-100人" value="medium" />
                <el-option label="100-500人" value="large" />
                <el-option label="500人以上" value="super_large" />
              </el-select>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">企业简介</label>
            <el-input v-model="form.description" type="textarea" :rows="4" />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">企业官网</label>
            <el-input v-model="form.website" placeholder="https://" />
          </div>

          <div class="pt-4 border-t border-gray-100">
            <h4 class="font-medium text-gray-900 mb-4">HR联系人信息</h4>
            <div class="grid grid-cols-3 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">联系人姓名</label>
                <el-input v-model="form.contact_name" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">联系电话</label>
                <el-input v-model="form.contact_phone" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">电子邮箱</label>
                <el-input v-model="form.contact_email" />
              </div>
            </div>
          </div>

          <div class="flex items-center justify-end pt-4">
            <el-button type="primary" @click="saveCompany" :loading="saving">保存修改</el-button>
          </div>
        </form>

        <div v-else-if="activeTab === 'account'" class="text-center p-8">
          <p class="text-gray-500">账号管理功能开发中...</p>
        </div>

        <div v-else-if="activeTab === 'certification'" class="text-center p-8">
          <div v-if="company.status === 'approved'" class="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <i class="fas fa-certificate text-4xl text-green-600"></i>
          </div>
          <div v-else class="w-20 h-20 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <i class="fas fa-clock text-4xl text-yellow-600"></i>
          </div>
          <h3 class="text-xl font-bold text-gray-900 mb-2">{{ company.status === 'approved' ? '已认证' : '待认证' }}</h3>
          <p class="text-gray-500">{{ company.status === 'approved' ? '营业执照已认证' : '请等待管理员审核' }}</p>
          <p v-if="company.verified_at" class="text-sm text-gray-400 mt-2">认证时间：{{ company.verified_at }}</p>
        </div>

        <div v-else-if="activeTab === 'notification'" class="text-center p-8">
          <p class="text-gray-500">通知设置功能开发中...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { companyAPI } from '@/api'

const activeTab = ref('company')
const saving = ref(false)
const logoInput = ref(null)

const tabs = [
  { label: '企业信息', value: 'company', icon: 'fas fa-building' },
  { label: '账号管理', value: 'account', icon: 'fas fa-user-friends' },
  { label: '资质认证', value: 'certification', icon: 'fas fa-shield-alt' },
  { label: '通知设置', value: 'notification', icon: 'fas fa-bell' }
]

const company = ref({
  name: '',
  logo: '',
  description: '',
  scale: '',
  industry: '',
  city: '',
  status: '',
  created_at: '',
  verified_at: ''
})

const form = reactive({
  short_name: '',
  city: '',
  address: '',
  industry: '',
  scale: '',
  description: '',
  website: '',
  contact_name: '',
  contact_phone: '',
  contact_email: ''
})

const industryMap = {
  it: '互联网/IT',
  finance: '金融',
  manufacturing: '制造业',
  education: '教育培训',
  healthcare: '医疗健康',
  real_estate: '房地产',
  other: '其他'
}

const scaleMap = {
  small: '0-20人',
  medium: '20-100人',
  large: '100-500人',
  super_large: '500人以上'
}

const formatIndustry = (value) => {
  return industryMap[value] || value || '-'
}

const formatScale = (value) => {
  return scaleMap[value] || value || '-'
}

const fetchCompanyProfile = async () => {
  try {
    const res = await companyAPI.getSettings()
    const data = res.data
    company.value = data
    Object.assign(form, {
      short_name: data.short_name || '',
      city: data.city || '',
      address: data.address || '',
      industry: data.industry || '',
      scale: data.scale || '',
      description: data.description || '',
      website: data.website || '',
      contact_name: data.contact_name || '',
      contact_phone: data.contact_phone || '',
      contact_email: data.contact_email || ''
    })
  } catch (error) {
    console.error('获取企业信息失败:', error)
    ElMessage.error('获取企业信息失败')
  }
}

const triggerLogoUpload = () => {
  logoInput.value?.click()
}

const handleLogoUpload = async (event) => {
  const file = event.target.files?.[0]
  if (!file) return

  const formData = new FormData()
  formData.append('file', file)
  formData.append('type', 'logo')

  try {
    const res = await companyAPI.uploadLogo(formData)
    if (res.data?.url) {
      company.value.logo = res.data.url
      localStorage.setItem('company_logo', res.data.url)
      ElMessage.success('Logo上传成功')
    }
  } catch (error) {
    console.error('上传失败:', error)
    ElMessage.error('Logo上传失败')
  }
}

const saveCompany = async () => {
  saving.value = true
  try {
    const res = await companyAPI.updateSettings(form)
    Object.assign(company.value, res.data)
    ElMessage.success('保存成功')
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

const editCompany = () => {
  activeTab.value = 'company'
}

onMounted(() => {
  fetchCompanyProfile()
})
</script>