/* global document */
import React, { useReducer, useState } from 'react'
import { Field, Form as FinalForm } from 'react-final-form'
import { Select, Form, Spin, Divider, Icon, Modal, Button } from 'antd'
import { useTranslation } from 'react-i18next'
import * as yup from 'yup'
import FinalField from './final-field'
import InputLabel from './input-label'
import ORG_TYPES from './org-types.json'
import SearchItem from '../modules/editor/section7/location-items/search-item'
import api from './api'

const { Option } = Select
const { Item } = Form
const Aux = node => node.children

let intid

const OrganizationSelect = ({ name, fieldName = 'organisation', orgs, loading, disabled, dict }) => {
  const { t } = useTranslation()
  const [state, setState] = useReducer(
    (state, newState) => ({ ...state, ...newState }), // eslint-disable-line
    { options: [], loading: false, searchStr: '', showAddOrgModal: false }
  )
  const filterOptions = value => {
    clearTimeout(intid)
    if (value.length > 1) {
      setState({
        options: [],
        loading: true,
        searchStr: value
      })
      intid = setTimeout(() => {
        const options = orgs
          .filter(it => it.name.toLowerCase().indexOf(value.toLowerCase()) !== -1 || it.longName.toLowerCase().indexOf(value.toLowerCase()) !== -1)
          .map(({ id, name }) => ({ value: id, label: name })) // eslint-disable-line
        setState({
          options,
          loading: false
        })
      }, 300)
    }
  }
  const AddOrgBtn = () => (
    <div className="add-org-btn">
    <Divider style={{ margin: '4px 0' }} />
    <div role="button" tabIndex={-1} style={{ padding: '8px', cursor: 'pointer' }} onClick={() => setState({ showAddOrgModal: true })}>
      <Icon type="plus" /> {t('Add new organisation')}
    </div>
    </div>
  )
  return (
    <Aux>
    <Field
      name={`${name}.organisationName`}
      render={(nameProps) => (
        <FinalField
          name={`${name}.${fieldName}`}
          render={({input, validateStatus, meta}) => {
            const $options =
              orgs && orgs.length > 0
                ? ((!meta.active && state.searchStr.length === 0 && input.value !== '') ? [{ value: input.value, label: orgs.find(it => it.id === input.value).name }] : state.options)
                : [{ value: input.value, label: nameProps.input.value }]
            return (
              <Item validateStatus={validateStatus} label={<InputLabel tooltip={dict.tooltip}>{dict.label}</InputLabel>}>
              <Select
                {...input}
                onChange={(val) => { setState({ searchStr: '', options: [] }); input.onChange(val); nameProps.input.onChange($options.find(it => it.value === val).label); input.onBlur() }}
                disabled={disabled}
                showSearch
                loading={loading}
                onSearch={filterOptions}
                notFoundContent={state.loading ? <Spin size="small" /> : <div>{(state.searchStr.length === 0 ? <span>{t('Start typing...')}</span> : <span>{t('No results')}</span>)}<AddOrgBtn /></div>}
                filterOption={false}
              >
                {$options.map(option => <Option value={option.value} key={option.value}>{option.label}</Option>)}
              </Select>
              </Item>
            )
          }}
        />
      )}
    />
    <AddOrganizationModal
      visible={state.showAddOrgModal}
      onHide={() => setState({ showAddOrgModal: false })}
    />
    </Aux>
  )
}

let formRef

const handleSubmit = () => {
  if (formRef) {
    formRef.form.submit()
  }
}

const validation = yup.object().shape({
  name: yup.string().required(),
  longName: yup.string().required(),
  newOrganisationType: yup.mixed().required(),
  location: yup.object().required()
})

const AddOrganizationModal = ({ visible, onHide }) => {
  const { t } = useTranslation()
  const [loading, setLoading] = useState(false)
  const [validationErrors, setValidationErrors] = useState([])
  const handleAddOrg = () => {
    // onHide()
    handleSubmit()
  }
  const submit = (values) => {
    setLoading(true)
    // console.log(values)
    try {
      validation.validateSync(values, { abortEarly: false })
      setValidationErrors([])
      const { lat, lng } = values.location.coordinates
      const data = { ...values, lat, lng, iatiCountry: values.location.countryCode }
      delete data.location
      api.post('/organisation/', data)
        .then(() => {
          setLoading(false)
        })
        .catch((err) => {
          setLoading(false)
          const errors = []
          Object.keys(err.response.data).forEach(key => {
            errors.push({
              path: key,
              messages: err.response.data[key]
            })
          })
          setValidationErrors(errors)
          document.getElementsByClassName('ant-modal-wrap')[0].scroll({ top: 0, behavior: 'smooth' })
        })
    } catch (errors) {
      console.log(errors)
      setValidationErrors(errors.inner)
      setLoading(false)
    }
  }
  const getValidateStatus = (fieldName) => {
    const err = validationErrors.find(it => it.path === fieldName)
    const ret = {}
    if(err){
      ret.validateStatus = 'error'
      if(err.messages){
        ret.help = err.messages.map(msg => <div>{msg}</div>)
      }
    }
    return ret
  }
  return (
    <Modal
      title={t('Add New Organization')}
      visible={visible}
      onCancel={onHide}
      className="add-org-modal"
      footer={[
        <Button key="back" onClick={onHide}>
          {t('Cancel')}
        </Button>,
        <Button key="submit" type="primary" loading={loading} onClick={handleAddOrg}>
          {t('Add')}
        </Button>,
      ]}
    >
      <Form layout="vertical">
        <FinalForm
          subscription={{}}
          ref={(ref) => { formRef = ref }}
          initialValues={{ name: '' }}
          onSubmit={submit}
          render={() => (
            <div>
              <Item {...getValidateStatus('name')} label={<InputLabel>{t('Name')}</InputLabel>}>
                <FinalField name="name" />
              </Item>
              <Item {...getValidateStatus('longName')} label={<InputLabel>{t('Long name')}</InputLabel>}>
                <FinalField name="longName" control="textarea" autosize />
              </Item>
              <Item {...getValidateStatus('iatiOrgId')} label={<InputLabel optional>{t('IATI identifier')}</InputLabel>}>
                <FinalField name="iatiOrgId" />
              </Item>
              <Item {...getValidateStatus('newOrganisationType')} label={<InputLabel>{t('Organisation type')}</InputLabel>}>
                <FinalField
                  name="newOrganisationType"
                  control="select"
                  options={ORG_TYPES}
                  withEmptyOption
                />
              </Item>
              <Item label={<InputLabel optional>{t('Website')}</InputLabel>}>
                <FinalField name="website" placeholder="https://..." />
              </Item>
              <FinalField
                name="location"
                render={({ input }) => (
                  <SearchItem
                    {...getValidateStatus('location')}
                    {...input}
                  />
                )}
              />
              <Item label={<InputLabel optional>{t('Contact name')}</InputLabel>}>
                <FinalField name="contactPerson" />
              </Item>
              <Item label={<InputLabel optional>{t('Contact email')}</InputLabel>}>
                <FinalField name="contactEmail" />
              </Item>
              <Item label={<InputLabel optional>{t('Description')}</InputLabel>}>
                <FinalField name="description" control="textarea" autosize />
              </Item>
            </div>
          )}
        />
      </Form>
    </Modal>
  )
}

export default OrganizationSelect
