import React from 'react';
import PropTypes from 'prop-types';

class Registration extends React.Component{

  static propTypes = {
    children: PropTypes.any,
  }

  constructor(props){
    super(props);

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  

  handleChange(){

  }

  handleSubmit(){

  }

  render(){
    return (
      <div>
        Registration

        <div className="registration-form-wrapper">
          <form>

          </form>
        </div>
      </div>
    );
  }
}

export default Registration;