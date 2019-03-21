import React from 'react';
// import PropTypes from 'prop-types';
import cfg from '../../constants';
import axios from 'axios'

class Participants extends React.Component{

  constructor(props){
    super(props);
    
    this.state = {
      voters: {
        haveVoted: [],
        haveRegistered: []
      }
    }

    this.fetchPeopleWhoRegistered = this.fetchPeopleWhoRegistered.bind(this);
    this.fetchPeopleWhoVoted = this.fetchPeopleWhoVoted.bind(this);
  }

  fetchPeopleWhoVoted(){
    const {baseUrl, resources} = cfg.api.cla;
    axios.get(baseUrl + resources.participants, {}, {
      headers: {
        "Access-Control-Allow-Origin" : "http://digivote.cyber.stmarytx.edu"
      }
    }).then(result => {

    }).catch(error => {

    })
  }

  fetchPeopleWhoRegistered(){
    const {baseUrl, resources} = cfg.api.cla;
    axios.get(baseUrl + resources.voters, {}, {
      headers: {
        "Access-Control-Allow-Origin" : "http://digivote.cyber.stmarytx.edu"
      }
    }).then(result => {

    }).catch(error => {

    })
  }

  render(){
    const { haveVoted, haveRegistered } = this.state.voters;
    return (
      <div className="participants">
        Participants
        <div>
          Registered voters
          <table>
            <thead>
              <tr>
                <th>First Name</th> 
                <th>Last Name</th> 
                <th>Birthdate</th> 
              </tr>
            </thead>
            <tbody>
              { (haveRegistered && haveRegistered.length > 0 && haveRegistered.map((value, index) => {
                return <tr key={index}>
                  <td>{value.firstName}</td>
                  <td>{value.lastName}</td>
                  <td>{value.birthdate}</td>
                </tr>;
              })) || <tr><td>Nobody's registered yet!</td></tr>}
            </tbody>
          </table>
          <hr/>
          Participating Voters
          <table>
            <thead>
              <tr>
                <th>First Name</th> 
                <th>Last Name</th> 
                <th>Birthdate</th> 
              </tr>
              
            </thead>
            <tbody>
              { (haveVoted && haveVoted.length > 0 && haveVoted.map((value, index) => {
                return <tr key={index}>
                  <td>{value.firstName}</td>
                  <td>{value.lastName}</td>
                  <td>{value.birthdate}</td>
                </tr>;
              })) || <tr><td>Nobody's voted yet!</td></tr>}
            </tbody>
          </table>
        </div>
      </div>
    );
  }
}

export default Participants;