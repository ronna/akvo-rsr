/* global window */
import React, { useState, useEffect } from 'react'
import { Collapse, Empty, Icon, Spin } from 'antd'
import { sumBy } from 'lodash'
import { useTranslation } from 'react-i18next'
import Result from './result'
import StickyClass from './sticky-class'
import Filters from './filters'
import './styles.scss'

const ExpandIcon = ({ isActive }) => (
  <div className={`expander ${isActive ? 'isActive' : ''}`}>
    <Icon type="down" />
  </div>
)

const { Panel } = Collapse

const ProgramView = ({
  params,
  loading,
  results,
  sources,
  search,
  contributors,
  partners,
  periods,
  selected,
  nfilter,
  countryOpts,
  targetsAt,
  setSelected,
  setSearch,
  setNfilter,
  setResults,
  setSources
}) => {
  const [filtering, setFiltering] = useState(false)
  const [indicators, setIndicators] = useState({
    id: null,
    data: []
  })
  const { t } = useTranslation()
  const handleResultChange = (index) => {
    if (index != null) window.scroll({ top: 142 + index * 88, behavior: 'smooth' })
  }
  const handleOnSelect = (values, type) => {
    setFiltering(true)
    setSelected({
      ...selected,
      [type]: values
    })
  }
  const handleOnCloseTag = (value, type) => {
    setSelected({
      ...selected,
      [type]: selected[type]
        ?.filter((val) => val !== value?.toString())
    })
    setFiltering(true)
  }
  const handleOnClear = () => {
    setSearch(null)
    setSelected({
      countries: [],
      contributors: [],
      periods: [],
      partners: []
    })
    setFiltering(true)
  }
  const handleOnSearch = (value) => {
    setSearch(value)
    setFiltering(true)
  }
  const handleOnIndicators = (ids) => {
    return ids
      ?.map((i) => {
        return ({
          ...i,
          periods: i?.periods
            ?.filter((p) => {
              if (selected.periods.length) {
                const pl = selected.periods.map((px) => px.split('-'))
                const fp = pl.map((px) => px[0].trim())
                const lp = pl.map((px) => px[1].trim())
                return fp.includes(p.periodStart) && lp.includes(p.periodEnd)
              }
              return p
            })
            ?.map((p) => {
              const cts = (selected.countries.length && p?.countries?.length)
                ? p.countries?.filter((c) => selected.countries.includes(c.isoCode))
                : p?.countries
              return ({
                ...p,
                countries: cts,
                contributors: p
                  ?.contributors
                  ?.filter((pc) => {
                    const fp = selected?.partners
                      ?.map((sp) => {
                        const r = partners?.find((pt) => pt?.id === parseInt(sp, 10))
                        return r?.value
                      })
                    let pname = pc?.projectSubtitle?.match(/\((.*?)\)/)
                    pname = pname ? pname[1] : pc?.projectSubtitle
                    return selected?.contributors?.length
                      ? selected.contributors.includes(pc?.projectId?.toString())
                      : fp?.length ? fp.filter((it) => it?.includes(pname))?.length : pc
                  })
                  .map((pc) => ({
                    ...pc,
                    contributors: pc.contributors
                      ?.filter((fc) => {
                        return selected.countries.length
                          ? selected.countries?.includes(fc?.country?.isoCode)
                          : fc
                      })
                  }))
              })
            })
            ?.filter((p) => {
              const isCP = (selected.contributors.length || selected.partners.length)
              return (
                (isCP && selected.countries.length && p?.contributors?.length && p?.countries?.length) ||
                ((isCP && !selected.countries.length) && p?.contributors?.length) ||
                ((!isCP && selected.countries.length) && p?.countries?.length) ||
                (!isCP && !selected.countries.length && p)
              )
            })
        })
      })
      ?.filter((i) => i.periods.length)
      ?.filter((i) => search ? i.title.toLowerCase().includes(search?.toLowerCase()) : i)
  }

  useEffect(() => {
    if (filtering) {
      setIndicators({
        ...indicators,
        data: null
      })
      const nf = sumBy(Object.values(selected), (s) => s.length)
      setNfilter(nf)
      const ds = sources
        ?.filter((s) => {
          return s?.indicatorTitles
            ?.filter((it) => search ? it?.toLowerCase()?.includes(search?.toLowerCase()) : it)
            ?.length
        })
        ?.map((s) => ({
          ...s,
          indicators: s?.indicators?.length ? handleOnIndicators(s.indicators) : s?.indicators
        }))
        ?.filter((s) => ((s.fetch && s.indicators.length) || !s.fetch))
      setTimeout(() => {
        const fd = ds?.find((it) => it?.id === indicators?.id)
        setIndicators({
          ...indicators,
          data: fd?.indicators || []
        })
      }, 1500)
      setResults(ds)
      setFiltering(false)
    }
  }, [selected, filtering, search, sources])
  return (
    <>
      <Filters
        {...{
          contributors,
          partners,
          periods,
          selected,
          nfilter,
          loading: filtering,
          countries: countryOpts,
          onSelect: handleOnSelect,
          onClose: handleOnCloseTag,
          onClear: handleOnClear,
          onSearch: handleOnSearch
        }}
      />
      {loading && <div className="loading-container"><Spin indicator={<Icon type="loading" style={{ fontSize: 40 }} spin />} /></div>}
      {(!loading && !results?.length && (nfilter || search)) ? <div className="loading-container"><Empty /></div> : null}
      <Collapse defaultActiveKey="0" destroyInactivePanel onChange={handleResultChange} accordion bordered={false} expandIcon={({ isActive }) => <ExpandIcon isActive={isActive} />}>
        {results?.map((result, index) =>
          <Panel
            key={index}
            header={(
              <StickyClass offset={20}>
                <h1>{result.title}</h1>
                <div>
                  <i>{result.type}</i>
                  <span>
                    {t('nindicators', {
                      count: result?.indicators?.length ? result.indicators.length : result.indicatorCount
                    })}
                  </span>
                </div>
              </StickyClass>
            )}
          >
            <Result
              {...{
                programId: params?.projectId,
                countryFilter: selected.countries,
                onIndicators: handleOnIndicators,
                selected,
                result,
                results,
                sources,
                indicators,
                targetsAt,
                setResults,
                setSources,
                setIndicators
              }}
            />
          </Panel>
        )}
      </Collapse>
    </>
  )
}

export default ProgramView
