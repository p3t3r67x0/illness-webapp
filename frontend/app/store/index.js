export const state = () => ({
  symptoms: null,
  area: null
})

export const mutations = {
  updateSymptoms(state, symptoms) {
    state.symptoms = symptoms
  },
  updateArea(state, area) {
    state.area = area
  }
}
