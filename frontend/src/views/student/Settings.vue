<template>
  <div class="space-y-6">
    <div class="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-6 text-white">
      <h1 class="text-2xl font-bold mb-2">账号设置</h1>
      <p class="text-blue-100">管理您的个人信息和账户设置</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
      <div class="lg:col-span-3 space-y-6">
        <div class="bg-white rounded-2xl shadow-md p-8 border border-gray-100">
          <h3 class="text-lg font-bold text-gray-900 mb-4 flex items-center">
            <i class="fas fa-user-circle mr-3 text-blue-600"></i>
            基本信息
          </h3>
          <div class="flex items-start space-x-6">
            <div class="flex flex-col items-center">
              <div class="relative">
                <img :src="form.avatar || 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&h=100&fit=crop&crop=face'" class="w-20 h-20 rounded-full object-cover border-4 border-gray-100 cursor-pointer hover:opacity-80" @click="triggerUpload">
                <button @click="triggerUpload" class="absolute bottom-0 right-0 w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white hover:bg-blue-700 transition-colors">
                  <i class="fas fa-camera text-sm"></i>
                </button>
                <input ref="avatarInput" type="file" accept="image/*" class="hidden" @change="handleAvatarUpload">
              </div>
              <p class="text-xs text-gray-500 mt-2">点击更换</p>
            </div>
            <div class="flex-1 grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">姓名</label>
                <el-input v-model="form.name" placeholder="请输入姓名" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">性别</label>
                <el-select v-model="form.gender" class="w-full">
                  <el-option label="男" value="male" />
                  <el-option label="女" value="female" />
                </el-select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">手机号</label>
                <el-input v-model="form.phone" placeholder="请输入手机号" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">邮箱</label>
                <el-input v-model="form.email" disabled />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">学号</label>
                <el-input v-model="form.student_no" disabled />
              </div>
            </div>
          </div>
          <div class="mt-4 flex justify-end">
            <el-button type="primary" @click="saveBasic">保存修改</el-button>
          </div>
        </div>

        <div class="bg-white rounded-2xl shadow-md p-8 border border-gray-100">
          <h3 class="text-lg font-bold text-gray-900 mb-4 flex items-center">
            <i class="fas fa-briefcase mr-3 text-emerald-600"></i>
            求职偏好
          </h3>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-3">期望职位类型</label>
              <el-checkbox-group v-model="preferences.jobTypes" class="flex flex-wrap gap-2">
                <el-checkbox label="全职" border value="fulltime" />
                <el-checkbox label="实习" border value="internship" />
                <el-checkbox label="兼职" border value="parttime" />
              </el-checkbox-group>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-3">期望薪资范围</label>
              <el-slider v-model="preferences.salaryRange" range :min="5" :max="50" />
              <p class="text-center text-blue-600 font-medium mt-2">{{ preferences.salaryRange[0] }}K - {{ preferences.salaryRange[1] }}K</p>
            </div>
          </div>
          <div class="mt-4">
            <label class="block text-sm font-medium text-gray-700 mb-3">期望工作地点</label>
            <el-checkbox-group v-model="preferences.locations" class="flex flex-wrap gap-2">
              <el-checkbox label="北京" border value="北京" />
              <el-checkbox label="上海" border value="上海" />
              <el-checkbox label="深圳" border value="深圳" />
              <el-checkbox label="杭州" border value="杭州" />
              <el-checkbox label="广州" border value="广州" />
              <el-checkbox label="南京" border value="南京" />
              <el-checkbox label="成都" border value="成都" />
              <el-checkbox label="武汉" border value="武汉" />
            </el-checkbox-group>
          </div>
          <div class="mt-4 flex justify-end">
            <el-button type="primary" @click="savePreferences">保存偏好</el-button>
          </div>
        </div>
      </div>

      <div class="space-y-6">
        <div class="bg-white rounded-2xl shadow-md p-6 border border-gray-100">
          <h3 class="text-lg font-bold text-gray-900 mb-4">账号信息</h3>
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-gray-500">注册时间</span>
              <span class="font-medium">{{ formatDate(profileData.created_at) }}</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-gray-500">所在院校</span>
              <span class="font-medium">{{ profileData.major || '-' }}</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-gray-500">毕业年份</span>
              <span class="font-medium">{{ profileData.graduation_year || '-' }}</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-gray-500">简历完善度</span>
              <span class="font-medium text-emerald-600">{{ resumeCompletion }}%</span>
            </div>
            <div class="w-full bg-gray-100 rounded-full h-2">
              <div class="bg-emerald-500 h-2 rounded-full" :style="{ width: resumeCompletion + '%' }"></div>
            </div>
          </div>
        </div>

        <div class="bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl shadow-md p-6 text-white">
          <h3 class="text-lg font-bold mb-4">求职提示</h3>
          <ul class="space-y-3 text-sm opacity-90">
            <li class="flex items-start">
              <i class="fas fa-check-circle mr-2 mt-1"></i>
              <span>完善简历可提高曝光率</span>
            </li>
            <li class="flex items-start">
              <i class="fas fa-check-circle mr-2 mt-1"></i>
              <span>及时投递岗位增加机会</span>
            </li>
            <li class="flex items-start">
              <i class="fas fa-check-circle mr-2 mt-1"></i>
              <span>关注宣讲会获取更多信息</span>
            </li>
          </ul>
        </div>

        <div class="bg-white rounded-2xl shadow-md p-6 border border-gray-100">
          <h3 class="text-lg font-bold text-gray-900 mb-4 flex items-center">
            <i class="fas fa-lock mr-3 text-amber-600"></i>
            修改密码
          </h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">当前密码</label>
              <el-input v-model="passwordForm.oldPassword" type="password" show-password placeholder="请输入当前密码" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">新密码</label>
              <el-input v-model="passwordForm.newPassword" type="password" show-password placeholder="请输入新密码" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">确认密码</label>
              <el-input v-model="passwordForm.confirmPassword" type="password" show-password placeholder="请再次输入新密码" />
            </div>
          </div>
          <div class="mt-4">
            <el-button type="primary" class="w-full" @click="changePassword">修改密码</el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { studentAPI, authAPI } from '@/api'
import { useUserStore } from '@/stores/user'
import api from '@/api'

const userStore = useUserStore()
const avatarInput = ref(null)

const triggerUpload = () => {
  avatarInput.value?.click()
}

const handleAvatarUpload = async (event) => {
  const file = event.target.files?.[0]
  if (!file) return

  const formData = new FormData()
  formData.append('file', file)

  try {
    const res = await studentAPI.uploadAvatar(formData)
    if (res.data?.url) {
      form.avatar = res.data.url
      profileData.avatar = res.data.url
      userStore.userInfo.student_profile.avatar = res.data.url
      userStore.userInfo.student_profile.name = res.data.name
      localStorage.setItem('userInfo', JSON.stringify(userStore.userInfo))
      ElMessage.success('头像上传成功')
    }
  } catch (error) {
    console.error('上传失败:', error)
    ElMessage.error('头像上传失败')
  }
}

const profileData = reactive({
  avatar: '',
  name: '',
  student_no: '',
  gender: '',
  phone: '',
  email: '',
  major: '',
  graduation_year: '',
  created_at: ''
})

const form = reactive({
  avatar: '',
  name: '',
  student_no: '',
  gender: '',
  phone: '',
  email: ''
})

const preferences = reactive({
  jobTypes: [],
  locations: [],
  salaryRange: [10, 30]
})

const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const resumeCompletion = computed(() => {
  let score = 0
  if (profileData.name) score += 20
  if (profileData.gender) score += 10
  if (profileData.phone) score += 20
  if (profileData.major) score += 20
  if (profileData.graduation_year) score += 10
  if (profileData.avatar) score += 20
  return score
})

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

const fetchProfile = async () => {
  try {
    const res = await studentAPI.getSettings()
    const data = res.data
    Object.assign(profileData, data)
    Object.assign(form, {
      avatar: data.avatar || '',
      name: data.name || '',
      student_no: data.student_no || '',
      gender: data.gender || 'male',
      phone: data.phone || '',
      email: data.email || ''
    })
    const userRes = await api.get('/auth/me')
    Object.keys(userRes.data).forEach(key => {
      userStore.userInfo[key] = userRes.data[key]
    })
    localStorage.setItem('userInfo', JSON.stringify(userStore.userInfo))
    if (userStore.userInfo.student_profile) {
      userStore.userInfo.student_profile.avatar = data.avatar
      userStore.userInfo.student_profile.name = data.name
      localStorage.setItem('userInfo', JSON.stringify(userStore.userInfo))
    }
  } catch (error) {
    console.error('获取个人信息失败:', error)
  }
}

const saveBasic = async () => {
  try {
    await studentAPI.updateSettings({
      name: form.name,
      gender: form.gender,
      phone: form.phone,
      avatar: form.avatar
    })
    Object.assign(profileData, form)
    ElMessage.success('基本信息已保存')
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

const savePreferences = async () => {
  try {
    await authAPI.savePreferences({ preferences })
    ElMessage.success('求职偏好已保存')
  } catch (error) {
    console.error('保存求职偏好失败:', error)
    ElMessage.error('保存失败')
  }
}

const loadPreferences = async () => {
  try {
    const res = await authAPI.getPreferences()
    const saved = res.data?.preferences
    if (saved) {
      Object.assign(preferences, saved)
    }
  } catch (error) {
    console.error('加载求职偏好失败:', error)
  }
}

const changePassword = async () => {
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    ElMessage.error('两次输入的密码不一致')
    return
  }
  if (!passwordForm.oldPassword || !passwordForm.newPassword) {
    ElMessage.error('请填写完整信息')
    return
  }
  try {
    await authAPI.changePassword({
      old_password: passwordForm.oldPassword,
      new_password: passwordForm.newPassword
    })
    ElMessage.success('密码修改成功')
    passwordForm.oldPassword = ''
    passwordForm.newPassword = ''
    passwordForm.confirmPassword = ''
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '密码修改失败')
  }
}

onMounted(() => {
  fetchProfile()
  loadPreferences()
})
</script>

<style scoped>
:deep(.el-checkbox.is-bordered) {
  padding: 6px 12px;
  border-radius: 8px;
}
:deep(.el-input__wrapper) {
  border-radius: 8px;
}
</style>