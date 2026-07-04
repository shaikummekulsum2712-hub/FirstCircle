import { apiRequest } from './api'

export const autoPlaceService = {
  async suggestDrop(userId, category, time) {
    try {
      const today = new Date()
      let preferredDay = today.toISOString().split('T')[0]
      if (time === 'tomorrow') {
        const tomorrow = new Date(today)
        tomorrow.setDate(tomorrow.getDate() + 1)
        preferredDay = tomorrow.toISOString().split('T')[0]
      }

      const response = await apiRequest('/auto-place/suggest', {
        method: 'POST',
        body: JSON.stringify({
          user_id: Number(userId),
          preferred_circle_type: category === 'anything' ? 'any' : category,
          preferred_day: preferredDay,
          preferred_start_time: '08:00',
          preferred_end_time: '22:00',
          preferred_vibes: []
        })
      })
      return response
    } catch (err) {
      console.error('Failed to get auto-place recommendation:', err)
      throw err
    }
  }
}
