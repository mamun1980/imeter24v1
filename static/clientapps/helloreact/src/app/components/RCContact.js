import React from "react";

import { LocationList } from './Locations';

export class RCContact extends React.Component {

    constructor(props) {
		super(props);
        this.state = {
            showlocations: false
        }
	}

    showAlert () {
        console.log('Hello world')
        

    }

    toggoleSites() {
        this.setState({
            showlocations: !this.state.showlocations
        })
    }

    render() {
        // console.log(props.users);
        return (
            
            <div className="box">
                <li key={this.props.user.pk} className="contact-list-row mdl-list__item mdl-list__item--two-line">
                    <span className="info-cell mdl-list__item-primary-content">
                        <i className="material-icons mdl-list__item-avatar">person</i>
                        <span>{this.props.user.fields.customer_name}</span>
                        <span className="mdl-list__item-sub-title">Account ID: {this.props.user.pk}</span>
                    </span>
                    <span className="info-cell mdl-list__item-primary-content">
                        <span>{this.props.user.fields.address_1}</span>
                        <span className="mdl-list__item-sub-title">{this.props.user.fields.city}</span>
                    </span>
                    <span className="info-cell mdl-list__item-primary-content">
                        <span>{this.props.user.fields.contact_type}</span>
                        <span className="mdl-list__item-sub-title">Phone: 78787878787</span>
                    </span>
                    <span className="info-cell mdl-list__item-primary-content">
                        <span>{this.props.user.fields.last_activity}</span>
                        <span className="mdl-list__item-sub-title">{this.props.user.fields.comments}</span>
                    </span>
                    <span className="mdl-list__item-secondary-content">
                        <button onClick={this.toggoleSites.bind(this)} className="mdl-button mdl-js-button mdl-button--fab mdl-button--mini-fab mdl-button--colored">
                            {this.state.showlocations ?
                            <i className="material-icons">remove</i> :
                            <i className="material-icons">add</i>
                            }
                        </button>
                    </span>
                </li>
                {this.state.showlocations ?
                    <LocationList contact={this.props.user.pk} showloc={this.state.showlocations} />
                : null }
            </div>
            
        );
    }
}
