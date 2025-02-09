import React, { useState, useEffect } from 'react'
import { Button, Modal, Input, Popconfirm } from 'antd'
import { useTranslation } from 'react-i18next'
import { connect } from 'react-redux'
import api from '../../../../utils/api'
import actionTypes from '../../action-types'

const ExternalProjects = ({ projectId, dispatch }) => {
  const { t } = useTranslation()
  const [isModalShown, showModal] = useState(false)
  const [inputValue, setInputValue] = useState('')
  const [adding, setAdding] = useState(false)
  const [projects, setProjects] = useState([])
  useEffect(() => {
    api.get(`/related_project/?related_project=${projectId}&relation=2`).then(({ data: { results } }) => {
      if (results.length && results[0]?.relatedProject) {
        dispatch({
          type: actionTypes.EDIT_SET_ITEM,
          sectionIndex: 1,
          setName: 'relatedProjects',
          itemIndex: 0,
          fields: {
            relatedProject: results[0]?.project,
            project: results[0]?.relatedProject,
            relation: 2
          }
        })
        dispatch({
          type: actionTypes.BACKEND_SYNC,
          lastSaved: null
        })
      }
      setProjects(results.filter(it => it.relatedIatiId !== ''))
    })
  }, [])
  const handleAdd = () => {
    setAdding(true)
    api.post('/related_project/', {
      project: projectId,
      relatedIatiId: inputValue,
      relation: '2'
    }).then(({data}) => {
      setAdding(false)
      showModal(false)
      setInputValue('')
      setProjects([...projects, data])
    }).catch((e) => {
      console.log(e)
      setAdding(false)
    })
  }
  const handleDelete = (project) => {
    api.delete(`/related_project/${project.id}`)
    setProjects(projects.filter(it => it.id !== project.id))
  }
  return (
    <div className="external-projects">
      {projects.length > 0 && (
        <div className="ant-row ant-form-item projects-list">
          <div className="ant-col ant-form-item-label"><label>{t('External child projects')}</label></div>
          {projects.map((project) =>
            <div className="project-row">
              <span>{project.relatedIatiId}</span>
              <Popconfirm
                title={t('Are you sure to delete this?')}
                onConfirm={() => handleDelete(project)}
                okText={t('Yes')}
                cancelText={t('No')}
              >
                <Button icon="delete" type="link" />
              </Popconfirm>
            </div>
          )}
        </div>
      )}
      <Button className="add-btn" type="link" icon="plus" onClick={() => showModal(true)}>{t('Add external contributing project')}</Button>
      <Modal
        title={t('Add external contributing project')}
        visible={isModalShown}
        onOk={handleAdd}
        okText={t('Add')}
        okButtonProps={{ disabled: inputValue.length === 0 }}
        onCancel={() => { showModal(false); setInputValue('') }}
        confirmLoading={adding}
      >
        <Input disabled={adding} placeholder="IATI Activity ID" value={inputValue} onChange={({target: {value}}) => setInputValue(value)} />
      </Modal>
    </div>
  )
}

const mapDispatchToProps = dispatch => {
  return {
    dispatch,
  }
}
export default connect(null, mapDispatchToProps)(ExternalProjects)
