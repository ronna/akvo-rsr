/** @jsx React.DOM */

// Akvo RSR is covered by the GNU Affero General Public License.
// See more details in the license.txt file located at the root folder of the
// Akvo RSR module. For additional details on the GNU license please see
// < http://www.gnu.org/licenses/agpl.html >.

var ApproveModal,
    Button = ReactBootstrap.Button,
    CountryJobTitle,
    DeleteModal,
    DropDownItem,
    DropdownButton = ReactBootstrap.DropdownButton,
    Employment,
    EmploymentList,
    MenuItem = ReactBootstrap.MenuItem,
    Modal = ReactBootstrap.Modal,
    ModalTrigger = ReactBootstrap.ModalTrigger,
    Table = ReactBootstrap.Table,
    TriggerModal,
    UserTable,
    initial_data,
    i18n;

// CSRF TOKEN
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

InviteRow = React.createClass({
    getInitialState: function() {
        return {
            button_text: '+',
            button_style: 'success'
        };
    },

    handleRowClick: function() {
        if (this.state.button_style === 'success') {
            this.props.addRow();
            this.setState({
                button_text: 'x',
                button_style: 'danger'
            });
        } else {
            this.props.deleteRow(this.props.rowKey);
        }
    },

    render: function() {
        var orgs = organisation_data.map(function(org) {
            return (
                <option key={org.id} value={org.id}>{org.name}</option>
            );
        });

        var roles = role_data.map(function(role) {
            return (
                <option key={role.id} value={role.id}>{role.name}</option>
            );
        });

        return (
            <tr className="invite-row">
                <td>
                    <input className="form-control" type="email" placeholder={i18n.email_text} maxLength="254" required="required" />
                </td>
                <td>
                    <select className="form-control org-select" defaultValue="">
                        <option key="" value="">{i18n.select_org_text}</option>
                        {orgs}
                    </select>
                </td>
                <td>
                    <select className="form-control role-select" defaultValue="">
                        <option key="" value="">{i18n.select_role_text}</option>
                        {roles}
                    </select>
                </td>
                <td>
                    <Button bsStyle={this.state.button_style} onClick={this.handleRowClick}>{this.state.button_text}</Button>
                </td>
            </tr>
        );
    }
});

InviteTable = React.createClass({
    getInitialState: function() {
        return {
            rowKey: 0
        };
    },

    componentDidMount: function() {
        if (this.isMounted()) {
            this.addRow();
        }
    },

    addRow: function () {
        this.setState({
            rowKey: this.state.rowKey + 1
        });

        var inviteTableBody = document.getElementById('invite-table').querySelector('tbody');
        var newRow = document.createElement('tr');
        newRow.setAttribute('id', 'row-' + this.state.rowKey);
        newRow.className = "invite-row";
        inviteTableBody.appendChild(newRow);
        React.renderComponent(<InviteRow rowKey={this.state.rowKey} addRow={this.addRow} deleteRow={this.deleteRow} />, newRow);
    },

    deleteRow: function(rowKey) {
        var row = document.getElementById('row-' + rowKey);
        row.parentNode.removeChild(row);
    },

    render: function() {
        return (
            <Table striped>
                <thead>
                    <tr>
                        <th>{i18n.email_text}</th>
                        <th>{i18n.organisations_text}</th>
                        <th>{i18n.role_text}</th>
                        <th> </th>
                    </tr>
                </thead>
                <tbody> </tbody>
            </Table>
        );
    }
});


InviteModal = React.createClass({
    getInitialState: function() {
        return {
            disable: false,
            successes: 0
        };
    },

    inviteApiCall: function(email, org, role, row) {
        if (email === "" && org === "" && role === "") {
            // Row without any data, ignore
        } else {
            // Create request
            var url = '/rest/v1/invite_user/?format=json';

            var request = new XMLHttpRequest();
            request.open('POST', url, true);
            request.setRequestHeader("X-CSRFToken", csrftoken);
            request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

            request.onload = function() {
                var status = request.status;
                var response = JSON.parse(request.responseText);

                if (status === 201) {
                    // Remove row
                    row.classList.add('has-success');
                    var button = row.querySelector('button');
                    button.parentNode.removeChild(button);
                    setTimeout(function() {
                        if (row.parentNode.querySelectorAll('tr').length === 1) {
                            // Only one row left, hack to close modal
                            var modalParent = document.querySelector('.modal').parentNode;
                            modalParent.innerHTML = '';
                            modalParent.appendChild(document.createElement('span'));
                        }
                        row.parentNode.removeChild(row);
                    }, 3000);
                } else if (status === 400) {
                    // Missing data
                    var missingData = response.missing_data;
                    for (var i = 0; i < missingData.length; i++) {
                        var fields = row.querySelectorAll('td');
                        var field = missingData[i];
                        if (field === 'email') {
                            fields[0].classList.add('has-error');
                        } else if (field === 'organisation') {
                            fields[1].classList.add('has-error');
                        } else if (field === 'group') {
                            fields[2].classList.add('has-error');
                        }
                    }
                } else {
                    // Forbidden or general error
                    row.classList.add('has-error');
                }
            };

            var data = "user_data=" + JSON.stringify({
                email: email,
                organisation: org,
                group: role
            });

            request.send(data);
        }
    },

    sendInvite: function() {
        // Disable invite button
        this.setState({
            disable: true
        });

        var inviteTable = document.getElementById('invite-table');
        var inviteRows = inviteTable.querySelectorAll('.invite-row');
        for (var i = 0; i < inviteRows.length; i++) {
            var inviteRow = inviteRows[i];
            var emailInput = inviteRow.querySelector('input').value;
            var orgInput = inviteRow.querySelector('.org-select').value;
            var roleInput = inviteRow.querySelector('.role-select').value;
            this.inviteApiCall(emailInput, orgInput, roleInput, inviteRow);
        }

        // Enable invite button again
        this.setState({
            disable: false
        });
    },

    render: function() {
        return this.transferPropsTo(
            <Modal bsSize="large" title="Invite Users">
                <div className="modal-body" id="invite-table">
                    {i18n.invite_users_heading}
                    <hr/>
                    <InviteTable />
                </div>
                <div className="modal-footer">
                    <Button onClick={this.props.onRequestHide} id="close-invite-modal">{i18n.close_text}</Button>
                    <Button onClick={this.sendInvite} bsStyle="success" disabled={this.state.disable}>{i18n.invite_users_text}</Button>
                </div>
            </Modal>
        );
    }
});


DeleteModal = React.createClass({
  deleteEmployment: function() {
    $.ajax({
      type: "DELETE",
      url: "/rest/v1/employment/" + this.props.employment.id + '/?format=json',
      success: function(data) {
        this.handleDelete();
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },

  handleDelete: function() {
    this.props.onDeleteToggle();
  },

  render: function() {
    return this.transferPropsTo(
      <Modal title={i18n.remove_user_text}>
      <div className="modal-body">
      {i18n.remove_text + ' ' + this.props.employment.user.first_name + ' ' + this.props.employment.user.last_name + ' ' + i18n.from_text + ' ' + this.props.employment.organisation.name + '?'}
      </div>
      <div className="modal-footer">
      <Button onClick={this.props.onRequestHide}>{i18n.close_text}</Button>
      <Button onClick={this.deleteEmployment} bsStyle="danger">{i18n.remove_button_text}</Button>
      </div>
      </Modal>
    );
  }
});


ApproveModal = React.createClass({
  approveEmployment: function() {
    $.ajax({
      type: "POST",
      url: "/rest/v1/employment/" + this.props.employment.id + '/approve/?format=json',
      success: function(data) {
        this.handleApprove();
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },

  handleApprove: function() {
    this.props.onRequestHide();
    this.props.onApproveToggle();
  },

  render: function() {
    return this.transferPropsTo(
      <Modal title="Approve user">
      <div className="modal-body">
      {i18n.approve_text + ' ' + this.props.employment.user.first_name + ' ' + this.props.employment.user.last_name + ' ' + i18n.at_text + ' ' + this.props.employment.organisation.name + '?'}
      </div>
      <div className="modal-footer">
      <Button onClick={this.props.onRequestHide}>{i18n.close_text}</Button>
      <Button onClick={this.approveEmployment} bsStyle="success">{i18n.approve_button_text}</Button>
      </div>
      </Modal>
    );
  }
});


TriggerModal = React.createClass({
  getInitialState: function() {
    return {
      visible: false
    };
  },

  componentDidMount: function() {
    var approved = this.props.employment.is_approved;
    if (this.isMounted() && this.props.delete) {
      this.setState({
        visible: true
      });
    } else if (this.isMounted() && !this.props.delete) {
      this.setState({
        visible: !approved
      });
    }
  },

  onApprove: function() {
    this.setState({
      visible: false
    });
  },

  render: function() {
    if ( !this.state.visible ) {
      return <span></span>;
    }
    if (this.props.delete) {
      return (
      <ModalTrigger modal={<DeleteModal employment={this.props.employment} onDeleteToggle={this.props.onDeleteToggle} />}>
      <Button bsStyle="danger" bsSize="xsmall">X</Button>
      </ModalTrigger>
      );
    } else {
      return (
        <ModalTrigger modal={<ApproveModal employment={this.props.employment} onApproveToggle={this.onApprove} />}>
        <Button bsStyle="success" bsSize="xsmall">&radic;</Button>
        </ModalTrigger>
      );
    }
  }
});

DropDownItem = React.createClass({
  setGroup: function() {
    $.ajax({
      type: "POST",
      url: "/rest/v1/employment/" + this.props.employment_id + '/set_group/' + this.props.group.id + '/?format=json',
      success: function(data) {
        this.props.onSetGroup(this.props.group.name);
      }.bind(this),
      error: function(xhr, status, err) {
        this.props.onSetGroup(this.props.old_group);
      }.bind(this)
    });
  },

  handleSetGroup: function() {
    // Ugly jQuery hack to close dropdown
    $("div.btn-group").removeClass("open");

    this.props.loading(true);
    this.props.onSetGroup(<i>{i18n.loading_text}</i>);
    this.setGroup();
    this.props.loading(false);
  },

  render: function() {
    return (
      <MenuItem eventKey={this.props.group.id} onClick={this.handleSetGroup}>{this.props.group.name}</MenuItem>
    );
  }
});


CountryJobTitle = React.createClass({
  render: function() {
    var country = this.props.country;
    var job_title = this.props.job_title;
    if (country === null && job_title === "") {
      return (
        <span>&nbsp;</span>
      );
    } else {
      var text = "(";
      if (job_title !== "") {
        text += job_title;
      }
      if (country !== null) {
        if (job_title !== "") {
          text += " ";
        }
        text += i18n.in_text + ' ' + country.name;
      }
      text += ")";
      return (
        <span className="small">{text}&nbsp; &nbsp;</span>
      );
    }
  }
});


Employment = React.createClass({
  getInitialState: function() {
    return {
      visible: true,
      button_title: '(' + i18n.none_text + ')',
      loading: false
    };
  },

  componentDidMount: function() {
    var group = this.props.employment.group;
    if (this.isMounted() && group !== null) {
      this.setState({
        button_title: group.name
      });
    }
  },

  isLoading: function(boolean) {
    this.setState({
      loading: boolean
    });
  },

  onDelete: function() {
    this.setState({visible: false});
  },

  setGroupName: function(group) {
    this.setState({
      button_title: group
    });
  },

  render: function() {
    var employment_id = this.props.employment.id;
    var setGroupName = this.setGroupName;
    var old_title = this.state.button_title;
    var loading = this.isLoading;
    var other_groups = this.props.employment.other_groups.map(function(group) {
      return (
        <DropDownItem key={group.id} group={group} employment_id={employment_id}
        onSetGroup={setGroupName} old_group={old_title} loading={loading} />
      );
    });
    if ( !this.state.visible ) {
      return <span></span>;
    } else {
      return (
        <span>
        {this.props.employment.organisation.name}&nbsp;
        <CountryJobTitle country={this.props.employment.country} job_title={this.props.employment.job_title} />
        <DropdownButton title={this.state.button_title} disabled={this.state.loading}>{other_groups}</DropdownButton> &nbsp; &nbsp;
        <TriggerModal employment={this.props.employment} onDeleteToggle={this.onDelete} delete={true} /> &nbsp;
        <TriggerModal employment={this.props.employment} onDeleteToggle={this.onDelete} delete={false} />
        </span>
      );
    }
  }
});

var EmploymentRow = React.createClass({
  render: function() {
    return (
      <tr>
      <td>{this.props.employment.user.email}</td>
      <td>{this.props.employment.user.first_name}</td>
      <td>{this.props.employment.user.last_name}</td>
      <td className="text-right">
          <Employment key={this.props.employment.id} employment={this.props.employment} />
      </td>
      </tr>
    );
  }
});


UserTable = React.createClass({
  getInitialState: function() {
    return {
      employments: []
    };
  },

  componentDidMount: function() {
    var employments = this.props.source;
    if (this.isMounted()) {
      this.setState({
        employments: employments
      });
    }
  },

  render: function() {
    var employments_table = this.state.employments.map(function(employment) {
      return (
        <EmploymentRow key={employment.id} employment={employment} />
      );
    });
    return (
      <Table striped>
          <thead>
              <tr>
                  <th>{i18n.email_text}</th>
                  <th>{i18n.first_name_text}</th>
                  <th>{i18n.last_name_text}</th>
                  <th className="text-right">{i18n.organisations_text}</th>
              </tr>
          </thead>
          <tbody>{employments_table}</tbody>
      </Table>
    );
  }
});


InviteButton = React.createClass({
    render: function() {
        return (
            <ModalTrigger modal={<InviteModal />}>
                <Button title={i18n.invite_users_text}>
                    <i className="glyphicon glyphicon-user"></i> +
                </Button>
            </ModalTrigger>
        );
    }
});


initial_employment_data = JSON.parse(document.getElementById("initial-employment-data").innerHTML);
organisation_data = JSON.parse(document.getElementById("organisation-data").innerHTML);
role_data = JSON.parse(document.getElementById("role-data").innerHTML);
i18n = JSON.parse(document.getElementById("user-management-text").innerHTML);

React.renderComponent(<UserTable source={initial_employment_data} />,
                      document.getElementById('user_table'));
React.renderComponent(<InviteButton />, document.getElementById('invite_button'));
