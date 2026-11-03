<template>
  <div class="flex min-h-screen bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800">
    <div class="hidden lg:flex lg:w-1/2 flex-col justify-between p-12">
      <div class="flex items-center space-x-3">
        <div class="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center">
          <i class="fas fa-graduation-cap text-white text-xl"></i>
        </div>
        <div>
          <h1 class="text-xl font-bold text-white">高校就业服务平台</h1>
          <p class="text-blue-200 text-sm">Campus Employment Platform</p>
        </div>
      </div>

      <div class="space-y-8">
        <h2 class="text-4xl font-bold text-white leading-tight">
          开启您的职业之旅<br>连接无限可能
        </h2>
        <div class="space-y-4">
          <div class="flex items-center space-x-4">
            <div class="w-12 h-12 bg-white/10 rounded-xl flex items-center justify-center">
              <i class="fas fa-user-graduate text-blue-300"></i>
            </div>
            <div>
              <p class="text-white font-medium">学生注册</p>
              <p class="text-blue-200 text-sm">完善简历，获取精准岗位推荐</p>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <div class="w-12 h-12 bg-white/10 rounded-xl flex items-center justify-center">
              <i class="fas fa-building text-blue-300"></i>
            </div>
            <div>
              <p class="text-white font-medium">企业入驻</p>
              <p class="text-blue-200 text-sm">发布岗位，高效招募校园人才</p>
            </div>
          </div>
        </div>
      </div>

      <div class="flex items-center space-x-6">
        <div class="text-center">
          <p class="text-3xl font-bold text-white">{{ stats.total_students.toLocaleString() }}</p>
          <p class="text-blue-200 text-sm">注册学生</p>
        </div>
        <div class="w-px h-12 bg-white/20"></div>
        <div class="text-center">
          <p class="text-3xl font-bold text-white">{{ stats.total_companies.toLocaleString() }}</p>
          <p class="text-blue-200 text-sm">入驻企业</p>
        </div>
        <div class="w-px h-12 bg-white/20"></div>
        <div class="text-center">
          <p class="text-3xl font-bold text-white">{{ stats.total_jobs.toLocaleString() }}</p>
          <p class="text-blue-200 text-sm">岗位总数</p>
        </div>
      </div>
    </div>

    <div class="w-full lg:w-1/2 flex items-center justify-center p-8">
      <div class="w-full max-w-md">
        <div class="lg:hidden flex items-center justify-center space-x-3 mb-8">
          <div class="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center">
            <i class="fas fa-graduation-cap text-white text-xl"></i>
          </div>
          <h1 class="text-xl font-bold text-white">高校就业服务平台</h1>
        </div>

        <div class="bg-white rounded-2xl shadow-2xl p-8">
          <div class="text-center mb-6">
            <h2 class="text-2xl font-bold text-gray-900">创建账号</h2>
            <p class="text-gray-500 mt-2">加入高校就业服务平台</p>
          </div>

          <div class="grid grid-cols-2 gap-4 mb-6">
            <button
              @click="form.role = 'student'"
              class="flex flex-col items-center p-4 border-2 rounded-xl transition-all"
              :class="form.role === 'student' ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-500'"
            >
              <div class="w-12 h-12 rounded-full flex items-center justify-center mb-2" :class="form.role === 'student' ? 'bg-blue-100' : 'bg-gray-100'">
                <i class="fas fa-user-graduate text-2xl" :class="form.role === 'student' ? 'text-blue-600' : 'text-gray-500'"></i>
              </div>
              <span :class="form.role === 'student' ? 'text-blue-700 font-medium' : 'text-gray-600'">我是学生</span>
            </button>
            <button
              @click="form.role = 'company'"
              class="flex flex-col items-center p-4 border-2 rounded-xl transition-all"
              :class="form.role === 'company' ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-500'"
            >
              <div class="w-12 h-12 rounded-full flex items-center justify-center mb-2" :class="form.role === 'company' ? 'bg-blue-100' : 'bg-gray-100'">
                <i class="fas fa-building text-2xl" :class="form.role === 'company' ? 'text-blue-600' : 'text-gray-500'"></i>
              </div>
              <span :class="form.role === 'company' ? 'text-blue-700 font-medium' : 'text-gray-600'">我是企业</span>
            </button>
          </div>

          <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
            <el-form-item label="用户名" prop="username">
              <el-input v-model="form.username" placeholder="请输入用户名（学号/手机号）" />
            </el-form-item>
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="form.email" placeholder="请输入邮箱" />
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input v-model="form.password" type="password" placeholder="请设置登录密码（至少6位）" show-password />
            </el-form-item>
            <el-form-item label="确认密码" prop="confirmPassword">
              <el-input v-model="form.confirmPassword" type="password" placeholder="请再次输入密码" show-password />
            </el-form-item>

            <el-form-item>
              <el-checkbox v-model="form.agree">
                我已阅读并同意 <a href="#" class="text-blue-600">《用户服务协议》</a> 和 <a href="#" class="text-blue-600">《隐私政策》</a>
              </el-checkbox>
            </el-form-item>

            <el-button type="primary" size="large" class="w-full" :loading="loading" @click="handleRegister">
              立即注册
            </el-button>
          </el-form>

          <div class="mt-6 text-center">
            <p class="text-gray-500 text-sm">
              已有账号？
              <router-link to="/login" class="text-blue-600 hover:text-blue-700 font-medium">立即登录</router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { authAPI } from '@/api'

const router = useRouter()

const formRef = ref(null)
const loading = ref(false)

const stats = reactive({
  total_students: 0,
  total_companies: 0,
  total_jobs: 0
})

const fetchStats = async () => {
  try {
    const res = await authAPI.getPublicStats()
    if (res.data) {
      stats.total_students = res.data.total_students || 0
      stats.total_companies = res.data.total_companies || 0
      stats.total_jobs = res.data.total_jobs || 0
    }
  } catch (error) {
    console.error('Failed to fetch stats:', error)
  }
}

onMounted(() => {
  fetchStats()
})

const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  role: 'student',
  agree: false
})

const validatePass2 = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== form.password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' }
  ],
  confirmPassword: [{ validator: validatePass2, trigger: 'blur' }]
}

const handleRegister = async () => {
  if (!form.agree) {
    ElMessage.warning('请阅读并同意用户协议')
    return
  }

  if (formRef.value) {
    await formRef.value.validate(async (valid) => {
      if (valid) {
        loading.value = true
        try {
          const result = await authAPI.register({
            username: form.username,
            email: form.email,
            password: form.password,
            role: form.role
          })
          if (result.data?.id) {
            ElMessage.success('注册成功，请登录')
            router.push('/login')
          } else {
            ElMessage.error(result.data?.detail || '注册失败')
          }
        } catch (error) {
          ElMessage.error(error.response?.data?.detail || '注册失败')
        } finally {
          loading.value = false
        }
      }
    })
  }
}
</script>
