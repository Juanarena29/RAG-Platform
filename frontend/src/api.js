import { API_KEY, API_URL } from './config.js'

async function parseError(response) {
  const body = await response.json().catch(() => ({}))
  const { detail } = body

  if (typeof detail === 'string') {
    return detail
  }

  if (Array.isArray(detail)) {
    return detail.map((entry) => entry.msg ?? JSON.stringify(entry)).join(', ')
  }

  return response.statusText || 'Request failed'
}

async function authFetch(path, options = {}) {
  const headers = {
    ...options.headers,
    Authorization: `Bearer ${API_KEY}`,
  }

  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers,
  })

  if (!response.ok) {
    throw new Error(await parseError(response))
  }

  return response
}

export async function checkHealth() {
  const response = await fetch(`${API_URL}/health`)

  if (!response.ok) {
    throw new Error(await parseError(response))
  }

  return response.json()
}

export async function getDocuments() {
  const response = await authFetch('/documents')
  return response.json()
}

export async function uploadDocument(file) {
  const formData = new FormData()
  formData.append('file', file)

  const response = await authFetch('/documents/upload', {
    method: 'POST',
    body: formData,
  })

  return response.json()
}

export async function queryRAG(question, options = {}) {
  const { maxSources = 5, useHyde = true } = options

  const response = await authFetch('/query', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      question,
      max_sources: maxSources,
      use_hyde: useHyde,
    }),
  })

  return response.json()
}

export async function submitFeedback(traceId, value, comment) {
  const response = await authFetch('/feedback', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      trace_id: traceId,
      value,
      ...(comment ? { comment } : {}),
    }),
  })

  return response.json()
}
