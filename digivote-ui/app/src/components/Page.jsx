import React from 'react';
import PropTypes from 'prop-types';

class Page extends React.Component{

  static propTypes = {
    children: PropTypes.any,
  }

  render(){
    const {children} = this.props;
    return (
      <div className="page">
        <header className="page-header">
          Page Header
        </header>
        <div className="page-content">
          Page Content
          {children}  
        </div>
      </div>
    );
  }
}

export default Page;