export function useAuth() {
  const token = useCookie<string | null>('auth_token', {
    default: () => null,
    sameSite: 'lax',
  })

  const isLoggedIn = computed(() => Boolean(token.value))

  function setToken(value: string) {
    token.value = value
  }

  function logout() {
    token.value = null
  }

  return { token, isLoggedIn, setToken, logout }
}
