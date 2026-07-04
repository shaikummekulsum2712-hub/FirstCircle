import { apiRequest } from './api'

export const feedbackService = {
  async submitFeedback(feedbackData) {
    try {
      const response = await apiRequest('/feedback/', {
        method: 'POST',
        body: JSON.stringify({
          circle_id: Number(feedbackData.circle_id || feedbackData.circleId),
          user_id: Number(feedbackData.user_id || feedbackData.userId),
          rating: Number(feedbackData.rating),
          vibe_match: Boolean(feedbackData.vibe_match || feedbackData.vibeMatch),
          felt_safe: Boolean(feedbackData.felt_safe || feedbackData.feltSafe),
          would_meet_again: Boolean(feedbackData.would_meet_again || feedbackData.wouldMeetAgain),
          comment: feedbackData.comment || ""
        })
      })
      return response
    } catch (err) {
      console.error('Failed to submit feedback:', err)
      throw err
    }
  },

  async submitReport(reportData) {
    try {
      const response = await apiRequest('/reports/', {
        method: 'POST',
        body: JSON.stringify({
          circle_id: Number(reportData.circleId || reportData.circle_id),
          reporter_user_id: Number(reportData.reporterUserId || reportData.reporter_user_id),
          reported_user_id: reportData.reportedUserId || reportData.reported_user_id ? Number(reportData.reportedUserId || reportData.reported_user_id) : null,
          reason: reportData.reason,
          details: reportData.details || ""
        })
      })
      return response
    } catch (err) {
      console.error('Failed to submit report:', err)
      throw err
    }
  }
}
