<script setup lang="ts">
const router = useRouter()
const { create } = useConsultationApi()

const patientName = ref('')
const notes = ref('')
const diagnosisCodes = ref<string[]>([])
const submitting = ref(false)
const errorMessage = ref('')

async function onSubmit() {
  errorMessage.value = ''

  if (!patientName.value.trim() || !notes.value.trim() || diagnosisCodes.value.length === 0) {
    errorMessage.value = 'Patient name, notes, and at least one diagnosis code are required.'
    return
  }

  submitting.value = true
  try {
    await create({
      patient_name: patientName.value.trim(),
      notes: notes.value.trim(),
      diagnosis_codes: diagnosisCodes.value,
    })
    await router.push('/consultations')
  } catch (err: any) {
    errorMessage.value = err?.data?.detail ?? 'Failed to save consultation.'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <section>
    <h2>New Consultation</h2>
    <form class="form" @submit.prevent="onSubmit">
      <label>
        Patient name
        <input v-model="patientName" type="text" required />
      </label>

      <div class="field">
        <span>Diagnosis codes</span>
        <DiagnosisCodePicker v-model="diagnosisCodes" />
      </div>

      <label>
        Notes
        <textarea v-model="notes" rows="5" required />
      </label>

      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

      <button type="submit" class="btn" :disabled="submitting">
        {{ submitting ? 'Saving…' : 'Save consultation' }}
      </button>
    </form>
  </section>
</template>
