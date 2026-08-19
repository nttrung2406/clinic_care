import type { DiagnosisCode } from '~/types'

export function useDiagnosisApi() {
  const config = useRuntimeConfig()

  const search = (term: string, limit = 50) =>
    $fetch<DiagnosisCode[]>('/diagnosis', {
      baseURL: config.public.apiBase,
      params: term ? { search: term, limit } : { limit },
    })

  return { search }
}
