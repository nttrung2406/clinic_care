<script setup lang="ts">
import type { DiagnosisCode } from '~/types'

const props = defineProps<{ modelValue: string[] }>()
const emit = defineEmits<{ (e: 'update:modelValue', value: string[]): void }>()

const { search } = useDiagnosisApi()

const query = ref('')
const results = ref<DiagnosisCode[]>([])
const loading = ref(false)
let debounceTimer: ReturnType<typeof setTimeout> | undefined

watch(query, (value) => {
  if (debounceTimer) clearTimeout(debounceTimer)
  const term = value.trim()
  if (!term) {
    results.value = []
    return
  }
  debounceTimer = setTimeout(async () => {
    loading.value = true
    try {
      results.value = await search(term)
    } catch {
      results.value = []
    } finally {
      loading.value = false
    }
  }, 250)
})

function addCode(code: DiagnosisCode) {
  if (!props.modelValue.includes(code.code)) {
    emit('update:modelValue', [...props.modelValue, code.code])
  }
  query.value = ''
  results.value = []
}

function removeCode(code: string) {
  emit(
    'update:modelValue',
    props.modelValue.filter((c) => c !== code),
  )
}
</script>

<template>
  <div class="diagnosis-picker">
    <div v-if="modelValue.length" class="chips">
      <span v-for="code in modelValue" :key="code" class="badge">
        {{ code }}
        <button type="button" class="chip-remove" @click="removeCode(code)">×</button>
      </span>
    </div>
    <input v-model="query" type="text" placeholder="Search ICD-10 code or description…" />
    <p v-if="loading" class="hint">Searching…</p>
    <ul v-if="results.length" class="picker-results">
      <li v-for="item in results" :key="item.code" @click="addCode(item)">
        <strong>{{ item.code }}</strong> — {{ item.description }}
      </li>
    </ul>
  </div>
</template>

<style scoped>
.diagnosis-picker {
  position: relative;
}

.chips {
  margin-bottom: 0.4rem;
}

.chip-remove {
  border: none;
  background: none;
  color: inherit;
  cursor: pointer;
  margin-left: 0.25rem;
  font-size: 0.9rem;
  line-height: 1;
}

.picker-results {
  position: absolute;
  z-index: 10;
  list-style: none;
  margin: 0.25rem 0 0;
  padding: 0.25rem 0;
  background: white;
  border: 1px solid #cbd5e1;
  border-radius: 0.375rem;
  width: 100%;
  max-height: 220px;
  overflow-y: auto;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
}

.picker-results li {
  padding: 0.4rem 0.65rem;
  cursor: pointer;
  font-size: 0.9rem;
}

.picker-results li:hover {
  background: #f1f5f9;
}
</style>
