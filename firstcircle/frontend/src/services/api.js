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

  try {
    const response = await fetch(`/api${path}`, {
      ...options,
      headers
    })
    
    if (!response.ok) {
      const errText = await response.text()
      throw new Error(errText || 'API Request failed')
    }
    
    return await response.json()
  } catch (error) {
    console.warn(`API call to ${path} failed. Running in standalone frontend fallback mode. Error:`, error)
    throw error // Propagate to let service handle local fallbacks
  }
}
