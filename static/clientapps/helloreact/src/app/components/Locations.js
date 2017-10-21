import React from "react";
import axios from 'axios';

import { Location } from './Location';

export class LocationList extends React.Component {

	constructor(props) {
		super(props);
		// console.log(props);

		this.state = {
            name: "Mamun",
            sites: [],
            data: false
        };
        
	}

	componentDidMount() {
		var url = "/user/"+this.props.contact+"/sites/";
		// console.log(url);

        axios.get(url)
          .then(res => {
            this.setState({ sites: res.data });
          })
    }

  	render() {

	    return (
	    	<div>
	    		{this.state.sites.length > 0 ?
	    		
		    	<table className="loc-table mdl-data-table mdl-js-data-table mdl-data-table--selectable mdl-shadow--6dp">
					<thead>
						<tr>
						  <th className="mdl-data-table__cell--non-numeric">Location</th>
						  <th>Location Details</th>
						  <th>Device Filename</th>
						  <th>Device Login</th>
						  <th>Device Address</th>
						  <th>Device Register</th>
						  <th>Action</th>
						</tr>
					</thead>
					<tbody>
						{this.state.sites.map((l) => (
		                    <Location key={l.pk} site={l} />
		                ))}
						
					</tbody>
				</table>
				:
					<div className="alert">
		    			<h4>No data to display</h4>

		    		</div>
	    		}
			</div>
	    );
  	}
}
