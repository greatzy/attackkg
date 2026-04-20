import request from './request'
import type { 
  Tactic, 
  Technique, 
  SubTechnique, 
  Mitigation, 
  Software,
  PaginatedResponse 
} from '@/types'

// Tactics
export const getTactics = (params?: { page?: number; per_page?: number; search?: string }) => {
  return request.get<PaginatedResponse<Tactic>>('/tactics', { params })
}

export const getTactic = (tacticId: string) => {
  return request.get<{ data: Tactic }>(`/tactics/${tacticId}`)
}

export const getTacticTechniques = (tacticId: string, params?: { page?: number; per_page?: number }) => {
  return request.get<PaginatedResponse<Technique>>(`/tactics/${tacticId}/techniques`, { params })
}

// Techniques
export const getTechniques = (params?: { 
  page?: number; 
  per_page?: number; 
  search?: string;
  tactic_id?: string;
  platform?: string;
}) => {
  return request.get<PaginatedResponse<Technique>>('/techniques', { params })
}

export const getTechnique = (techniqueId: string) => {
  return request.get<{ data: Technique }>(`/techniques/${techniqueId}`)
}

export const createTechnique = (data: Partial<Technique>) => {
  return request.post<{ message: string; data: Technique }>('/techniques', data)
}

export const updateTechnique = (techniqueId: string, data: Partial<Technique>) => {
  return request.put<{ message: string; data: Technique }>(`/techniques/${techniqueId}`, data)
}

export const deleteTechnique = (techniqueId: string) => {
  return request.delete<{ message: string }>(`/techniques/${techniqueId}`)
}

export const getTechniqueSubtechniques = (techniqueId: string) => {
  return request.get<{ data: SubTechnique[] }>(`/techniques/${techniqueId}/subtechniques`)
}

// SubTechniques
export const getSubtechniques = (params?: { page?: number; per_page?: number; technique_id?: string }) => {
  return request.get<PaginatedResponse<SubTechnique>>('/subtechniques', { params })
}

export const getSubtechnique = (subtechniqueId: string) => {
  return request.get<{ data: SubTechnique }>(`/subtechniques/${subtechniqueId}`)
}

// Mitigations
export const getMitigations = (params?: { page?: number; per_page?: number; search?: string }) => {
  return request.get<PaginatedResponse<Mitigation>>('/mitigations', { params })
}

export const getMitigation = (mitigationId: string) => {
  return request.get<{ data: Mitigation }>(`/mitigations/${mitigationId}`)
}

// Software
export const getSoftware = (params?: { page?: number; per_page?: number; search?: string; type?: string }) => {
  return request.get<PaginatedResponse<Software>>('/software', { params })
}

export const getSoftwareById = (softwareId: string) => {
  return request.get<{ data: Software }>(`/software/${softwareId}`)
}

// Search
export const searchAttack = (q: string) => {
  return request.get<{
    tactics: Tactic[];
    techniques: Technique[];
    software: Software[];
    total: number;
  }>('/search', { params: { q } })
}

// Statistics
export const getStatistics = () => {
  return request.get<{
    tactics: number;
    techniques: number;
    subtechniques: number;
    mitigations: number;
    software: { total: number; malware: number; tools: number };
    platforms: number;
  }>('/statistics')
}

// Matrix
export interface MatrixTactic {
  tactic_id: string
  name: string
  description: string
  url: string
  techniques: MatrixTechnique[]
}

export interface MatrixTechnique {
  technique_id: string
  name: string
  description: string
  url: string
  tactic_id: string
  platforms: string[]
  is_subtechnique: boolean
}

export const getAttackMatrix = (platform?: string) => {
  return request.get<{
    matrix: MatrixTactic[]
    total_tactics: number
    total_techniques: number
  }>('/visualization/attack_matrix', { params: { platform } })
}

// Attack Paths
export const getAttackPaths = (tacticId?: string) => {
  return request.get<{
    nodes: any[]
    edges: any[]
    total_nodes: number
    total_edges: number
  }>('/visualization/attack_paths', { params: { tactic_id: tacticId } })
}
