import React from 'react';
import axios from 'axios';
import { Link, withRouter } from 'react-router-dom';
import { Chart } from 'react-google-charts';
import PropTypes from 'prop-types';

class Demographics extends React.Component{

  constructor(props){
    super(props);

    this.state = {
      electionStatus: {}
    }

    this.fetchElectionParticipants.bind(this);
    this.fetchElectionRegistrants.bind(this);
  }

  componentWillMount(){
    this.fetchElectionStatus().then(() => {
      const { electionStatus } = this.state;
      if(electionStatus === "closed"){
        this.fetchElectionParticipants();
        this.fetchElectionRegistrants();
      }
      console.log(this.state);
    })
  }

  fetchElectionStatus(){
    return axios.get("https://ctf.cyber.stmarytx.edu/polls/status")
      .then((response) => {
        this.setState({
          electionStatus: response.data.status
        });
      });
  }

  fetchElectionParticipants(){
    return axios.get("https://cla.cyber.stmarytx.edu/voters?only_participants=true")
      .then((response) => {
        console.log(response.data);
        this.setState({
          participants: response.data
        })
      })
  }

  fetchElectionRegistrants(){
    return axios.get("https://cla.cyber.stmarytx.edu/voters")
      .then((response) => {
        console.log(response.data);
        this.setState({
          registrants: response.data
        })
      })
  }

  generateCityComparisonChart(){
    if(!this.state.participants || !this.state.registrants){
      return;
    }

    let cities = {};
    for(const voter of this.state.registrants){
      if(cities[voter.city] === undefined){
        console.log(voter.city);
        cities[voter.city] = {
          registrants: 1,
          participants: 0
        }
      }else{
        cities[voter.city].registrants++;
      }
    }

    for(const voter of this.state.participants){
      if(cities[voter.city] === undefined){
        cities[voter.city] = {
          registrants: 0,
          participants: 1
        }
      }else{
        cities[voter.city].participants++;
      }
    }
    let data = [
      ['Role', 'Registered', 'Voted']
    ];
    for(const city in cities){
      data.push([city, cities[city].registrants || 0, cities[city].participants || 0]);
    }
    return (
      <div style={{
        display:"inline-block",
        width: "50%",
        minHeight: "auto",
        marginBottom: "30px"
      }}>
        <Chart
          width={'500px'}
          height={'300px'}
          chartType="BarChart"
          loader={<div>Loading Chart</div>}
          data={data}
          options={{
            title: 'Cities Voters and Registrants',
            chartArea: { width: '50%' },
            hAxis: {
              title: 'Total Population',
              minValue: 0,
            },
            vAxis: {
              title: 'City',
            },
          }}
          // For tests
          rootProps={{ 'data-testid': '1' }}
        />
      </div>);
  }

  generateGenderComparisonChart(){
    if(!this.state.participants || !this.state.registrants){
      return;
    }
    console.log(this.state.participants);
    console.log(this.state.registrants);
    const womenVoters = this.state.participants.filter(voter => voter.gender === "female").length;
    const menVoters = this.state.participants.filter(voter => voter.gender === "male").length;
    const womenRegistrants = this.state.registrants.filter(voter => voter.gender === "female").length;
    const menRegistrants = this.state.registrants.filter(voter => voter.gender === "male").length;
    return (
      <div style={{
        display:"inline-block",
        width: "50%"
      }}>
        <Chart
          width={'500px'}
          height={'300px'}
          chartType="BarChart"
          loader={<div>Loading Chart</div>}
          data={[
            ['Role', 'Registered', 'Voted'],
            ['Women', womenRegistrants, womenVoters],
            ['Men', menRegistrants, menVoters],
          ]}
          options={{
            title: 'Genders of Voters and Registrants',
            chartArea: { width: '50%' },
            hAxis: {
              title: 'Total Population',
              minValue: 0,
            },
            vAxis: {
              title: 'Gender',
            },
          }}
          // For tests
          rootProps={{ 'data-testid': '1' }}
        />
      </div>);
  }

  generateDemographics(){
    return (
    <div>
      {this.generateGenderComparisonChart()}
      {this.generateCityComparisonChart()}
    </div> 
    );
  }

  render(){
    return (
      <div className="voter-demographics" style={{paddingBottom: "100px"}}>
        <h3>
          Voter Demographics
        </h3>
        {this.state.electionStatus === "open" && <div className="content">
          Sorry, the elections are still open.
          <br/>
          Demographics will not be available until the elections close.
          <br/>
          <Link to="/">Return to the Main Page</Link>
        </div>}
        {this.state.electionStatus === "closed" && this.generateDemographics()}
      </div>
    );
  }
}

Demographics.propTypes = {
  status: PropTypes.string
};

export default withRouter(Demographics);