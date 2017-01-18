/*
    Akvo RSR is covered by the GNU Affero General Public License.
    See more details in the license.txt file located at the root folder of the
    Akvo RSR module. For additional details on the GNU license please see
    < http://www.gnu.org/licenses/agpl.html >.
 */

import React, { PropTypes } from 'react';
import {Panel} from 'rc-collapse';

import Level from './Level.jsx'


export default class Comments extends Level {
    constructor(props) {
        super(props);
        this.state = {model: "comments"};
    }

    renderPanel(comment) {
        return (
            <Panel header={comment.comment} key={comment.id}>
                <div>By: {comment.user_details.first_name}</div>
            </Panel>
        )
    }

    render() {
        return (
            <Level items={this.props.items} renderPanel={this.renderPanel.bind(this)}/>
        );
    }
}

Comments.propTypes = {
    items: PropTypes.array,
    callbacks: PropTypes.object
};
