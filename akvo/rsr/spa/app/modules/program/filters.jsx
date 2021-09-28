import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import {
  Button,
  Col,
  Dropdown,
  Icon,
  Input,
  Popover,
  Row,
  Tag,
  Menu,
  Badge
} from 'antd'
import classNames from 'classnames'
import countriesDict from '../../utils/countries-dict'

const Item = ({ type, item }) => {
  switch (type) {
    case 'countries':
      return countriesDict[item]
    case 'contributors':
    case 'partners':
      return item?.value
    default:
      return item
  }
}

const DropdownItems = ({ onSelect, type, selected, items = [] }) => (
  <Menu
    multiple
    style={{
      width: 300,
      height: 200,
      overflowY: 'scroll',
      borderWidth: 1,
      borderStyle: 'solid',
      borderColor: '#eee'
    }}
    onSelect={({ selectedKeys }) => onSelect(selectedKeys, type)}
    onDeselect={({ selectedKeys }) => onSelect(selectedKeys, type)}
    selectedKeys={selected[type]}
  >
    {items?.map(item => (
      <Menu.Item key={['contributors', 'partners'].includes(type) ? item?.id : item}>
        <Item {...{ type, item }} />
      </Menu.Item>
    ))}
  </Menu>
)

const BadgeCircle = (props) => <Badge {...props} style={{ backgroundColor: '#fff', color: '#999', boxShadow: '0 0 0 1px #d9d9d9 inset' }} />

const DropdownFilter = ({ count, label = '', ...props }) => (
  <Dropdown overlay={<DropdownItems {...props} />} trigger={['click']}>
    <Button size="large" block>
      <span style={{ float: 'left' }}>
        {label}&nbsp;
        {count ? <BadgeCircle count={count} /> : ''}
      </span>
      <Icon type="down" style={{ float: 'right', paddingTop: 5 }} />
      <div style={{ clear: 'both' }} />
    </Button>
  </Dropdown>
)

const SelectForm = ({
  contributors,
  partners,
  periods,
  countries,
  selected,
  onSelect
}) => {
  const { t } = useTranslation()
  return (
    <Row gutter={[16, 16]} className="program-popover-form">
      <Col span={24}>
        <DropdownFilter
          {...{
            label: t('Countries'),
            count: selected?.countries.length,
            items: countries,
            type: 'countries',
            selected,
            onSelect
          }}
        />
      </Col>
      <Col span={24}>
        <DropdownFilter
          {...{
            label: t('Contributors'),
            count: selected?.contributors?.length,
            items: contributors,
            type: 'contributors',
            selected,
            onSelect
          }}
        />
      </Col>
      <Col span={24}>
        <DropdownFilter
          {...{
            label: t('Reporting Periods'),
            count: selected?.periods?.length,
            items: periods,
            type: 'periods',
            selected,
            onSelect
          }}
        />
      </Col>
      <Col span={24}>
        <DropdownFilter
          {...{
            label: t('Partners'),
            count: selected?.partners?.length,
            items: partners,
            type: 'partners',
            selected,
            onSelect
          }}
        />
      </Col>
    </Row>
  )
}

const Taggable = ({ text, dataId, type, onClose }) => <Tag onClose={() => onClose(dataId, type)} closable>{text?.replace(/^(.{15}[^\s]*).*/, '$1')}</Tag>

const Filters = (props) => {
  const [visible, setVisible] = useState(false)
  const { selected, contributors, partners, loading, nfilter, onClose, onClear, onSearch } = props
  const { t } = useTranslation()
  return (
    <div style={{ padding: 12, backgroundColor: '#eee' }}>
      <Row gutter={[8, 8]}>
        <Col lg={5} xs={12}>
          <Input
            allowClear
            size="large"
            prefix={<Icon type="search" />}
            placeholder={t('Search Indicators')}
            onChange={(e) => onSearch(e.target.value)}
          />
        </Col>
        <Col lg={2} xs={12} style={{ marginRight: 20 }}>
          <Popover placement="bottom" content={<SelectForm {...props} />} visible={visible}>
            <Button
              size="large"
              loading={loading}
              onClick={() => setVisible(!visible)}
              className={classNames({ 'bg-dark': nfilter })}
            >
              <Icon
                type="control"
                style={{
                  fontSize: 18,
                  WebkitTransform: 'rotate(90deg)',
                  msTransform: 'rotate(90deg)',
                  transform: 'rotate(90deg)'
                }}
              />
              {t('Filter By')}&nbsp;
              {nfilter ? <BadgeCircle count={nfilter} /> : null}
            </Button>
          </Popover>
        </Col>
        <Col lg={14} xs={24}>
          <div className="program-filters-grid">
            <div className="row">
              <ul>
                {selected.countries.length ? (
                  <li>
                    <div className="label">{t('countries')}</div>
                    {selected.countries.map((c) => <Taggable key={c} {...{ onClose, dataId: c, text: countriesDict[c] || '', type: 'countries' }} />)}
                  </li>
                ) : null}
                {selected.contributors.length ? (
                  <li>
                    <div className="label">{t('contributors')}</div>
                    {
                      contributors
                        ?.filter((c) => selected.contributors.map((cx) => parseInt(cx, 10))?.includes(c?.id))
                        ?.map((c) => <Taggable key={c?.id} {...{ onClose, dataId: c?.id, text: c?.value, type: 'contributors' }} />)
                    }
                  </li>
                ) : null}
                {selected.periods.length ? (
                  <li>
                    <div className="label">{t('periods')}</div>
                    {selected?.periods?.map((p) => <Taggable key={p} {...{ onClose, dataId: p, text: p, type: 'periods' }} />)}
                  </li>
                ) : null}
                {selected.partners.length ? (
                  <li>
                    <div className="label">{t('partners')}</div>
                    {
                      partners
                        ?.filter((p) => selected.partners.map((px) => parseInt(px, 10))?.includes(p?.id))
                        ?.map((p) => <Taggable key={p?.id} {...{ onClose, dataId: p?.id, text: p?.value, type: 'partners' }} />)
                    }
                  </li>
                ) : null}
              </ul>
            </div>
          </div>
        </Col>
        <Col lg={2} xs={24}>
          {nfilter ? (
            <Button type="link" style={{ fontSize: 12, fontWeight: 'bold', color: '#000' }} onClick={onClear}>
              <Icon type="close" />
              {t('Clear all filters')}
            </Button>
          ) : null}
        </Col>
      </Row>
      <div style={{ clear: 'both' }} />
    </div>
  )
}

export default Filters
