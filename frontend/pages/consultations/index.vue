<script setup lang="ts">
import type { Consultation } from '~/types'

const { list } = useConsultationApi()
const {
  data: consultations,
  pending,
  error,
} = await useAsyncData<Consultation[]>('consultations', () => list())
</script>

<template>
  <section>
    <div class="page-header">
      <h2>Consultations</h2>
      <NuxtLink to="/consultations/new" class="btn">+ New consultation</NuxtLink>
    </div>

    <p v-if="pending">Loading…</p>
    <p v-else-if="error" class="error">Failed to load consultations.</p>
    <table v-else class="table">
      <thead>
        <tr>
          <th>Patient</th>
          <th>Diagnosis Codes</th>
          <th>Notes</th>
          <th>Date</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="c in consultations" :key="c.id">
          <td>{{ c.patient_name }}</td>
          <td>
            <span v-for="code in c.diagnosis_codes" :key="code" class="badge">{{ code }}</span>
          </td>
          <td>{{ c.notes }}</td>
          <td>{{ new Date(c.created_at).toLocaleString() }}</td>
        </tr>
        <tr v-if="!consultations?.length">
          <td colspan="4">No consultations yet.</td>
        </tr>
      </tbody>
    </table>
  </section>
</template>
