export const state = () => ({
  symptoms: '',
  area: ''
})

export const mutations = {
  updateSymptoms(state, symptoms) {
    state.symptoms = symptoms
  },
  updateArea(state, area) {
    state.area = area
  }
}
