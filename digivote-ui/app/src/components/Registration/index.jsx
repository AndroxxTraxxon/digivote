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

  

  handleChange(event){
    console.log(event.target.value, event.target.name)
  }

  handleSubmit(event){

  }

  render(){
    return (
      <div>
        Registration

        <div className="registration-form-wrapper">
          <form onSubmit={this.handleSubmit}>
          firstName='',
          lastName='',
          ssn='000-00-0000',
          streetAddress='',
          city='',
          state='',
          zip='00000',
          birthdate=datetime.datetime.now(),
          </form>
        </div>
      </div>
    );
  }
}

export default Registration;