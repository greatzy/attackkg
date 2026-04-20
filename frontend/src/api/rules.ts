import request from './request'
import type { DetectionRule } from '@/types'

export interface RuleQueryParams {
  page?: number
  per_page?: number
  search?: string
  rule_type?: string
  status?: string
  sort_by?: string
  sort_order?: 'asc' | 'desc'
}

export interface RuleListResponse {
  items: DetectionRule[]
  total: number
  page: number
  per_page: number
  pages: number
}

export const getRules = (params?: RuleQueryParams) => {
  return request.get<RuleListResponse>('/rules', { params })
}

export const getRule = (id: string) => {
  return request.get<DetectionRule>(`/rules/${id}`)
}

export const createRule = (data: Partial<DetectionRule>) => {
  return request.post<DetectionRule>('/rules', data)
}

export const updateRule = (id: string, data: Partial<DetectionRule>) => {
  return request.put<DetectionRule>(`/rules/${id}`, data)
}

export const deleteRule = (id: string) => {
  return request.delete(`/rules/${id}`)
}

export const validateRule = (id: string) => {
  return request.post(`/rules/${id}/validate`)
}

export const exportRules = (params?: RuleQueryParams) => {
  return request.get('/rules/export', { 
    params,
    responseType: 'blob'
  })
}
