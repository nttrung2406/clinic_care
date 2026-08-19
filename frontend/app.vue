<template>
  <div class="app-shell">
    <header class="app-header">
      <h1>ClinicCare Mini EMR</h1>
      <nav>
        <NuxtLink to="/consultations">Consultations</NuxtLink>
        <NuxtLink to="/consultations/new">New Consultation</NuxtLink>
        <NuxtLink to="/search">Search</NuxtLink>
      </nav>
    </header>
    <main class="app-main">
      <NuxtPage />
    </main>
  </div>
</template>

<style>
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
  color: #1f2937;
  background: #f8fafc;
}

.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 2rem;
  background: #0f766e;
  color: white;
}

.app-header h1 {
  font-size: 1.25rem;
  margin: 0;
}

.app-header nav {
  display: flex;
  gap: 1.25rem;
}

.app-header nav a {
  color: white;
  text-decoration: none;
  opacity: 0.85;
}

.app-header nav a.router-link-active {
  opacity: 1;
  font-weight: 600;
  text-decoration: underline;
}

.app-main {
  max-width: 960px;
  margin: 0 auto;
  padding: 2rem;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.btn {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: #0f766e;
  color: white;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  text-decoration: none;
  font-size: 0.95rem;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06);
}

.table th,
.table td {
  text-align: left;
  padding: 0.65rem 0.85rem;
  border-bottom: 1px solid #e5e7eb;
}

.table th {
  background: #f1f5f9;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: #475569;
}

.badge {
  display: inline-block;
  background: #e0f2fe;
  color: #075985;
  border-radius: 999px;
  padding: 0.1rem 0.55rem;
  font-size: 0.8rem;
  margin: 0 0.2rem 0.2rem 0;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 520px;
}

.form.inline {
  flex-direction: row;
  align-items: flex-end;
  flex-wrap: wrap;
  max-width: none;
  margin-bottom: 1.5rem;
}

.form label {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  font-size: 0.9rem;
  color: #334155;
}

.form input,
.form textarea {
  padding: 0.5rem 0.65rem;
  border: 1px solid #cbd5e1;
  border-radius: 0.375rem;
  font-size: 0.95rem;
  font-family: inherit;
}

.error {
  color: #b91c1c;
}

.hint {
  color: #64748b;
  font-size: 0.85rem;
  margin: 0.25rem 0;
}
</style>
