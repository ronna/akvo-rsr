/* global window */
import React, { useEffect, useState, useRef } from 'react'
import classNames from 'classnames'
import { Icon, Spin } from 'antd'
import { CSSTransition, TransitionGroup } from 'react-transition-group'
import { useTranslation } from 'react-i18next'
import InfiniteScroll from 'react-infinite-scroll-component'
import { useLocalStorage } from '@rehooks/local-storage'
import lookup from 'country-code-lookup'
import logoPng from '../../images/logo3.png'

const pageSize = 20
// let allowShowMore = true
const isLocal = window.location.href.indexOf('localhost') !== -1 || window.location.href.indexOf('localakvoapp') !== -1
const urlPrefix = isLocal ? 'http://rsr.akvo.org' : ''
const isRSR = window.location.host.split('.')[0] === 'rsr'

const Projects = ({ projects = [], loading, show, setShow, ulRef, showSortLabel = true }) => {
  const { t } = useTranslation()
  const [lang] = useLocalStorage('lang', 'en')
  const [visibleProjects, setVisibleProjects] = useState([])
  const [hasMore, setHasMore] = useState(false)
  const [projectsLength, setProjectsLength] = useState(pageSize)
  const page = useRef(0)
  const ignoreScroll = useRef(false)
  useEffect(() => {
    setVisibleProjects(projects.slice(0, pageSize))
    setHasMore(projects.length > pageSize)
    ulRef.current.scroll({top: 0})
    page.current = 0
  }, [projects])
  const showMore = () => {
    if (ignoreScroll.current === false){
      page.current += 1
      ignoreScroll.current = true
      const updatedVisible = [...visibleProjects, ...projects.slice(page.current * pageSize, page.current * pageSize + pageSize)]
      setVisibleProjects(updatedVisible)
      setProjectsLength(updatedVisible.length)
      setHasMore(projects.length > page.current * pageSize + pageSize)
      setTimeout(() => { ignoreScroll.current = false }, 1000)
    } else {
      if(visibleProjects.length < projects.length){
        setProjectsLength(visibleProjects.length + 1)
      }
    }
  }
  return [
    <div className={classNames('projects', { on: show })}>
      <div className="expander" role="button" tabIndex={-1} onClick={() => setShow(!show)}>
        <Icon type="caret-right" />
      </div>
      {loading && <div className="loading-container"><Spin indicator={<Icon type="loading" style={{ fontSize: 36 }} spin />} /></div>}
      <ul ref={ulRef} id="ul-scrollview">
        <InfiniteScroll
          dataLength={projectsLength}
          next={showMore}
          hasMore={hasMore}
          scrollableTarget="ul-scrollview"
          scrollThreshold="100px"
        >
          {showSortLabel && <div className="sort-label">{isRSR ? t('Most active projects in RSR') : t('Most active projects')}</div>}
        {projects.length > 0 &&
        <TransitionGroup component={null}>
        {visibleProjects.map((project) =>
          <CSSTransition
            key={project.id}
            timeout={500}
            classNames="project"
          >
          <li>
            <a href={`/dir${project.url}`} target="_blank" rel="noopener noreferrer">
              <div className="img">
                <img src={`${project.image}`} />
              </div>
            <h3>{project.title}</h3>
            <div className="locations">
              {project.countries.map(it => {
                const found = lookup.byIso(it)
                if(found) return t(found.country)
                return it
              }).join(', ')}
            </div>
            </a>
          </li>
          </CSSTransition>
        )}
        </TransitionGroup>
        }
        </InfiniteScroll>
      </ul>
      <footer>
        <a href="//akvo.org"><img src={logoPng} /></a>
        <ul>
          <li><a href="http://akvo.org/products/rsr/">{t('About')}</a></li>
          <li><a href="http://akvo.org/help/akvo-policies-and-terms-2/akvo-rsr-terms-of-use/">{t('Terms')}</a></li>
          <li><a href="https://github.com/akvo/akvo-rsr/wiki/RSR_Partner-API">API</a></li>
          <li><a href="http://rsrsupport.akvo.org/">{t('Support')}</a></li>
          <li><a href="https://github.com/akvo/akvo-rsr">{t('Source')} &nbsp;<Icon type="github" /></a></li>
        </ul>
      </footer>
    </div>,
    <div className={classNames('projects-placeholder', {on: show})} />
  ]
}

export default Projects
