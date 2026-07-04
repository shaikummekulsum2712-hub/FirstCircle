import { apiRequest } from './api'

export const dropService = {
  async getDrops() {
    try {
      const response = await apiRequest('/drops/')
      return response
    } catch (err) {
      console.error('Failed to get drops:', err)
      throw err
    }
  },

  async createDrop(creatorUserId, dropData) {
    try {
      // 1. Resolve location ID by looking up locations
      const locations = await apiRequest('/locations/')
      let location = locations.find(l => l.name.toLowerCase() === dropData.place.toLowerCase())
      
      if (!location) {
        // If the location does not exist in the DB, seed it automatically
        location = await apiRequest('/locations/', {
          method: 'POST',
          body: JSON.stringify({
            name: dropData.place,
            location_type: 'campus',
            is_safe: true,
            allowed_circle_types: 'friend,study,build,random'
          })
        })
      }

      // 2. Format Date (Today, Tomorrow, Saturday, etc. -> YYYY-MM-DD)
      let scheduledDate = dropData.date
      const today = new Date()
      if (dropData.date === 'Today') {
        scheduledDate = today.toISOString().split('T')[0]
      } else if (dropData.date === 'Tomorrow') {
        const tomorrow = new Date(today)
        tomorrow.setDate(tomorrow.getDate() + 1)
        scheduledDate = tomorrow.toISOString().split('T')[0]
      } else if (dropData.date === 'Saturday') {
        const sat = new Date(today)
        sat.setDate(sat.getDate() + ((6 - sat.getDay() + 7) % 7))
        scheduledDate = sat.toISOString().split('T')[0]
      } else if (dropData.date === 'This Week') {
        scheduledDate = today.toISOString().split('T')[0]
      } else if (!/^\d{4}-\d{2}-\d{2}$/.test(dropData.date)) {
        scheduledDate = today.toISOString().split('T')[0]
      }

      // 3. Format Time (e.g. "4:00 PM" -> "16:00")
      const formatTime = (timeStr) => {
        if (!timeStr) return "18:00"
        const match = timeStr.match(/(\d+):(\d+)\s*(AM|PM)?/i)
        if (!match) return "18:00"
        let hours = parseInt(match[1])
        const minutes = match[2].padStart(2, '0')
        const ampm = match[3]
        if (ampm) {
          if (ampm.toUpperCase() === 'PM' && hours < 12) hours += 12
          if (ampm.toUpperCase() === 'AM' && hours === 12) hours = 0
        }
        return `${String(hours).padStart(2, '0')}:${minutes}`
      }

      const startTime = formatTime(dropData.time)
      // End time defaults to start time + 2 hours
      const endTime = (() => {
        const [h, m] = startTime.split(':').map(Number)
        return `${String((h + 2) % 24).padStart(2, '0')}:${String(m).padStart(2, '0')}`
      })()

      // 4. Calculate expires_at (6 hours from now)
      const expiresAt = new Date(Date.now() + 6 * 3600 * 1000).toISOString()

      const payload = {
        creator_user_id: Number(creatorUserId),
        title: dropData.title,
        description: dropData.description || "",
        circle_type: dropData.type || "friend",
        location_id: location.id,
        scheduled_date: scheduledDate,
        start_time: startTime,
        end_time: endTime,
        max_members: Number(dropData.groupSize || 4),
        urgency_level: 'medium',
        vibe_tags: dropData.vibe || [],
        expires_at: expiresAt
      }

      const response = await apiRequest('/drops/', {
        method: 'POST',
        body: JSON.stringify(payload)
      })
      return response
    } catch (err) {
      console.error('Failed to create drop:', err)
      throw err
    }
  },

  async getDrop(dropId) {
    try {
      const response = await apiRequest(`/drops/${dropId}`)
      return response
    } catch (err) {
      console.error('Failed to get drop:', err)
      throw err
    }
  },

  async joinDrop(dropId, userId) {
    try {
      const response = await apiRequest('/drop-members/join', {
        method: 'POST',
        body: JSON.stringify({
          drop_id: Number(dropId),
          user_id: Number(userId)
        })
      })
      return response
    } catch (err) {
      console.error('Failed to join drop:', err)
      throw err
    }
  }
}
