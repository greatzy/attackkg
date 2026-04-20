export interface ApiResponse<T> {
  [key: string]: any
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  pages: number
  page: number
  per_page: number
  has_next: boolean
  has_prev: boolean
}

// ATT&CK Data Types
export interface Tactic {
  id: number
  tactic_id: string
  name: string
  description: string
  short_name?: string
  url?: string
  version?: string
  created_at: string
  updated_at: string
  technique_count?: number
}

export interface Technique {
  id: number
  technique_id: string
  name: string
  description: string
  tactic_id: string
  platforms?: string[]
  permissions_required?: string[]
  data_sources?: string[]
  defense_bypassed?: string[]
  detection?: string
  url?: string
  version?: string
  is_subtechnique: boolean
  created_at: string
  updated_at: string
  subtechnique_count?: number
  tactic_name?: string
}

export interface SubTechnique {
  id: number
  subtechnique_id: string
  name: string
  description: string
  technique_id: string
  platforms?: string[]
  permissions_required?: string[]
  data_sources?: string[]
  defense_bypassed?: string[]
  detection?: string
  url?: string
  version?: string
  created_at: string
  updated_at: string
  parent_technique_name?: string
}

export interface Mitigation {
  id: number
  mitigation_id: string
  name: string
  description: string
  url?: string
  version?: string
  created_at: string
  updated_at: string
}

export interface Software {
  id: number
  software_id: string
  name: string
  type: string
  description: string
  platforms?: string[]
  aliases?: string[]
  url?: string
  version?: string
  created_at: string
  updated_at: string
}

// Threat Actor Types
export interface ThreatActor {
  id: number
  actor_id: string
  name: string
  aliases?: string[]
  description: string
  first_seen?: string
  last_seen?: string
  motivation?: string
  origin?: string
  targets?: string[]
  tools_used?: string[]
  url?: string
  version?: string
  created_at: string
  updated_at: string
  technique_count?: number
  software_count?: number
}

export interface ActorTechnique {
  id: number
  actor_id: string
  technique_id: string
  usage_description?: string
  created_at: string
  updated_at: string
  technique_name?: string
  tactic_id?: string
}

export interface ActorSoftware {
  id: number
  actor_id: string
  software_id: string
  usage_description?: string
  created_at: string
  updated_at: string
  software_name?: string
  software_type?: string
}

// Detection Rule Types
export interface DetectionRule {
  id: number
  name: string
  description?: string
  rule_type: string
  content: string
  language?: string
  severity: string
  status: string
  platform?: string
  data_source?: string
  false_positives?: string
  references?: string[]
  tags?: string[]
  author?: string
  created_by?: number
  version: number
  created_at: string
  updated_at: string
  creator_name?: string
  technique_count?: number
}

export interface RuleTechnique {
  id: number
  rule_id: number
  technique_id: string
  coverage_level?: string
  notes?: string
  created_at: string
  updated_at: string
  technique_name?: string
  tactic_id?: string
}

// Threat Intelligence Types
export interface ThreatIntelligence {
  id: number
  title: string
  description?: string
  source?: string
  source_type?: string
  threat_type?: string
  severity: string
  confidence: string
  status: string
  technique_ids?: string[]
  actor_ids?: string[]
  software_ids?: string[]
  iocs?: any[]
  first_seen?: string
  last_seen?: string
  published_at?: string
  risk_score?: number
  risk_factors?: any
  references?: string[]
  raw_data?: any
  tags?: string[]
  created_by?: number
  created_at: string
  updated_at: string
  creator_name?: string
}

// Report Types
export interface Report {
  id: number
  title: string
  description?: string
  report_type: string
  format: string
  status: string
  content?: string
  file_path?: string
  file_size?: number
  parameters?: any
  technique_ids?: string[]
  actor_ids?: string[]
  tactic_ids?: string[]
  page_count?: number
  generation_time?: number
  created_by?: number
  created_at: string
  updated_at: string
  creator_name?: string
  download_url?: string
}

// User Types
export interface User {
  id: number
  username: string
  email: string
  full_name?: string
  department?: string
  phone?: string
  is_active: boolean
  is_admin: boolean
  last_login?: string
  login_count: number
  created_at: string
  updated_at: string
  roles?: string[]
  permissions?: string[]
}

export interface Role {
  id: number
  name: string
  description?: string
  is_system: boolean
  created_at: string
  updated_at: string
  permissions?: string[]
  user_count?: number
}

export interface Permission {
  id: number
  name: string
  resource: string
  action: string
  description?: string
  created_at: string
  updated_at: string
}

export interface LoginForm {
  username: string
  password: string
  remember?: boolean
}

export interface UserInfo {
  id: number
  username: string
  email: string
  full_name?: string
  department?: string
  phone?: string
  is_admin: boolean
  roles: string[]
  permissions: string[]
}

// Operation Log Types
export interface OperationLog {
  id: number
  user_id?: number
  username?: string
  ip_address?: string
  user_agent?: string
  action: string
  resource_type?: string
  resource_id?: string
  resource_name?: string
  method?: string
  path?: string
  request_data?: any
  response_status?: number
  description?: string
  result?: string
  error_message?: string
  duration?: number
  created_at: string
  updated_at: string
}

// Statistics Types
export interface AttackStatistics {
  tactics: number
  techniques: number
  subtechniques: number
  mitigations: number
  software: {
    total: number
    malware: number
    tools: number
  }
  platforms: number
}
