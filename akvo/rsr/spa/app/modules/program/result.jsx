import React, { useEffect, useState } from 'react'
import { Collapse, Icon, Spin } from 'antd'
import classNames from 'classnames'
import { useTranslation } from 'react-i18next'
import Indicator from './indicator'
import api from '../../utils/api'
import StickyClass from './sticky-class'

const { Panel } = Collapse
const ExpandIcon = ({ isActive }) => (
  <div className={classNames('expander', { isActive })}>
    <Icon type="down" />
  </div>
)
const Aux = node => node.children

const Result = ({
  selected,
  result,
  results,
  sources,
  programId,
  targetsAt,
  countryFilter,
  setResults,
  setSources,
  onIndicators
}) => {
  const { t } = useTranslation()
  const [loading, setLoading] = useState(true)
  const [indicators, setIndicators] = useState({
    id: null,
    data: []
  })
  const handleOnRequestIndicators = () => {
    api
      .get(`/project/${programId}/result/${result.id}/`)
      .then(({ data: { indicators: ids } }) => {
        setIndicators({
          id: result.id,
          data: ids
        })
      })
      .finally(() => {
        setLoading(false)
      })
  }
  useEffect(() => {
    if (!result?.indicators.length) {
      setLoading(true)
      handleOnRequestIndicators()
    }
  }, [])
  useEffect(() => {
    if (indicators?.id && (!result?.indicators?.length && indicators.id === result?.id)) {
      const ds = results
        ?.map((s) => s.id === result.id ? ({ ...s, indicators: onIndicators(indicators?.data), fetch: true }) : s)
        ?.filter((s) => ((s.indicators.length && s.fetch) || !s.fetch))
      setResults(ds)
      setSources(sources?.map((s) => s.id === result.id ? ({ ...s, indicators: indicators?.data, fetch: true }) : s))
    }
    if (indicators?.id && (indicators.id !== result?.id && !result?.indicators?.length) && !loading) {
      setLoading(true)
      handleOnRequestIndicators()
    }
  }, [result, results, sources, indicators, loading])
  return (
    <Aux>
      {(loading && !result?.fetch) ? <div className="loading-container"><Spin indicator={<Icon type="loading" style={{ fontSize: 32 }} spin />} /></div> : null}
      <Collapse defaultActiveKey={result?.indicators?.map((it) => it.id)} expandIcon={({ isActive }) => <ExpandIcon isActive={isActive} />}>
        {result?.indicators?.map((indicator) =>
          <Panel
            key={indicator.id}
            header={
              <StickyClass top={40}>
                <h3>{indicator.title}</h3>
                <div><span className="type">{indicator.type}</span> <span className="periods">{t('nperiods', { count: indicator.periodCount })}</span></div>
              </StickyClass>}
            destroyInactivePanel
          >
            <Indicator periods={indicator.periods} indicatorType={indicator.type} scoreOptions={indicator.scoreOptions} {...{ countryFilter, targetsAt, indicator, selected }} />
          </Panel>
        )}
      </Collapse>
    </Aux>
  )
}

export default Result
