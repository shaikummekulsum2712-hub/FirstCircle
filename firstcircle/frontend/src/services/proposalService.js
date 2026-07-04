import { apiRequest } from './api'

export const proposalService = {
  async getActiveProposals(userId) {
    try {
      const response = await apiRequest(`/proposals/user/${userId}`)
      return response
    } catch (err) {
      console.error('Failed to get active proposals:', err)
      throw err
    }
  },

  async getProposalDetails(proposalId) {
    try {
      const response = await apiRequest(`/proposals/${proposalId}`)
      return response
    } catch (err) {
      console.error('Failed to get proposal details:', err)
      throw err
    }
  },

  async acceptProposal(proposalId, userId) {
    try {
      const response = await apiRequest(`/proposals/${proposalId}/accept?user_id=${userId}`, {
        method: 'PATCH'
      })
      return response
    } catch (err) {
      console.error('Failed to accept proposal:', err)
      throw err
    }
  },

  async skipProposal(proposalId, userId) {
    try {
      const response = await apiRequest(`/proposals/${proposalId}/skip?user_id=${userId}`, {
        method: 'PATCH'
      })
      return response
    } catch (err) {
      console.error('Failed to skip proposal:', err)
      throw err
    }
  },

  async createProposalForDrop(dropId, requiredAcceptCount = 3) {
    try {
      const response = await apiRequest(`/proposals/drop/${dropId}?required_accept_count=${requiredAcceptCount}`, {
        method: 'POST'
      })
      return response
    } catch (err) {
      console.error('Failed to create proposal for drop:', err)
      throw err
    }
  }
}
