import { apiRequest } from './api'

/**
 * User Service - handles user creation and management
 */
export const userService = {
  async createUser(email, name, rollNumber) {
    try {
      const response = await apiRequest('/users/', {
        method: 'POST',
        body: JSON.stringify({ email, name, roll_number: rollNumber })
      })
      // Store current user ID for reference
      localStorage.setItem('currentUserId', response.id)
      return response
    } catch (err) {
      console.error('Failed to create user:', err)
      // Fallback: generate mock user
      const mockId = Date.now()
      localStorage.setItem('currentUserId', mockId)
      return { id: mockId, email, name, roll_number: rollNumber }
    }
  },

  async getUserId() {
    // Get current user ID from localStorage or return null
    return localStorage.getItem('currentUserId')
  },

  async getCurrentUser() {
    try {
      const userId = localStorage.getItem('currentUserId')
      if (!userId) return null
      
      const response = await apiRequest(`/users/${userId}`)
      return response
    } catch (err) {
      console.error('Failed to get current user:', err)
      return null
    }
  }
}
