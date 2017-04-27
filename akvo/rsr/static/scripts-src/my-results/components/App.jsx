/*
    Akvo RSR is covered by the GNU Affero General Public License.
    See more details in the license.txt file located at the root folder of the
    Akvo RSR module. For additional details on the GNU license please see
    < http://www.gnu.org/licenses/agpl.html >.
 */


import React from 'react'
import Select from 'react-select'
import 'react-select/dist/react-select.css';
import { connect } from "react-redux"

import {
    fetchModel, fetchUser, testFetchModel, lockSelectedPeriods, unlockSelectedPeriods
} from "../actions/model-actions"
// TODO: look at refactoring the actions, moving the dispatch calls out of them. Not entirely trivial...
import { setPageData } from "../actions/page-actions"
import {
    activateToggleAll, updateFormOpen, selectablePeriods, periodSelectReset,
    periodsThatNeedReporting, selectPeriodsThatNeedReporting
} from "../actions/ui-actions"

// import { c.OBJECTS_PERIODS, c.OBJECTS_UPDATES, c.UPDATE_STATUS_DRAFT, c.PARENT_FIELD } from "../const"
import * as c from "../const"
import {fieldValueOrSpinner, openNodes} from "../utils"

import Results from "./Results"
import { ToggleButton } from "./common"
import {getApprovedUpdates, getDraftUpdates} from "../selectors";


const dataFromElement = (elementName) => {
    return JSON.parse(document.getElementById(elementName).innerHTML);
};

const modifyUser = (isMEManager) => {
    return (data) => {
        // maintain compatibility with existing updates JSON
        data.approved_organisations = [data.organisation];
        data.isMEManager = isMEManager;
        // transform to common JSON data shape so normalize works in modelsReducer
        return {results: data};
    };
};


@connect((store) => {
    return {
        page: store.page,
        models: store.models,
        ui: store.ui,
        draftUpdates: getDraftUpdates(store),
        approvedUpdates: getApprovedUpdates(store),
    }
})
export default class App extends React.Component {
    constructor(props) {
        super(props);
        this.showDraft = this.showDraft.bind(this);
        this.showApproved = this.showApproved.bind(this);
        this.unlockSelected = this.unlockSelected.bind(this);
        this.lockSelected = this.lockSelected.bind(this);
        this.selectChange = this.selectChange.bind(this);
        this.state = {selectedOption: undefined}
    }

    fetchUser(userId) {
        fetchModel('user', userId, activateToggleAll);
        this.props.dispatch(
            {type: UPDATE_MODEL_FULFILLED, payload: {model, object}});

    }

    componentDidMount() {
        const project = dataFromElement('project-ids');
        const settings = dataFromElement('settings');
        const strings = dataFromElement('translation-texts');
        this.props.dispatch(setPageData({project, settings, strings}));

        const userId = dataFromElement('endpoint-data').userID;
        const isMEManager = dataFromElement('endpoint-data').isMEManager;
        fetchModel('user', userId, activateToggleAll, modifyUser(isMEManager));

        const projectId = project.project_id;
        fetchModel('results', projectId, activateToggleAll);
        fetchModel('indicators', projectId, activateToggleAll);
        // fetchModel('periods', projectId, [activateToggleAll, selectablePeriods]);
        fetchModel('periods', projectId, activateToggleAll);
        fetchModel('updates', projectId, activateToggleAll);
        fetchModel('comments', projectId, activateToggleAll);
    }

    showUpdates(updateIds) {
        periodSelectReset();
        updateIds.map((id) => updateFormOpen(id));
        openNodes(c.OBJECTS_UPDATES, updateIds, true);
    }

    showDraft() {
        this.showUpdates(this.props.draftUpdates);
    }

    showApproved() {
        this.showUpdates(this.props.approvedUpdates);
    }

    unlockSelected() {
        unlockSelectedPeriods();
    }

    lockSelected() {
        lockSelectedPeriods();
    }

    selectChange(e) {
        this.setState({selectedOptions: e});
        e.value();
    }

    needReporting() {
        selectPeriodsThatNeedReporting();
    }

    render() {
        const right = {float: 'right'};
        const clearfix = {clear: 'both'};
        const selectOptions = selectablePeriods(this.props.models.periods && this.props.models.periods.ids);
        const needReportingCount = fieldValueOrSpinner(periodsThatNeedReporting(), 'length');
        const needReportingLabel = `Need reporting (${needReportingCount})`;
        const draftUpdateCount = fieldValueOrSpinner(this.props.draftUpdates, 'length');
        const draftUpdateLabel = `Pending approval (${draftUpdateCount})`;
        const approvedUpdateCount = fieldValueOrSpinner(this.props.approvedUpdates, 'length');
        const approvedUpdateLabel = `Approved (${approvedUpdateCount})`;


        return (
            <div>
                <div className={'row results-bar-titles'}>
                    <div className="col-xs-3">Select periods</div>
                    <div className="col-xs-3">Period actions</div>
                    <div className="col-xs-2">Show periods</div>
                    <div className="col-xs-4">Show updates</div>
                </div>
                <div className={'row'}>
                    <div  className="col-xs-3">
                        <Select options={selectOptions} value={this.state.selectedOptions}
                                multi={false} placeholder="Select period(s)" searchable={false}
                                clearable={false} onChange={this.selectChange}/>
                    </div>
                    <div  className="col-xs-3">
                        <ToggleButton onClick={this.lockSelected} label="Lock selected"
                                      disabled={!this.props.ui.allFetched}/>
                        <ToggleButton onClick={this.unlockSelected} label="Unlock selected"
                                      disabled={!this.props.ui.allFetched}/>
                    </div>
                    <div  className="col-xs-2">
                        <ToggleButton onClick={this.needReporting} label={needReportingLabel}
                                      disabled={!this.props.ui.allFetched}/>
                    </div>
                    <div  className="col-xs-4">
                        <ToggleButton onClick={this.showDraft} label={draftUpdateLabel}
                                      disabled={!this.props.ui.allFetched}/>
                        <ToggleButton onClick={this.showApproved} label={approvedUpdateLabel}
                                      disabled={!this.props.ui.allFetched}/>
                    </div>
                </div>
                <div style={clearfix}></div>
                <Results parentId="results"/>
            </div>
        );
    }
}
