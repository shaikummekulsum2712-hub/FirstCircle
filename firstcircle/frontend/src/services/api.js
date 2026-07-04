/**
 * Safe fetch wrapper that communicates with FastAPI.
 * Automatically falls back to localStorage/mock data if the server is unreachable.
 */
export async function apiRequest(path, options = {}) {
  const token = localStorage.getItem('token')
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(options.headers || {})
  }

  // Normalize path to prevent double /api
  const cleanPath = path.startsWith('/api') ? path.substring(4) : path
  const normalizedPath = cleanPath.startsWith('/') ? cleanPath : `/${cleanPath}`

  try {
    const response = await fetch(`/api${normalizedPath}`, {
      ...options,
      headers
    })
    
    if (!response.ok) {
      let errText = ''
      try {
        const json = await response.clone().json()
        errText = json.detail || json.message || ''
      } catch (e) {
        errText = await response.text()
      }
      throw new Error(errText || `API Request failed with status ${response.status}`)
    }
    
    return await response.json()
  } catch (error) {
    console.warn(`API call to ${path} failed. Error:`, error)
    throw error // Propagate to let service handle local fallbacks
  }
}
