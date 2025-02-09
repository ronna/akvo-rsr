import React from 'react'
import { Card, Collapse, Empty, Icon, Row, Col } from 'antd'
import { useTranslation } from 'react-i18next'
import moment from 'moment'
import { UpdatePeriod } from './UpdatePeriod'

const { Panel } = Collapse
const Aux = node => node.children

export const Indicator = ({
  role,
  project,
  result,
  targetsAt,
  indicator,
  editPeriod,
  defaultFirstKey,
  handleOnClickLockPeriod,
  results,
  setResults,
  setItems
}) => {
  const { t } = useTranslation()
  return indicator.periods.length === 0
    ? (
      <Row>
        <Col style={{ padding: 16 }}>
          <Card>
            <Empty description={t('This indicator has no periods')} />
          </Card>
        </Col>
      </Row>
    )
    : (
      <Aux>
        <Collapse accordion className="periods" bordered={false} defaultActiveKey={defaultFirstKey ? defaultFirstKey.period : null}>
          {indicator.periods.map(period => {
            const updates = period?.updates?.sort((a, b) => b.id - a.id)
            const baseline = { year: indicator.baselineYear, value: indicator.baselineValue }
            return (
              <Panel
                key={period.id}
                header={
                  <div style={{ display: 'flex' }}>
                    {moment(period.periodStart, 'DD/MM/YYYY').format('DD MMM YYYY')} - {moment(period.periodEnd, 'DD/MM/YYYY').format('DD MMM YYYY')}
                    <Icon
                      type={period.locked ? 'lock' : 'unlock'}
                      className={`iconbtn ${period.locked ? 'locked' : 'unlocked'}`}
                      onClick={(e) => handleOnClickLockPeriod(e, period, indicator.id, result.id)}
                    />
                  </div>
                }
              >
                <UpdatePeriod
                  {...{
                    role,
                    project,
                    period,
                    indicator,
                    updates,
                    baseline,
                    targetsAt,
                    editPeriod,
                    results,
                    setResults,
                    setItems
                  }}
                />
              </Panel>
            )
          })}
        </Collapse>
      </Aux>
    )
}
