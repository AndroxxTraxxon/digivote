import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';

import '../styles/page.css';
import '../styles/basic-input.css';

class Page extends React.Component{

  static propTypes = {
    children: PropTypes.any,
  }

  render(){
    const {children} = this.props;
    return (
      <div className="page">
        <header className="page-header">
          <Link to="/">
            <img className="header-logo"src="logo.png" alt="Digivote Logo"/>
          </Link>
          <div className="caption">  
            Digital Voting Services
          </div> 
        </header>
        <div className="page-content">
          {children}

          <br/>
          <hr/>
          <footer>
            All Rights Reserved. &copy; 2019  David Culbreth
          </footer>
        </div>
        
      </div>
    );
  }
}

export default Page;