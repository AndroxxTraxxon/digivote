import React from 'react';
import axios from 'axios';
import { Link, withRouter } from 'react-router-dom';
import { Chart } from 'react-google-charts';
import PropTypes from 'prop-types';

class Results extends React.Component{

  constructor(props){
    super(props);

    this.state = {
      participants: {},
      registrants: {},
      electionStatus: {},
    }

    this.fetchElectionResults.bind(this);
    this.fetchElectionStatus.bind(this);
  }

  componentWillMount(){
    this.fetchElectionStatus().then(() => {
      const { electionStatus } = this.state;
      if(electionStatus === "closed"){
        this.fetchElectionResults();
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

  fetchElectionResults(){
    return axios.get("https://ctf.cyber.stmarytx.edu/results")
      .then((response) => {
        this.setState({
          results: response.data
        })
      });
  }

  generateChart(name, optionData){
    let data = [
      [
        name ,
        'Votes',
        { role: 'style' },
        {
          sourceColumn: 0,
          role: 'annotation',
          type: 'string',
          calc: 'stringify',
        },
      ],
    ];
    for(let option in optionData){
      data.push([option, optionData[option], undefined, null]);
    }
    return (
      <div key={name} style={{
        display:"inline-block",
        width: "50%"
      }}>
        <Chart
        width={'500px'}
        height={'300px'}
        chartType="BarChart"
        loader={<div>Loading Chart</div>}
        data={data}
        options={{
        title: name,
        width: 600,
        height: 400,
        bar: { groupWidth: '95%' },
        legend: { position: 'none' },
      }}
      // For tests
      rootProps={{ 'data-testid': '6' }}
    />
      </div>);
  }

  generateResults(){
    console.log(this.state.results);
    let output = [];
    for(let entry in this.state.results){
      output.push(this.generateChart(entry, this.state.results[entry]));
    }
    return output;
  }

  render(){
    return (
      <div className="voter-demographics">
        <h3>
          Election Results
        </h3>
        {this.state.electionStatus === "open" && <div className="content">
          Sorry, the elections are still open.
          <br/>
          Election results will not be available until the elections close.
          <br/>
          <Link to="/">Return to the Main Page</Link>
        </div>}
        {this.state.electionStatus === "closed" && this.generateResults()}
      </div>
    );
  }
}
Results.propTypes = {
  status: PropTypes.string
}

export default withRouter(Results);