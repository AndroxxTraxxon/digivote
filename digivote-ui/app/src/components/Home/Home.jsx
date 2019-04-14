import React from 'react';
// import PropTypes from 'prop-types';

import { Link } from 'react-router-dom';

class Home extends React.Component{

  render(){
    return (
      <div>
        <h1>Welcome to <b>Digivote</b> digital voting services!</h1>
        <p>
        We provide voting and tallying services for clients in need of anonymous
        voting solutions.
        </p>
        <hr/>
        <div style={{display: "inline-block", width: "50%"}}>
          <h2>
          Are you ready to Vote? 
        </h2>
        <Link to="/registration">
          Register to Vote
        </Link>
        </div>
        <div style={{display: "inline-block", width: "50%"}}>
          <h3>
            Already Registered?
          </h3>
          <Link to="/resume">
            Continue voting
          </Link>
        </div>
        <hr/>
        <div style={{display: "inline-block", width: "50%"}}>
          <h2>
            We also have the latest results!
          </h2>
          <Link to="/election">
            Election Results
          </Link>
        </div>
        <div style={{display: "inline-block", width: "50%"}}>
          <h2>
            Click here to access the Election Demographics!
          </h2>
          <Link to="/demographics">
            Election Demographics
          </Link>
        </div>
      </div>
    );
  }
}

export default Home;