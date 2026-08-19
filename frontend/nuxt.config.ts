// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  runtimeConfig: {
    public: {
      // base URL of the ClinicCare FastAPI backend
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8090',
    },
  },
})
