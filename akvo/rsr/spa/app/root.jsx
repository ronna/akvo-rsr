import React from 'react'
import SVGInline from 'react-svg-inline'
import { Icon, Button, Menu, Dropdown } from 'antd'
// import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'

import 'reset-css'
import 'antd/dist/antd.css'

import rsrSvg from './images/akvorsr.svg'
import Editor from './modules/editor/editor'

const menu = () => (
  <Menu>
    <Menu.Item key="0">
      <a href="http://www.alipay.com/">My details</a>
    </Menu.Item>
    <Menu.Item key="1">
      <a href="http://www.taobao.com/">Sign out</a>
    </Menu.Item>
  </Menu>
)

const Root = () => {
  return (
    <div id="root">
      <div className="top-bar">
        <div className="ui container">
          <SVGInline svg={rsrSvg} />
          <div className="right-side">
            <Dropdown overlay={menu} trigger={['click']}>
              <span className="user ant-dropdown-link">
                Anthony Gonzalez <Icon type="caret-down" />
              </span>
            </Dropdown>
            <Button type="primary" ghost>My Projects</Button>
          </div>
        </div>
      </div>
      <div className="ui container">
        <header>
          <Icon type="left" />
          <h1>Project name here</h1>
        </header>
        <Editor />
      </div>
    </div>
  )
}

export default Root
