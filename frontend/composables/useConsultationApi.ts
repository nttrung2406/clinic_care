import type { Consultation, ConsultationCreatePayload, ConsultationSearchParams } from '~/types'

export function useConsultationApi() {
  const config = useRuntimeConfig()
  const { token, logout } = useAuth()

  function authHeaders() {
    return token.value ? { Authorization: `Bearer ${token.value}` } : undefined
  }

  function onResponseError({ response }: { response: { status: number } }) {
    if (response.status === 401) {
      logout()
      navigateTo('/login')
    }
  }

  const list = (params: ConsultationSearchParams = {}) =>
    $fetch<Consultation[]>('/consultation', {
      baseURL: config.public.apiBase,
      params,
      headers: authHeaders(),
      onResponseError,
    })

  const create = (payload: ConsultationCreatePayload) =>
    $fetch<Consultation>('/consultation', {
      baseURL: config.public.apiBase,
      method: 'POST',
      body: payload,
      headers: authHeaders(),
      onResponseError,
    })

  return { list, create }
}
