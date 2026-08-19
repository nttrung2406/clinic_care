import type { DiagnosisCode } from '~/types'

export function useDiagnosisApi() {
  const config = useRuntimeConfig()
  const { token, logout } = useAuth()

  const search = (term: string, limit = 50) =>
    $fetch<DiagnosisCode[]>('/diagnosis', {
      baseURL: config.public.apiBase,
      params: term ? { search: term, limit } : { limit },
      headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined,
      onResponseError({ response }) {
        if (response.status === 401) {
          logout()
          navigateTo('/login')
        }
      },
    })

  return { search }
}
