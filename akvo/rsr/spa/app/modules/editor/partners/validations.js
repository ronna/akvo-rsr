import * as yup from 'yup'

export const basic = yup.object().shape({
  name: yup.string().required().default(''),
  role: yup.number().required().default(1),
  secondaryReporter: yup.boolean(),
  iatiActivityID: yup.string(),
  fundingAmount: yup.mixed().when('role', {
    is: 1,
    then: yup.mixed().required()
  })
})

const array = yup.array().of(basic).min(1, 'At least one partner is required for your validation set')
const arrays = {
  basic: array,
  IATI: array,
  DGIS: array
}

export const getValidationSets = (validationSets, opts = {}) => {
  return [opts.arrays ? arrays.basic : basic]
}

export default arrays
