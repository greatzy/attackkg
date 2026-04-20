import request from './request'
import type { PaginatedResponse } from '@/types'

export interface Report {
  id: number
  title: string
  description: string
  report_type: string
  format: string
  status: string
  content?: string
  file_path?: string
  file_size?: number
  parameters?: Record<string, any>
  technique_ids?: string[]
  actor_ids?: string[]
  tactic_ids?: string[]
  page_count?: number
  generation_time?: number
  created_by?: number
  creator_name?: string
  download_url?: string
  created_at: string
  updated_at: string
}

export interface CreateReportParams {
  title: string
  description?: string
  report_type: string
  format?: string
  parameters?: Record<string, any>
  technique_ids?: string[]
  actor_ids?: string[]
  tactic_ids?: string[]
}

export interface ReportGenerateParams {
  title: string
  description?: string
  report_type: 'attack_path' | 'technique_detail' | 'threat_assessment' | 'custom'
  format?: 'pdf' | 'word' | 'excel' | 'html'
  technique_ids?: string[]
  actor_ids?: string[]
  tactic_ids?: string[]
}

export const getReports = (params?: {
  page?: number
  per_page?: number
  search?: string
}) => {
  return request.get<PaginatedResponse<Report>>('/reports', { params })
}

export const getReport = (reportId: number) => {
  return request.get<{ data: Report }>(`/reports/${reportId}`)
}

export const createReport = (data: CreateReportParams) => {
  return request.post<{ message: string; report: Report }>('/reports', data)
}

export const updateReport = (reportId: number, data: Partial<Report>) => {
  return request.put<{ message: string; report: Report }>(`/reports/${reportId}`, data)
}

export const deleteReport = (reportId: number) => {
  return request.delete<{ message: string }>(`/reports/${reportId}`)
}

export const generateReport = (reportId: number) => {
  return request.post<{
    report_id: number
    name: string
    status: string
    download_url: string
  }>(`/reports/${reportId}/generate`)
}

export const downloadReport = (reportId: number) => {
  return request.get<{ message: string; file_path?: string }>(`/reports/${reportId}/download`)
}