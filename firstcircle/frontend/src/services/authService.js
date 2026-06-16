import { apiRequest } from './api'
import { FAKE_CURRENT_USER } from '../data/fakeUsers'

export const authService = {
  async register(email, password) {
    try {
      const data = await apiRequest('/auth/register', {
        method: 'POST',
        body: JSON.stringify({ email, password })
      })
      return data
    } catch (err) {
      // Standalone Fallback
      localStorage.setItem('token', 'fallback-mock-jwt-token')
      return { token: 'fallback-mock-jwt-token', user: { id: 1, email } }
    }
  },

  async login(email, password) {
    try {
      const data = await apiRequest('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password })
      })
      localStorage.setItem('token', data.access_token)
      return data
    } catch (err) {
      // Standalone Fallback
      localStorage.setItem('token', 'fallback-mock-jwt-token')
      return { access_token: 'fallback-mock-jwt-token', token_type: 'bearer' }
    }
  },

  async getMe() {
    try {
      const user = await apiRequest('/auth/me')
      return user
    } catch (err) {
      return { id: 1, email: 'alice@example.com' }
    }
  }
}
