import { apiRequest } from './api'

export const circleService = {
  async getUserCircles(userId) {
    try {
      const response = await apiRequest(`/circles/user/${userId}`)
      return response
    } catch (err) {
      console.error('Failed to get user circles:', err)
      throw err
    }
  },

  async getCircleDetails(circleId) {
    try {
      const response = await apiRequest(`/circles/${circleId}`)
      return response
    } catch (err) {
      console.error('Failed to get circle details:', err)
      throw err
    }
  },

  async createCircleFromProposal(proposalId, circleData) {
    try {
      const response = await apiRequest(`/circles/from-proposal/${proposalId}`, {
        method: 'POST',
        body: JSON.stringify({
          proposal_id: Number(proposalId),
          meeting_place: circleData.meeting_place || circleData.meetingPlace || "Library Cafe",
          meeting_date: circleData.meeting_date || circleData.meetingDate || new Date().toISOString().split('T')[0],
          start_time: circleData.start_time || circleData.startTime || "18:00",
          end_time: circleData.end_time || circleData.endTime || "20:00"
        })
      })
      return response
    } catch (err) {
      console.error('Failed to create circle from proposal:', err)
      throw err
    }
  },

  async getCircleMembers(dropId) {
    try {
      const members = await apiRequest(`/drop-members/drop/${dropId}`)
      const hydratedMembers = await Promise.all(
        members.map(async (m) => {
          try {
            const user = await apiRequest(`/users/${m.user_id}`)
            const profile = await apiRequest(`/profiles/user/${m.user_id}`)
            return {
              id: m.user_id,
              name: user.name,
              email: user.email,
              rollNumber: user.roll_number,
              year: profile.year,
              branch: profile.branch,
              studentType: profile.student_type,
              bio: profile.bio,
              interests: profile.interests,
              comfort: profile.comfort_preferences || []
            }
          } catch (e) {
            console.error(`Failed to hydrate member user ${m.user_id}:`, e)
            return null
          }
        })
      )
      return hydratedMembers.filter(Boolean)
    } catch (err) {
      console.error('Failed to get circle members:', err)
      return []
    }
  }
}
