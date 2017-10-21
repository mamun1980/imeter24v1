import React from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';

import { RCContactList } from './components/RCContactList';
import { LocationList } from './components/Locations';


class Dashboard extends React.Component {

	constructor(props) {
		super(props);

		this.state = {
            name: "Mamun",
            contacts: [],
            showLocations: false
        };

	}

    getLocations() {
        this.setState({
            showLocations: !this.state.showLocations
        })
    }

	componentDidMount() {
        axios.get("/user/contacts.json")
          .then(res => {
            this.setState({ contacts: res.data });
          })
    }

  	render() {

	    return (
            <div className="mdl-grid">
                <RCContactList contacts={this.state.contacts} showloc={this.getLocations.bind(this)} /> 
            </div>  
	    );
	}
}

ReactDOM.render(<Dashboard />, document.getElementById("dashboard"));
