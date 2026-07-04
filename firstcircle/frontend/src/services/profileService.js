import { apiRequest } from './api'

/**
 * Profile Service - handles profile creation, updating, and free slots
 */
export const profileService = {
  async createProfile(userId, profileData) {
    try {
      const payload = {
        user_id: Number(userId),
        year: profileData.year,
        branch: profileData.branch,
        student_type: profileData.studentType || profileData.student_type,
        bio: profileData.bio || "",
        interests: profileData.interests || [],
        comfort_preferences: profileData.comfort || profileData.comfort_preferences || [],
        skills: profileData.skills || []
      }
      
      const response = await apiRequest('/profiles/', {
        method: 'POST',
        body: JSON.stringify(payload)
      })
      localStorage.setItem('currentProfileId', response.id)
      localStorage.setItem('profile', JSON.stringify(response))
      return response
    } catch (err) {
      console.error('Failed to create profile:', err)
      // Fallback: store in localStorage
      const mockProfile = {
        id: Date.now(),
        user_id: Number(userId),
        ...profileData
      }
      localStorage.setItem('currentProfileId', mockProfile.id)
      localStorage.setItem('profile', JSON.stringify(mockProfile))
      return mockProfile
    }
  },

  async updateProfile(userId, profileData) {
    try {
      const payload = {
        year: profileData.year,
        branch: profileData.branch,
        student_type: profileData.studentType || profileData.student_type,
        bio: profileData.bio,
        interests: profileData.interests,
        comfort_preferences: profileData.comfort || profileData.comfort_preferences,
        skills: profileData.skills
      }
      const response = await apiRequest(`/profiles/user/${userId}`, {
        method: 'PUT',
        body: JSON.stringify(payload)
      })
      localStorage.setItem('profile', JSON.stringify(response))
      return response
    } catch (err) {
      console.error('Failed to update profile:', err)
      // Fallback
      const stored = localStorage.getItem('profile')
      const updated = stored 
        ? { ...JSON.parse(stored), ...profileData }
        : { user_id: Number(userId), ...profileData }
      localStorage.setItem('profile', JSON.stringify(updated))
      return updated
    }
  },

  async saveFreeSlots(userId, slots) {
    try {
      // Save each free slot
      const savedSlots = await Promise.all(
        slots.map(slot =>
          apiRequest('/free-slots/', {
            method: 'POST',
            body: JSON.stringify({
              user_id: Number(userId),
              day_of_week: slot.day,
              start_time: slot.start,
              end_time: slot.end
            })
          })
        )
      )
      return savedSlots
    } catch (err) {
      console.error('Failed to save free slots:', err)
      // Fallback: store in localStorage
      const mockSlots = slots.map((s, idx) => ({
        id: 300 + idx,
        user_id: Number(userId),
        ...s
      }))
      localStorage.setItem('freeSlots', JSON.stringify(mockSlots))
      return mockSlots
    }
  },

  async getProfile(userId) {
    try {
      const response = await apiRequest(`/profiles/user/${userId}`)
      return response
    } catch (err) {
      console.error('Failed to get profile:', err)
      const stored = localStorage.getItem('profile')
      return stored ? JSON.parse(stored) : null
    }
  }
}
