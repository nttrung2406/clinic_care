<script setup lang="ts">
const { login } = useAuthApi()
const { setToken, isLoggedIn } = useAuth()

if (isLoggedIn.value) {
  await navigateTo('/consultations')
}

const username = ref('')
const password = ref('')
const loading = ref(false)
const errorMessage = ref('')

async function onSubmit() {
  errorMessage.value = ''
  loading.value = true
  try {
    const { access_token } = await login({ username: username.value, password: password.value })
    setToken(access_token)
    await navigateTo('/consultations')
  } catch {
    errorMessage.value = 'Invalid username or password.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <form class="form login-form" @submit.prevent="onSubmit">
      <h1>ClinicCare Login</h1>
      <label>
        Username
        <input v-model="username" type="text" autocomplete="username" required />
      </label>
      <label>
        Password
        <input v-model="password" type="password" autocomplete="current-password" required />
      </label>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      <button type="submit" class="btn" :disabled="loading">
        {{ loading ? 'Signing in…' : 'Sign in' }}
      </button>
    </form>
  </div>
</template>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
}

.login-form {
  background: white;
  padding: 2rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 360px;
}

.login-form h1 {
  font-size: 1.25rem;
  margin: 0 0 1.5rem;
  color: #0f766e;
}
</style>
