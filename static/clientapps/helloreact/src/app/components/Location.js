import React from "react";

export class Location extends React.Component {

	constructor(props) {
		super(props);
        // console.log(props);
	}

  	render() {

	    return (
	    	<tr>
				<td className="mdl-data-table__cell--non-numeric">{this.props.site.pk}</td>
				<td>{this.props.site.fields.locationid}</td>
				<td>{this.props.site.fields.device_filename}</td>
				<td>{this.props.site.fields.device_login}</td>
				<td>{this.props.site.fields.device_address}</td>
				<td>{this.props.site.fields.device_register}</td>
				<td>Action</td>
			</tr>
	    );
  	}
}
