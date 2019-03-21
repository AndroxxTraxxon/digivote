import React from 'react';
// import PropTypes from 'prop-types';

import { Link } from 'react-router-dom';

class Home extends React.Component{

  render(){
    return (
      <div>
        Home
        <br/>
        <Link to="/registration">
          Register
        </Link>
      </div>
    );
  }
}

export default Home;