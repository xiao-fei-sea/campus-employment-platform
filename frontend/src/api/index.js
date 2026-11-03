import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  },
  maxRedirects: 0
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

let isRedirecting = false

api.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config
    if (error.response?.status === 307 && originalRequest && !originalRequest._retry) {
      originalRequest._retry = true
      const location = error.response.headers['location']
      if (location) {
        const token = localStorage.getItem('token')
        if (token) {
          originalRequest.headers['Authorization'] = `Bearer ${token}`
        }
        return api(originalRequest)
      }
    }

    if (error.response) {
      const { status, data } = error.response
      const isLoginRequest = error.config?.url?.includes('/auth/login')
      const skipRedirect = error.config?.headers?.['X-Skip-Redirect'] === true

      if (skipRedirect) {
        return Promise.reject(error)
      }

      switch (status) {
        case 401:
          if (!isLoginRequest && !isRedirecting) {
            isRedirecting = true
            ElMessage.error('登录已过期，请重新登录')
            console.error('401 Error - Redirecting to login. URL:', error.config?.url)
            console.error('401 Error - Token:', localStorage.getItem('token'))
          }
          break
        case 403:
          ElMessage.error('没有权限访问')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 500:
          ElMessage.error('服务器错误，请稍后重试')
          break
        default:
          if (!isLoginRequest) {
            ElMessage.error(data.message || '请求失败')
          }
      }
    } else {
      ElMessage.error('网络错误，请检查您的连接')
    }

    return Promise.reject(error)
  }
)

export default api

export const authAPI = {
  login: (data) => api.post('/auth/login', data),
  register: (data) => api.post('/auth/register', data),
  me: () => api.get('/auth/me'),
  getWechatQRCode: () => api.get('/auth/wechat/qrcode'),
  getWechatQRStatus: (scene) => api.get(`/auth/wechat/qrstatus/${scene}`),
  getPublicStats: () => api.get('/auth/public/stats'),
  changePassword: (data) => api.post('/auth/password', data),
  getPreferences: () => api.get('/auth/preferences'),
  savePreferences: (data) => api.put('/auth/preferences', data)
}

export const studentAPI = {
  getDashboard: () => api.get('/student/dashboard/'),
  getJobs: (params) => api.get('/student/jobs/', { params }),
  getJobDetail: (id) => api.get(`/student/jobs/${id}`),
  collectJob: (id) => api.post(`/student/jobs/${id}/collect`),
  cancelCollect: (id) => api.delete(`/student/jobs/${id}/collect`),
  applyJob: (id, data = {}) => api.post(`/student/jobs/${id}/apply`, data),
  withdrawApplication: (id) => api.post(`/student/applications/${id}/withdraw`),
  getApplications: (params) => api.get('/student/applications/', { params }),
  getFavorites: (params) => api.get('/student/jobs/favorites', { params }),
  getCareerTalks: (params) => api.get('/student/career-talks/', { params }),
  getCareerTalk: (id) => api.get(`/student/career-talks/${id}`),
  getCareerTalkDetail: (id) => api.get(`/student/career-talks/${id}`),
  registerCareerTalk: (id, data) => api.post(`/student/career-talks/${id}/register`, data),
  cancelCareerTalk: (id) => api.delete(`/student/career-talks/${id}/cancel`),
  cancelCareerTalkRegistration: (id) => api.delete(`/student/career-talks/${id}/cancel`),
  getProfile: () => api.get('/student/profile/'),
  updateProfile: (data) => api.put('/student/profile/', data),
  getSettings: () => api.get('/student/profile/'),
  updateSettings: (data) => api.put('/student/profile/', data),
  uploadAvatar: (formData) => api.post('/student/profile/avatar', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  getResumes: (params) => api.get('/student/resumes/', { params }),
  createResume: (data) => api.post('/student/resumes/', data),
  updateResume: (id, data) => api.put(`/student/resumes/${id}`, data),
  deleteResume: (id) => api.delete(`/student/resumes/${id}`),
  getResumeSuggestions: (id) => api.post(`/student/resumes/${id}/suggestions`),
  uploadResume: (formData) => api.post('/student/resumes/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  setDefaultResume: (id) => api.post(`/student/resumes/${id}/set-default`),
  getMessages: (params) => api.get('/student/messages/', { params }),
  getUnreadMessageCount: () => api.get('/student/messages/unread-count'),
  markMessageRead: (id) => api.post(`/student/messages/${id}/read`),
  markAllMessagesRead: () => api.post('/student/messages/read-all'),
  deleteMessage: (id) => api.delete(`/student/messages/${id}`)
}

export const companyAPI = {
  getJobs: (params) => api.get('/company/jobs/', { params }),
  createJob: (data) => api.post('/company/jobs/', data),
  updateJob: (id, data) => api.put(`/company/jobs/${id}`, data),
  deleteJob: (id) => api.delete(`/company/jobs/${id}`),
  getJobApplicants: (id, params) => api.get(`/company/jobs/${id}/applicants/`, { params }),
  reviewApplication: (id, data) => api.put(`/company/resumes/applications/${id}/status`, data),
  getResumes: (params) => api.get('/company/resumes/applications/', { params }),
  getResumeDetail: (id) => api.get(`/company/resumes/applications/${id}`),
  getTalks: (params) => api.get('/company/career-talks/', { params }),
  createTalk: (data) => api.post('/company/career-talks/', data),
  updateTalk: (id, data) => api.put(`/company/career-talks/${id}`, data),
  deleteTalk: (id) => api.delete(`/company/career-talks/${id}`),
  getTalkRegistrations: (id) => api.get(`/company/career-talks/${id}/registrations`),
  getAnalytics: (params) => api.get('/company/analytics/', { params }),
  getDashboard: () => api.get('/company/dashboard/'),
  getSettings: () => api.get('/company/profile/'),
  updateSettings: (data) => api.put('/company/profile/', data),
  uploadLogo: (formData) => api.post('/company/profile/logo', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  uploadLicense: (formData) => api.post('/company/license/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

export const adminAPI = {
  get: (path) => api.get(path),
  getDashboardStats: () => api.get('/admin/statistics/stats'),
  getStudents: (params) => api.get('/admin/students', { params }),
  createStudent: (data) => api.post('/admin/students', data),
  getStudentDetail: (id) => api.get(`/admin/students/${id}`),
  updateStudent: (id, data) => api.put(`/admin/students/${id}`, data),
  updateStudentStatus: (id, data) => api.put(`/admin/students/${id}/status`, data),
  getCompanies: (params) => api.get('/admin/companies', { params }),
  getCompanyDetail: (id) => api.get(`/admin/companies/${id}`),
  approveCompany: (id) => api.post(`/admin/companies/${id}/approve`),
  rejectCompany: (id) => api.post(`/admin/companies/${id}/reject`),
  blacklistCompany: (id) => api.post(`/admin/companies/${id}/blacklist`),
  removeBlacklistCompany: (id) => api.delete(`/admin/companies/${id}/remove-blacklist`),
  getJobs: (params) => api.get('/admin/jobs', { params }),
  approveJob: (id) => api.post(`/admin/jobs/${id}/approve`, { status: 'approved' }),
  rejectJob: (id, data) => api.post(`/admin/jobs/${id}/approve`, data),
  getActivities: (params) => api.get('/admin/activities/career-talks', { params }),
  getActivityDetail: (id) => api.get(`/admin/activities/career-talks/${id}`),
  approveActivity: (id, data) => api.post(`/admin/activities/career-talks/${id}/approve`, data),
  createActivity: (data) => api.post('/admin/activities/career-talks', data),
  updateActivity: (id, data) => api.put(`/admin/activities/career-talks/${id}`, data),
  deleteActivity: (id) => api.delete(`/admin/activities/career-talks/${id}`),
  getStatistics: (params) => api.get('/admin/statistics/stats', { params }),
  getDepartmentStats: (params) => api.get('/admin/statistics/department-stats', { params }),
  getMajorStats: (params) => api.get('/admin/statistics/major-stats', { params }),
  getSalaryDistribution: (params) => api.get('/admin/statistics/salary-distribution', { params }),
  getEmploymentTrend: (params) => api.get('/admin/statistics/employment-trend', { params }),
  getEmploymentStatusDistribution: () => api.get('/admin/statistics/employment-status-distribution'),
  getRegionDistribution: () => api.get('/admin/statistics/region-distribution'),
  getConversionFunnel: () => api.get('/admin/statistics/conversion-funnel'),
  getCompanyScaleDistribution: () => api.get('/admin/statistics/company-scale-distribution'),
  getActivityStats: () => api.get('/admin/statistics/activity-stats'),
  exportReport: (params) => api.get('/admin/statistics/export', { params, responseType: 'blob' }),
  getSettings: () => api.get('/admin/system'),
  updateSettings: (data) => api.put('/admin/system', data),
  getAdminUsers: () => api.get('/admin/system/users'),
  createAdminUser: (data) => api.post('/admin/system/users', data),
  updateAdminUser: (id, data) => api.put(`/admin/system/users/${id}`, data),
  deleteAdminUser: (id) => api.delete(`/admin/system/users/${id}`),
  getRoles: () => api.get('/admin/system/roles'),
  updateRolePermissions: (id, data) => api.put(`/admin/system/roles/${id}`, data),
  getOperationLogs: (params) => api.get('/admin/system/operation-logs', { params }),
  getBackups: () => api.get('/admin/system/backups'),
  createBackup: () => api.post('/admin/system/backup'),
  downloadBackup: (filename) => api.get(`/admin/system/backups/${filename}`, { responseType: 'blob' }),
  deleteBackup: (filename) => api.delete(`/admin/system/backups/${filename}`)
}
