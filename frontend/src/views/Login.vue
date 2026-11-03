<template>
  <div class="login-container">
    <div class="login-overlay"></div>
    <div class="login-left">
      <div class="login-left-header">
        <div class="login-logo">
          <i class="fas fa-graduation-cap"></i>
        </div>
        <div>
          <h1>高校就业服务平台</h1>
          <p>Campus Employment Platform</p>
        </div>
      </div>

      <div class="login-left-content">
        <h2>
          连接校园人才<br>开启职业之旅
        </h2>
        <div class="login-stats">
          <div class="stat-card">
            <p class="stat-number">{{ stats.total_students.toLocaleString() }}</p>
            <p class="stat-label">注册学生</p>
          </div>
          <div class="stat-card">
            <p class="stat-number">{{ stats.total_companies.toLocaleString() }}</p>
            <p class="stat-label">入驻企业</p>
          </div>
          <div class="stat-card">
            <p class="stat-number">{{ stats.total_jobs.toLocaleString() }}</p>
            <p class="stat-label">岗位总数</p>
          </div>
          <div class="stat-card">
            <p class="stat-number">{{ stats.employed_count.toLocaleString() }}</p>
            <p class="stat-label">成功就业</p>
          </div>
        </div>
      </div>

      <div class="login-left-footer">
        <span>关于我们</span>
        <span>联系方式</span>
        <span>隐私政策</span>
      </div>
    </div>

    <div class="login-right">
      <div class="login-form-container">
        <div class="login-mobile-header">
          <div class="login-logo">
            <i class="fas fa-graduation-cap"></i>
          </div>
          <h1>高校就业服务平台</h1>
        </div>

        <div class="login-form-card">
          <div class="login-form-header">
            <h2>欢迎回来</h2>
            <p>请选择您的登录方式</p>
          </div>

          <div class="login-form-body">
            <el-tabs v-model="activeTab" class="login-tabs">
              <el-tab-pane label="账号登录" name="account">
                <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
                  <el-form-item label="账号" prop="username">
                    <el-input v-model="form.username" placeholder="请输入学号/手机号/邮箱" size="large">
                      <template #prefix>
                        <i class="fas fa-user"></i>
                      </template>
                    </el-input>
                  </el-form-item>
                  <el-form-item label="密码" prop="password">
                    <el-input v-model="form.password" type="password" placeholder="请输入密码" size="large" show-password>
                      <template #prefix>
                        <i class="fas fa-lock"></i>
                      </template>
                    </el-input>
                  </el-form-item>
                  <el-form-item label="用户类型">
                    <el-select v-model="form.role" class="w-full">
                      <el-option label="学生" value="student" />
                      <el-option label="企业" value="company" />
                      <el-option label="管理员" value="admin" />
                    </el-select>
                  </el-form-item>
                  <div class="login-options">
                    <el-checkbox v-model="form.remember">记住我</el-checkbox>
                    <a href="#" class="forgot-password">忘记密码？</a>
                  </div>
                  <el-button type="primary" size="large" class="login-button" :loading="loading" @click="handleLogin">
                    登录
                  </el-button>
                </el-form>
              </el-tab-pane>

              <el-tab-pane label="微信快捷登录" name="quick">
                <div class="quick-login">
                  <div class="wechat-qr-container">
                    <div class="wechat-qr-box">
                      <i class="fab fa-weixin wechat-icon"></i>
                      <div v-if="qrCodeLoading" class="wechat-qr-code">
                        <div class="qr-loading">
                          <i class="fas fa-spinner fa-spin"></i>
                          <p>生成中...</p>
                        </div>
                      </div>
                      <div v-else-if="qrCodeUrl" class="wechat-qr-code">
                        <img :src="qrCodeUrl" alt="登录二维码" class="qr-code-img">
                      </div>
                      <div v-else class="wechat-qr-code">
                        <div class="qr-placeholder">
                          <i class="fas fa-qrcode qr-icon"></i>
                          <p>点击刷新</p>
                        </div>
                      </div>
                      <p class="wechat-tip">请使用微信扫描二维码登录</p>
                      <button class="refresh-qr-btn" @click="generateQRCode">
                        <i class="fas fa-redo"></i> 刷新二维码
                      </button>
                    </div>
                  </div>
                </div>
              </el-tab-pane>
            </el-tabs>
          </div>
          <div class="login-form-footer">
            <p>
              还没有账号？
              <router-link to="/register" class="register-link">立即注册</router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import { authAPI } from '@/api'

const router = useRouter()
const userStore = useUserStore()

const activeTab = ref('account')
const loading = ref(false)
const formRef = ref(null)

const qrCodeUrl = ref('')
const qrCodeLoading = ref(false)
const qrScene = ref('')

const stats = reactive({
  total_students: 0,
  total_companies: 0,
  total_jobs: 0,
  employed_count: 0
})

const form = reactive({
  role: 'student',
  username: '',
  password: '',
  remember: false
})

const fetchStats = async () => {
  try {
    const res = await authAPI.getPublicStats()
    if (res.data) {
      stats.total_students = res.data.total_students || 0
      stats.total_companies = res.data.total_companies || 0
      stats.total_jobs = res.data.total_jobs || 0
      stats.employed_count = res.data.employed_count || 0
    }
  } catch (error) {
    console.error('Failed to fetch stats:', error)
  }
}

onMounted(() => {
  fetchStats()
})

const generateQRCode = async () => {
  qrCodeLoading.value = true
  try {
    const response = await authAPI.getWechatQRCode()
    qrCodeUrl.value = response.data.qrcode_url || response.data.qrcode
    qrScene.value = response.data.scene || ''
  } catch (error) {
    ElMessage.error('获取二维码失败，请稍后重试')
  } finally {
    qrCodeLoading.value = false
  }
}

watch(() => activeTab.value, (newTab) => {
  if (newTab === 'quick') {
    generateQRCode()
  }
})

const handleLogin = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const result = await userStore.login({
          username: form.username,
          password: form.password,
          role: form.role
        })

        if (result.success) {
          ElMessage.success('登录成功')
          router.push(`/${userStore.userRole}/dashboard`)
        } else {
          ElMessage.error(result.message)
        }
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<style scoped>
.login-container {
  display: flex;
  min-height: 100vh;
  background-image: url('/images/login-bg.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}
.login-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1;
}
.login-left {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  width: 50%;
  padding: 48px;
  position: relative;
  z-index: 10;
}
@media (min-width: 1024px) {
  .login-left {
    display: flex;
  }
}
.login-left-header {
  display: flex;
  align-items: center;
  gap: 12px;
}
.login-logo {
  width: 48px;
  height: 48px;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.login-logo i {
  color: white;
  font-size: 20px;
}
.login-left-header h1 {
  color: white;
  font-size: 20px;
  font-weight: bold;
}
.login-left-header p {
  color: rgba(191, 219, 254, 1);
  font-size: 14px;
}
.login-left-content {
  gap: 32px;
  display: flex;
  flex-direction: column;
}
.login-left-content h2 {
  color: white;
  font-size: 36px;
  font-weight: bold;
  line-height: 1.2;
}
.login-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}
.stat-card {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 16px;
}
.stat-number {
  color: white;
  font-size: 36px;
  font-weight: bold;
}
.stat-label {
  color: rgba(191, 219, 254, 1);
  font-size: 14px;
}
.login-left-footer {
  display: flex;
  align-items: center;
  gap: 24px;
  color: rgba(191, 219, 254, 1);
  font-size: 14px;
}
.login-right {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px;
  position: relative;
  z-index: 10;
}
@media (min-width: 1024px) {
  .login-right {
    width: 50%;
  }
}
.login-form-container {
  width: 100%;
  max-width: 448px;
}
.login-mobile-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 32px;
}
@media (min-width: 1024px) {
  .login-mobile-header {
    display: none;
  }
}
.login-mobile-header h1 {
  color: white;
  font-size: 20px;
  font-weight: bold;
}
.login-form-card {
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  padding: 32px;
}
.login-form-header {
  text-align: center;
  margin-bottom: 32px;
}
.login-form-header h2 {
  color: #111827;
  font-size: 24px;
  font-weight: bold;
}
.login-form-header p {
  color: #6b7280;
  margin-top: 8px;
}
.login-form-body {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.login-tabs :deep(.el-tabs__header) {
  margin-bottom: 24px;
}
.login-tabs :deep(.el-tabs__nav-wrap::after) {
  display: none;
}
.login-tabs :deep(.el-tabs__active-bar) {
  height: 3px;
  border-radius: 2px;
}
.login-tabs :deep(.el-tabs__item) {
  font-size: 16px;
  height: 48px;
  line-height: 48px;
}
.login-tabs :deep(.el-tabs__item.is-active) {
  color: #3b82f6;
}
.login-tabs :deep(.el-form-item__label) {
  font-weight: 500;
}
.login-options {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}
.forgot-password {
  color: #2563eb;
  font-size: 14px;
  text-decoration: none;
}
.forgot-password:hover {
  color: #1d4ed8;
}
.login-button {
  width: 100%;
}
.quick-login {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 16px 0;
}
.wechat-qr-container {
  display: flex;
  justify-content: center;
  padding: 20px 0;
}
.wechat-qr-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}
.wechat-icon {
  font-size: 48px;
  color: #22c55e;
}
.wechat-qr-code {
  width: 200px;
  height: 200px;
  background: linear-gradient(135deg, #f0f9eb 0%, #e8f5e9 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dashed #22c55e;
}
.qr-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #22c55e;
}
.qr-icon {
  font-size: 48px;
}
.qr-placeholder p {
  font-size: 14px;
  font-weight: 500;
}
.qr-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #22c55e;
}
.qr-loading i {
  font-size: 32px;
}
.qr-code-img {
  width: 180px;
  height: 180px;
  border-radius: 8px;
}
.refresh-qr-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background-color: #f3f4f6;
  border: none;
  border-radius: 8px;
  color: #6b7280;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}
.refresh-qr-btn:hover {
  background-color: #e5e7eb;
  color: #22c55e;
}
.wechat-tip {
  color: #6b7280;
  font-size: 14px;
}
.quick-login-divider {
  display: flex;
  align-items: center;
  gap: 16px;
  color: #9ca3af;
  font-size: 14px;
}
.quick-login-divider::before,
.quick-login-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background-color: #e5e7eb;
}
.quick-login-options {
  display: flex;
  gap: 12px;
}
.quick-login-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  border-radius: 12px;
  border: none;
  color: white;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.15s;
}
.quick-login-btn i {
  font-size: 18px;
}
.quick-login-btn.wechat {
  background-color: #22c55e;
}
.quick-login-btn.wechat:hover {
  background-color: #16a34a;
}
.login-form-footer {
  margin-top: 24px;
  text-align: center;
}
.login-form-footer p {
  color: #6b7280;
  font-size: 14px;
}
.register-link {
  color: #2563eb;
  font-weight: 500;
  text-decoration: none;
}
.register-link:hover {
  color: #1d4ed8;
}
</style>
