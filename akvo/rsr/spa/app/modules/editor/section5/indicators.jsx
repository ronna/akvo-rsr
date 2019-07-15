import React from 'react'
import { connect } from 'react-redux'
import { Form, Button, Dropdown, Menu, Collapse, Divider, Col, Row, Radio, Popconfirm } from 'antd'
import { Field } from 'react-final-form'
import { FieldArray } from 'react-final-form-arrays'

import RTE from '../../../utils/rte'
import FinalField from '../../../utils/final-field'
import './styles.scss'
import InputLabel from '../../../utils/input-label'
import Accordion from '../../../utils/accordion'
import Condition from '../../../utils/condition'
import AutoSave from '../../../utils/auto-save'
import { addSetItem, removeSetItem } from '../actions'
import Periods from './periods/periods'
import Disaggregations from './disaggregations/disaggregations'
import IndicatorNavMenu, { fieldNameToId } from './indicator-nav-menu'

const { Item } = Form
const { Panel } = Collapse
const Aux = node => node.children


const indicatorTypes = [
  { value: 1, label: 'quantitative'},
  { value: 2, label: 'qualitative'}
]

const Indicators = connect(null, {addSetItem, removeSetItem})(({ fieldName, formPush, addSetItem, removeSetItem, resultId, primaryOrganisation }) => { // eslint-disable-line
  const add = (key) => {
    const newItem = { type: key, periods: [] }
    if(key === 1) newItem.disaggregations = []
    if(resultId) newItem.result = resultId
    formPush(`${fieldName}.indicators`, newItem)
    addSetItem(5, `${fieldName}.indicators`, newItem)
  }
  const remove = (index, fields) => {
    fields.remove(index)
    removeSetItem(5, `${fieldName}.indicators`, index)
  }
  return (
    <FieldArray name={`${fieldName}.indicators`} subscription={{}}>
    {({ fields }) => (
      <Aux>
        <Accordion
          multiple
          className="indicators-list"
          finalFormFields={fields}
          setName={`${fieldName}.indicators`}
          renderPanel={(name, index, activeKey) => (
            <Panel
              key={index}
              header={(
              <span>
                <Field
                  name={`${name}.type`}
                  render={({input}) => {
                    const type = indicatorTypes.find(it => it.value === input.value)
                    return <span><span className="capitalized">{type && type.label}</span>&nbsp;Indicator {index + 1}</span>
                  }}
                />
              </span>)}
              extra={(
                /* eslint-disable-next-line */
                <div onClick={(e) => { e.stopPropagation() }} style={{ display: 'flex' }}>
                <IndicatorNavMenu fieldName={name} isActive={activeKey.indexOf(String(index)) !== -1} />
                <div className="delete-btn-holder">
                <Popconfirm
                  title="Are you sure to delete this indicator?"
                  onConfirm={() => remove(index, fields)}
                  okText="Yes"
                  cancelText="No"
                >
                  <Button size="small" icon="delete" className="delete-panel" />
                </Popconfirm>
                </div>
                </div>
              )}
            >
              <AutoSave sectionIndex={5} setName={`${fieldName}.indicators`} itemIndex={index} />
              <div id={`${fieldNameToId(name)}-info`} />
              <Item label={<InputLabel optional>Title</InputLabel>}>
                <FinalField
                  name={`${name}.title`}
                  control="textarea"
                  autosize
                />
              </Item>
              <Condition when={`${name}.type`} is={1}>
                <Row gutter={16}>
                  <Col span={12}>
                    <Item label="Measure">
                      <FinalField
                        name={`${name}.measure`}
                        render={({input}) => (
                          <Radio.Group {...input}>
                            <Radio.Button value="1">Unit</Radio.Button>
                            <Radio.Button value="2">Percentage</Radio.Button>
                          </Radio.Group>
                        )}
                      />
                    </Item>
                  </Col>
                  <Col span={12}>
                    <Item label={<InputLabel>Order</InputLabel>}>
                      <FinalField
                        name={`${name}.ascending`}
                        render={({input}) => (
                          <Radio.Group {...input}>
                            <Radio.Button value>Ascending</Radio.Button>
                            <Radio.Button value={false}>Descending</Radio.Button>
                          </Radio.Group>
                        )}
                      />
                    </Item>
                  </Col>
                </Row>
              </Condition>
              <Item label={<InputLabel optional>Description</InputLabel>}>
                <FinalField name={`${name}.description`} render={({input}) => <RTE {...input} />} />
              </Item>
              <Divider />
              <div id={`${fieldNameToId(name)}-disaggregations`} />
              <Condition when={`${name}.type`} is={1}>
                <Aux>
                  <Field name={`${name}.id`} render={({ input: {value} }) => <Disaggregations formPush={formPush} fieldName={name} indicatorId={value} />} />
                  {/* <Disaggregations formPush={formPush} fieldName={name} /> */}
                  <Divider />
                </Aux>
              </Condition>
              <div id={`${fieldNameToId(name)}-baseline`} />
              <Row gutter={15}>
                <Col span={12}>
                  <Item label={<InputLabel optional>Baseline year</InputLabel>}>
                    <FinalField name={`${name}.baselineYear`} />
                  </Item>
                </Col>
                <Col span={12}>
                  <Item label={<InputLabel optional>Baseline value</InputLabel>}>
                  <FinalField name={`${name}.baselineValue`} />
                  </Item>
                </Col>
              </Row>
              <Item label={<InputLabel optional>Baseline comment</InputLabel>}>
                <FinalField name={`${name}.baselineComment`} render={({input}) => <RTE {...input} />} />
              </Item>
              <Divider />
              <div id={`${fieldNameToId(name)}-periods`} />
              <FinalField name={`${name}.id`} render={({ input }) => <Periods formPush={formPush} fieldName={name} indicatorId={input.value} primaryOrganisation={primaryOrganisation} />} />
            </Panel>
          )}
        />
        <Dropdown
          overlay={(
            <Menu style={{ textAlign: 'center' }} onClick={(e) => add(Number(e.key))}>
              <Menu.Item key={1}>
                Quantitative
              </Menu.Item>
              <Menu.Item key={2}>
                Qualitative
              </Menu.Item>
            </Menu>
          )}
          trigger={['click']}
        >
          <Button icon="plus" block type="dashed">Add indicator</Button>
        </Dropdown>
      </Aux>
    )}
    </FieldArray>
  )
})

export default Indicators
