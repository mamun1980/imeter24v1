import React from "react";

import { RCContact } from './RCContact';

export class RCContactList extends React.Component {

	constructor(props) {
		super(props);
        // console.log(props);
	}

  	render() {

	    return (
	    	<div className="mdl-cell mdl-cell--12-col">
				<div className="mdl-card mdl-shadow--2dp">
				    <div className="mdl-card__supporting-text">
		                <ul className="mdl-list">
		                	<li className="contact-list-row-heading mdl-list__item mdl-list__item--two-line">
				                <span className="info-cell mdl-list__item-primary-content">
				                    <span>Customer Name</span>
				                </span>
				                <span className="info-cell mdl-list__item-primary-content">
				                    <span>Address</span>
				                </span>
				                <span className="info-cell mdl-list__item-primary-content">
				                    <span>Contact</span>
				                </span>
				                <span className="info-cell mdl-list__item-primary-content">
				                    <span>Comments</span>
				                    
				                </span>
				                <span className="mdl-list__item-primary-content">
				                    <span>Action</span>
				                </span>
				            </li>
			                {this.props.contacts.map((c,i) => (
			                    <RCContact key={i} user={ c } />
			                ))}
		                </ul>
					</div>
				</div>
			</div>
	    );
  	}
}
