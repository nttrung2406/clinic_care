export interface DiagnosisCode {
  code: string
  description: string
}

export interface Consultation {
  id: number
  patient_name: string
  notes: string
  diagnosis_codes: string[]
  created_at: string
}

export interface ConsultationCreatePayload {
  patient_name: string
  notes: string
  diagnosis_codes: string[]
}

export interface ConsultationSearchParams {
  patient?: string
  diagnosis_code?: string
}
