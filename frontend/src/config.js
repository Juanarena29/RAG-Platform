export const API_URL = import.meta.env.VITE_API_URL ?? ''
export const API_KEY = import.meta.env.VITE_API_KEY ?? ''

if (!API_URL) {
  console.warn('[config] VITE_API_URL is not set')
}

if (!API_KEY) {
  console.warn('[config] VITE_API_KEY is not set')
}
