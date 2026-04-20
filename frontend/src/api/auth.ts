import request from './request'
import type { LoginForm, UserInfo } from '@/types'

export const login = (data: LoginForm) => {
  return request.post<{
    access_token: string
    user: UserInfo
  }>('/auth/login', data)
}

export const getUserInfo = () => {
  return request.get<UserInfo>('/auth/profile')
}

export const logout = () => {
  return request.post('/auth/logout')
}

export const refreshToken = () => {
  return request.post<{
    access_token: string
  }>('/auth/refresh')
}
