import { apiRequest } from './api'
import { FAKE_CURRENT_USER } from '../data/fakeUsers'

export const profileService = {
  async getProfile() {
    try {
      const data = await apiRequest('/profile/me')
      return data
    } catch (err) {
      // Local fallback
      const stored = localStorage.getItem('profile')
      return stored ? JSON.parse(stored) : FAKE_CURRENT_USER
    }
  },

  async updateProfile(profileData) {
    try {
      const data = await apiRequest('/profile/me', {
        method: 'PUT',
        body: JSON.stringify(profileData)
      })
      return data
    } catch (err) {
      localStorage.setItem('profile', JSON.stringify({ ...FAKE_CURRENT_USER, ...profileData }))
      return { ...FAKE_CURRENT_USER, ...profileData }
    }
  },

  async getSlots() {
    try {
      const data = await apiRequest('/profile/slots')
      return data
    } catch (err) {
      const stored = localStorage.getItem('profile')
      const profile = stored ? JSON.parse(stored) : FAKE_CURRENT_USER
      return profile.free_slots || []
    }
  },

  async saveSlots(slots) {
    try {
      const data = await apiRequest('/profile/slots', {
        method: 'POST',
        body: JSON.stringify(slots)
      })
      return data
    } catch (err) {
      const stored = localStorage.getItem('profile')
      const profile = stored ? JSON.parse(stored) : FAKE_CURRENT_USER
      const updated = { ...profile, free_slots: slots.map((s, idx) => ({ id: 200 + idx, ...s })) }
      localStorage.setItem('profile', JSON.stringify(updated))
      return updated.free_slots
    }
  }
}
