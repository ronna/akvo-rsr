import types from './action-types'
import { basic } from './validations'
import { yupModel } from '../../../utils/validation-utils'

const newPartner = yupModel(basic)

const initialState = [{...newPartner}]

export default (state = initialState, action) => {
  switch(action.type){
    case types.ADD:
      return [...state, {...newPartner}]
    case types.REMOVE:
      return [...state.slice(0, action.index), ...state.slice(action.index + 1)]
    case types.EDIT_FIELD:
      const field = {}
      field[action.key] = action.value
      const updated = Object.assign({}, state[action.index], field)
      return [...state.slice(0, action.index), updated, ...state.slice(action.index + 1)]
    default: return state
  }
}
