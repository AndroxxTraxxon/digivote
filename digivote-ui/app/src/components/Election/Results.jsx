import React from 'react';
// import PropTypes from 'prop-types';

class Results extends React.Component{

  constructor(props){
    super(props);

    this.state = {

    };

    this.fetchElectionResults = this.fetchElectionResults.bind(this);
  }

  fetchElectionResults(){
    
  }

  render(){
    return (
      <div className="results">
        Results
      </div>
    );
  }
}

export default Results;