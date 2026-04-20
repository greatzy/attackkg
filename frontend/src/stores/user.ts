import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login, getUserInfo as fetchUserInfo } from '@/api/auth'
import type { LoginForm, UserInfo } from '@/types'

export const useUserStore = defineStore('user', () => {
  // State
  const token = ref<string>('')
  const userInfo = ref<UserInfo | null>(null)
  
  // Getters
  const isLoggedIn = computed(() => !!token.value)
  const username = computed(() => userInfo.value?.username || '')
  const isAdmin = computed(() => userInfo.value?.is_admin || false)
  const permissions = computed(() => userInfo.value?.permissions || [])
  
  // Actions
  const setToken = (newToken: string) => {
    token.value = newToken
  }
  
  const setUserInfo = (info: UserInfo) => {
    userInfo.value = info
  }
  
  const loginAction = async (loginForm: LoginForm) => {
    const res = await login(loginForm)
    const { access_token, user } = res
    setToken(access_token)
    setUserInfo(user)
    return res
  }
  
  const getUserInfo = async () => {
    const res = await fetchUserInfo()
    setUserInfo(res)
    return res
  }
  
  const logout = () => {
    token.value = ''
    userInfo.value = null
  }
  
  const initialize = () => {
    // Token is automatically restored by pinia-plugin-persistedstate
    // This function can be used for additional initialization
  }
  
  const hasPermission = (permission: string): boolean => {
    if (isAdmin.value) return true
    return permissions.value.includes(permission)
  }
  
  return {
    token,
    userInfo,
    isLoggedIn,
    username,
    isAdmin,
    permissions,
    setToken,
    setUserInfo,
    loginAction,
    getUserInfo,
    logout,
    initialize,
    hasPermission
  }
}, {
  persist: {
    key: 'user',
    paths: ['token', 'userInfo']
  }
})
