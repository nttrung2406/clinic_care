<script setup lang="ts">
import type { Consultation } from '~/types'

const { list } = useConsultationApi()

const patient = ref('')
const diagnosisCode = ref('')
const results = ref<Consultation[]>([])
const loading = ref(false)
const searched = ref(false)
const errorMessage = ref('')

async function onSearch() {
  errorMessage.value = ''
  loading.value = true
  searched.value = true
  try {
    results.value = await list({
      patient: patient.value.trim() || undefined,
      diagnosis_code: diagnosisCode.value.trim() || undefined,
    })
  } catch {
    errorMessage.value = 'Failed to search consultations.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section>
    <h2>Search Consultations</h2>
    <form class="form inline" @submit.prevent="onSearch">
      <label>
        Patient name
        <input v-model="patient" type="text" placeholder="e.g. Jane" />
      </label>
      <label>
        Diagnosis code
        <input v-model="diagnosisCode" type="text" placeholder="e.g. A00" />
      </label>
      <button type="submit" class="btn" :disabled="loading">Search</button>
    </form>

    <p v-if="loading">Searching…</p>
    <p v-else-if="errorMessage" class="error">{{ errorMessage }}</p>
    <table v-else-if="searched" class="table">
      <thead>
        <tr>
          <th>Patient</th>
          <th>Diagnosis Codes</th>
          <th>Notes</th>
          <th>Date</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="c in results" :key="c.id">
          <td>{{ c.patient_name }}</td>
          <td>
            <span v-for="code in c.diagnosis_codes" :key="code" class="badge">{{ code }}</span>
          </td>
          <td>{{ c.notes }}</td>
          <td>{{ new Date(c.created_at).toLocaleString() }}</td>
        </tr>
        <tr v-if="!results.length">
          <td colspan="4">No matching consultations.</td>
        </tr>
      </tbody>
    </table>
  </section>
</template>
