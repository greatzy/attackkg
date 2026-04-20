import axios, { type AxiosInstance, type AxiosRequestConfig, type AxiosResponse } from 'axios'
import type { ApiResponse } from '@/types'
import { useUserStore } from '@/stores/user'
import router from '@/router'
import { ElMessage } from 'element-plus'

// 创建axios实例
const service: AxiosInstance = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json;charset=UTF-8'
  }
})

// 请求拦截器
service.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    const userStore = useUserStore()
    if (userStore.token) {
      config.headers = config.headers || {}
      config.headers.Authorization = `Bearer ${userStore.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  (response: AxiosResponse) => {
    const { data, status } = response
    
    // 成功响应
    if (status === 200) {
      return data
    }
    
    // 业务逻辑错误
    ElMessage.error(data?.message || '请求失败')
    return Promise.reject(new Error(data?.message || '请求失败'))
  },
  async (error) => {
    const { response } = error
    
    if (response) {
      const userStore = useUserStore()
      
      switch (response.status) {
        // 401: 未授权
        case 401:
          ElMessage.error('会话已过期，请重新登录')
          userStore.logout()
          router.push('/login')
          break
        
        // 403: 禁止访问
        case 403:
          ElMessage.error('权限不足，无法访问')
          break
        
        // 404: 资源未找到
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        
        // 422: 验证错误
        case 422:
          const errors = response.data?.errors
          if (errors) {
            const errorMessages = Object.values(errors).flat()
            ElMessage.error(errorMessages[0])
          } else {
            ElMessage.error(response.data?.message || '验证失败')
          }
          break
        
        // 500: 服务器错误
        case 500:
          ElMessage.error('服务器内部错误')
          break
        
        // 其他错误
        default:
          ElMessage.error(response.data?.message || '请求失败')
      }
    } else if (error.code === 'ERR_NETWORK') {
      ElMessage.error('网络错误，请检查网络连接')
    } else if (error.code === 'ECONNABORTED') {
      ElMessage.error('请求超时，请重试')
    }
    
    return Promise.reject(error)
  }
)

// 请求方法封装
export default {
  get<T = any>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    return service.get(url, config)
  },
  
  post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    return service.post(url, data, config)
  },
  
  put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    return service.put(url, data, config)
  },
  
  delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    return service.delete(url, config)
  },
  
  patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    return service.patch(url, data, config)
  }
}
