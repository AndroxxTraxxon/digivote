import React from 'react';
import PropTypes from 'prop-types';

class Ballot extends React.Component{

  static propTypes = {
    children: PropTypes.any,
  }

  render(){
    return (
      <div className="Ballot">
        Ballot
      </div>
    );
  }
}

export default Ballot;