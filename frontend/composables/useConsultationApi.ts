import type { Consultation, ConsultationCreatePayload, ConsultationSearchParams } from '~/types'

export function useConsultationApi() {
  const config = useRuntimeConfig()

  const list = (params: ConsultationSearchParams = {}) =>
    $fetch<Consultation[]>('/consultation', { baseURL: config.public.apiBase, params })

  const create = (payload: ConsultationCreatePayload) =>
    $fetch<Consultation>('/consultation', {
      baseURL: config.public.apiBase,
      method: 'POST',
      body: payload,
    })

  return { list, create }
}
