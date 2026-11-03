import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('userInfo') || '{}'))
  const userRole = ref(localStorage.getItem('userRole') || '')

  const isLoggedIn = computed(() => !!token.value)

  async function login(loginData) {
    try {
      let response
      if (loginData.phone) {
        response = await api.post('/auth/phone/login', loginData)
      } else {
        response = await api.post('/auth/login', loginData)
      }
      const { access_token } = response.data
      token.value = access_token
      localStorage.setItem('token', access_token)

      const userResponse = await api.get('/auth/me')
      userInfo.value = userResponse.data
      userRole.value = userResponse.data.role
      localStorage.setItem('userInfo', JSON.stringify(userResponse.data))
      localStorage.setItem('userRole', userResponse.data.role)

      return { success: true, data: { token: access_token, user: userResponse.data } }
    } catch (error) {
      token.value = ''
      userInfo.value = {}
      userRole.value = ''
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
      localStorage.removeItem('userRole')
      return { success: false, message: error.response?.data?.detail || '登录失败' }
    }
  }

  async function register(registerData) {
    try {
      const response = await api.post('/auth/register', registerData)
      return { success: true, data: response.data }
    } catch (error) {
      return { success: false, message: error.response?.data?.message || '注册失败' }
    }
  }

  function logout() {
    token.value = ''
    userInfo.value = {}
    userRole.value = ''
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
    localStorage.removeItem('userRole')
  }

  async function fetchUserInfo() {
    try {
      const response = await api.get('/auth/me')
      userInfo.value = response.data
      localStorage.setItem('userInfo', JSON.stringify(response.data))
    } catch (error) {
      console.error('获取用户信息失败', error)
    }
  }

  return {
    token,
    userInfo,
    userRole,
    isLoggedIn,
    login,
    register,
    logout,
    fetchUserInfo
  }
})
