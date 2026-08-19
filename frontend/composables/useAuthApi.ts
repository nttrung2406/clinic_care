import type { LoginPayload, LoginResponse } from '~/types'

export function useAuthApi() {
  const config = useRuntimeConfig()

  const login = (payload: LoginPayload) =>
    $fetch<LoginResponse>('/auth/login', {
      baseURL: config.public.apiBase,
      method: 'POST',
      body: payload,
    })

  return { login }
}
