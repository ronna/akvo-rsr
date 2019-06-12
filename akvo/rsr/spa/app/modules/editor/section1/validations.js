import * as yup from 'yup'

const RSR = yup.object().shape({
  isPublic: yup.boolean().default(true),
  validations: yup.array().of(yup.number()).default([1, 2]),
  title: yup.string().default('').required(),
  subtitle: yup.string().default('').required(),
  iatiStatus: yup.string().required(),
  dateStartPlanned: yup.string().required(),
  dateEndPlanned: yup.string().required(),
  dateStartActual: yup.string(),
  dateEndActual: yup.string(),
  currency: yup.string().default('EUR'),
  language: yup.string().default('en'),
  currentImage: yup.string().nullable(), // .required(),
  currentImageCaption: yup.string(),
  currentImageCredit: yup.string(),
  defaultAidType: yup.string(),
})

const IATI_BASIC = RSR.clone().shape({
  iatiActivityId: yup.string().required()
})

const IATI = IATI_BASIC.clone().shape({
  hierarchy: yup.string(),
  defaultAidTypeVocabulary: yup.string(),
  // defaultAidType: yup.string(),
  defaultFlowType: yup.string(),
  defaultTiedStatus: yup.string(),
  collaborationType: yup.string(),
  defaultFinanceType: yup.string(),
})

const DGIS = RSR.clone().shape({
  dateStartActual: RSR.fields.dateStartActual.required(),
  dateEndActual: RSR.fields.dateEndActual.required(),
  defaultAidTypeVocabulary: yup.string(),
  defaultAidType: yup.string().required(),
  defaultFlowType: yup.string().required(),
  defaultTiedStatus: yup.string().required(),
})

const DFID = IATI.clone()

const defs = {
  1: RSR,
  2: IATI,
  3: DGIS,
  6: DFID,
  8: IATI_BASIC
}

export default defs
