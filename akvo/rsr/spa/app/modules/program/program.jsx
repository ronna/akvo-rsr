/* global document */
import React, { useState, useEffect } from 'react'
import { connect } from 'react-redux'
import { Tabs } from 'antd'
import classNames from 'classnames'
import { Route, Link, Redirect } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { uniq } from 'lodash'
import moment from 'moment'
import Hierarchy from '../hierarchy/hierarchy'
import Editor from '../editor/editor'
import api from '../../utils/api'
import Reports from '../reports/reports'
import * as actions from '../editor/actions'
import ProgramView from './program-view'

const { TabPane } = Tabs


const Program = ({ match: { params }, userRdr, ...props }) => {
  const { t } = useTranslation()
  const [results, setResults] = useState([])
  const [title, setTitle] = useState('')
  const [loading, setLoading] = useState(true)
  const [sources, setSources] = useState(null)
  const [countryOpts, setCountryOpts] = useState([])
  const [targetsAt, setTargetsAt] = useState(null)
  const [contributors, setContributors] = useState([])
  const [periods, setPeriods] = useState([])
  const [partners, setPartners] = useState([])
  const [nfilter, setNfilter] = useState(0)
  const [search, setSearch] = useState(null)
  const [selected, setSelected] = useState({
    countries: [],
    contributors: [],
    periods: [],
    partners: []
  })

  const handleOnUnique = (data, field) => {
    const ds = data
      ?.map((d) => (
        Object.keys(d[field]).map((r) => ({
          id: parseInt(r, 10),
          value: d[field][r]
        }))
      ))
      ?.flatMap((d) => d)
    return uniq(data.flatMap((r) => Object.keys(r[field])))
      ?.map((k) => ds.find((d) => d.id === parseInt(k, 10)))
      ?.sort((a, b) => a?.value?.localeCompare(b?.value))
  }
  const initiate = () => {
    setLoading(true)
    if (params.projectId !== 'new') {
      api.get(`/project/${params.projectId}/results`)
        .then(({ data }) => {
          const ds = data.results.map(it => ({ ...it, indicators: [], fetch: false }))
          setResults(ds)
          setSources(ds)
          setTitle(data.title)
          props.setProjectTitle(data.title)
          document.title = `${data.title} | Akvo RSR`
          setTargetsAt(data.targetsAt)
          // collect country opts
          const opts = []
          data.results.forEach(result => {
            result.countries.forEach(opt => { if (opts.indexOf(opt) === -1) opts.push(opt) })
          })
          setCountryOpts(opts?.sort())
          setContributors(handleOnUnique(data.results, 'contributors'))
          setPartners(handleOnUnique(data.results, 'partners'))
          const pds = uniq(data.results
            ?.flatMap((r) => r.periods)
            ?.map((p) => `${moment(p[0], 'YYYY-MM-DD').format('DD/MM/YYYY')} - ${moment(p[1], 'YYYY-MM-DD').format('DD/MM/YYYY')}`))
            ?.sort((a, b) => {
              const xb = b.split(' - ')
              const xa = a.split(' - ')
              return moment(xb[1], 'DD/MM/YYYY').format('YYYY') - moment(xa[1], 'DD/MM/YYYY').format('YYYY')
            })
          setPeriods(pds)
          setLoading(false)
        })
    } else {
      setLoading(false)
    }
  }
  useEffect(initiate, [])
  const canEdit = userRdr.programs && userRdr.programs.find(program => program.id === parseInt(params.projectId, 10))?.canEditProgram
  const _title = (!props?.title && title) ? title : props?.title ? props.title : t('Untitled program')
  return (
    <div className="program-view">
      <Route path="/programs/:id/:view?" render={({ match }) => {
        const view = match.params.view ? match.params.view : ''
        return [
          <header className={classNames('main-header', { editor: match.params.view === 'editor' })}>
            <h1>{!loading && _title}</h1>
          </header>,
          <Tabs size="large" activeKey={view}>
            {((results?.length || (!results?.length && (nfilter || search))) || !match.params.view) && <TabPane tab={<Link to={`/programs/${params.projectId}`}>Overview</Link>} key="" />}
            {canEdit && <TabPane tab={<Link to={`/programs/${params.projectId}/editor`}>Editor</Link>} key="editor" />}
            <TabPane tab={<Link to={`/programs/${params.projectId}/hierarchy`}>Hierarchy</Link>} key="hierarchy" />
            <TabPane tab={<Link to={`/programs/${params.projectId}/reports`}>Reports</Link>} key="reports" />
          </Tabs>
        ]
      }} />
      <Route path="/programs/:projectId" exact>
        {(!loading && !results?.length && !search && !nfilter) ? setTimeout(() => <Redirect to={`/programs/${params.projectId}/editor`} />, 1500) : null}
        <ProgramView
          {...{
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
          }}
        />
      </Route>
      <Route path="/programs/:programId/hierarchy/:projectId?" render={(_props) =>
        <Hierarchy {..._props} canEdit={canEdit} program />
      } />
      <Route path="/programs/:projectId/reports" render={() =>
        <Reports programId={params.projectId} />
      } />
      <Route path="/programs/:id/editor" render={({ match: { params } }) =>
        <Editor {...{ params }} program />
      } />
      <div id="bar-tooltip" />
      <div id="disagg-bar-tooltip" />
    </div>
  )
}

export default connect(
  ({ editorRdr: { section1: { fields: { title } } }, userRdr }) => ({ title, userRdr }), actions
)(Program)
