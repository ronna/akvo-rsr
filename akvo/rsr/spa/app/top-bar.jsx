import React, { useEffect } from 'react'
import { connect } from 'react-redux'
import { Link, Route } from 'react-router-dom'
import { Icon, Button, Dropdown, Menu } from 'antd'
import { useTranslation } from 'react-i18next'
import classNames from 'classnames'

const langs = ['en', 'es', 'fr']
const langDict = {
  en: 'ENG',
  es: 'ESP',
  fr: 'FRA'
}

const langMenu = ({ userRdr, dispatch }) => {
  const { i18n } = useTranslation()
  useEffect(() => {
    i18n.changeLanguage(userRdr.lang)
  }, [])
  const setLang = (lang) => {
    dispatch({ type: 'SET_LANG', lang })
    i18n.changeLanguage(lang)
  }
  return (
    <Menu className="lang-menu">
      {langs.filter(it => it !== userRdr.lang).map((lang, index) => (
        <Menu.Item key={index} onClick={() => setLang(lang)}>{langDict[lang]}</Menu.Item>
      ))}
    </Menu>
  )
}


const LinkItem = ({ to, children, basicLink}) => (
  <Route
    path={to}
    exact
    children={({ match }) => {
      if (!basicLink) return <Link className={classNames({ active: match })} to={to}>{children}</Link>
      return <a className={classNames({ active: match })} href={`/my-rsr${to}`}>{children}</a>
    }}
  />
)

const ProgramsMenuItem = ({ programs = [], canCreateProjects }) => {
  const { t } = useTranslation()
  if (programs && programs.length === 1 && !canCreateProjects){
    return <li><LinkItem to={`/programs/${programs[0].id}`}>{t('Program')}</LinkItem></li>
  }
  if ((programs && programs.length > 1) || (canCreateProjects)){
    const menu = (
    <Menu>
      {programs.map(program => <Menu.Item><LinkItem basicLink to={`/programs/${program.id}`}>{program.name || t('Untitled program')}</LinkItem></Menu.Item>)}
      <Menu.Divider />
      <Menu.Item><a href="/my-rsr/programs/new/editor"><Icon type="plus" /> {t('Create new program')}</a></Menu.Item>
    </Menu>
    )
    return (
      <Dropdown overlay={menu}>
        <li>
          <Route path={'/programs'} children={({ match }) => <a className={classNames({ active: match })}>{t('Programs')} <Icon type="caret-down" /></a>} />{/* eslint-disable-line */}
        </li>
      </Dropdown>
    )
  }
  return null
}

const TopBar = ({ userRdr, dispatch }) => {
  const { t } = useTranslation()
  const canCreateProjects = userRdr.organisations && userRdr.organisations.findIndex(it => it.canCreateProjects) !== -1
  return (
    <div className="top-bar">
      <div className="ui container">
        <a href={`/${userRdr.lang}/projects`}>
        <img className="logo" src="/logo" />
        </a>
        <ul>
          <ProgramsMenuItem programs={userRdr.programs} {...{ canCreateProjects }} />
          {userRdr.canManageUsers && <li><LinkItem to="/users">{t('Users')}</LinkItem></li>}
          <li><a href={`/${userRdr.lang}/myrsr/iati`}>IATI</a></li>
          <li><LinkItem to="/reports">{t('Reports')}</LinkItem></li>
        </ul>
        <div className="right-side">
          <Dropdown overlay={langMenu({userRdr, dispatch})} trigger={['click']}>
            <span className="lang">{langDict[userRdr.lang]}</span>
          </Dropdown>
          {userRdr.firstName &&
          <Dropdown
            trigger={['click']}
            overlay={
              <Menu>
                <Menu.Item key="0">
                  <a href="/en/myrsr/details/">{t('My details')}</a>
                </Menu.Item>
                <Menu.Item key="1">
                  <a href="/en/sign_out">{t('Sign out')}</a>
                </Menu.Item>
              </Menu>
            }
          >
            <span className="user ant-dropdown-link">
              {userRdr.firstName} {userRdr.lastName} <Icon type="caret-down" />
            </span>
          </Dropdown>
          }
          <Link to="/projects"><Button type="primary" ghost>{t('My projects')}</Button></Link>
        </div>
      </div>
    </div>
  )
}

export default connect(
  ({ userRdr }) => ({ userRdr })
)(TopBar)
