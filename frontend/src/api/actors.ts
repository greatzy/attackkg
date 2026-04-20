import request from './request'
import type { ThreatActor, ActorTechnique, ActorSoftware, PaginatedResponse } from '@/types'

export const getActors = (params?: { page?: number; per_page?: number; search?: string; origin?: string; motivation?: string }) => {
  return request.get<PaginatedResponse<ThreatActor>>('/actors', { params })
}

export const getActor = (actorId: string) => {
  return request.get<{ data: ThreatActor }>(`/actors/${actorId}`)
}

export const createActor = (data: Partial<ThreatActor>) => {
  return request.post<{ message: string; actor: ThreatActor }>('/actors', data)
}

export const updateActor = (actorId: string, data: Partial<ThreatActor>) => {
  return request.put<{ message: string; actor: ThreatActor }>(`/actors/${actorId}`, data)
}

export const deleteActor = (actorId: string) => {
  return request.delete<{ message: string }>(`/actors/${actorId}`)
}

export const getActorTechniques = (actorId: string) => {
  return request.get<{ data: ActorTechnique[] }>(`/actors/${actorId}/techniques`)
}

export const getActorSoftware = (actorId: string) => {
  return request.get<{ data: ActorSoftware[] }>(`/actors/${actorId}/software`)
}
