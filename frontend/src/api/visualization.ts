import request from './request'

export interface GraphNode {
  id: string
  name: string
  type: 'tactic' | 'technique'
  category: string
  value: number
  is_subtechnique?: boolean
  description?: string
  url?: string
}

export interface GraphEdge {
  source: string
  target: string
  type: 'belongs_to' | 'leads_to'
}

export interface AttackPathsResponse {
  nodes: GraphNode[]
  edges: GraphEdge[]
  total_nodes: number
  total_edges: number
}

export const getAttackPaths = (tacticId?: string) => {
  return request.get<AttackPathsResponse>('/visualization/attack_paths', {
    params: tacticId ? { tactic_id: tacticId } : undefined
  })
}

export interface TechniqueByTactic {
  name: string
  id: string
  techniques: number
}

export const getTechniquesByTactic = () => {
  return request.get<TechniqueByTactic[]>('/visualization/techniques_by_tactic')
}

export interface TechniqueByPlatform {
  name: string
  count: number
}

export const getTechniquesByPlatform = () => {
  return request.get<TechniqueByPlatform[]>('/visualization/techniques_by_platform')
}

export interface MitigationsStatistics {
  total_mitigations: number
  most_used_techniques: Array<{ name: string; count: number }>
  mitigations_by_category: Record<string, number>
}

export const getMitigationsStatistics = () => {
  return request.get<MitigationsStatistics>('/visualization/mitigations_statistics')
}

export interface DashboardData {
  stats: {
    tactics: number
    techniques: number
    subtechniques: number
    mitigations: number
    rules: number
    actors: number
  }
  recent_activity: Array<{
    type: string
    id: string
    name: string
    timestamp: string
    action: string
  }>
  risk_scores: {
    high: number
    medium: number
    low: number
  }
}

export const getDashboardData = () => {
  return request.get<DashboardData>('/visualization/dashboard')
}
