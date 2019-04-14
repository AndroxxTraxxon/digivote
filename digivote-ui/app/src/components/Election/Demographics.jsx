import React from 'react';
import axios from 'axios';
// import PropTypes from 'prop-types';

class Demographics extends React.Component{

  constructor(props){
    super(props);

    this.state = {
      participants: {},
      registrants: {}
    }

    this.fetchElectionParticipants.bind(this);
    this.fetchElectionRegistrants.bind(this);
  }

  componentWillMount(){
    this.fetchElectionParticipants();
    this.fetchElectionRegistrants();
  }

  fetchElectionParticipants(){
    axios.get("https://cla.cyber.stmarytx.edu/voters?only_participants=true")
      .then((response) => {
        console.log(response.data);
        this.setState({
          participants: response.data
        })
      })
  }

  fetchElectionRegistrants(){
    axios.get("https://cla.cyber.stmarytx.edu/voters")
      .then((response) => {
        console.log(response.data);
        this.setState({
          registrants: response.data
        })
      })
  }

  render(){
    return (
      <div className="results">
        
      </div>
    );
  }
}

export default Demographics;