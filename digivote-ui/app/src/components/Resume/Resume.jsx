import React from 'react';
import PropTypes from 'prop-types';
import BasicInput from '../BasicInput';
// import StateViewer from '../StateViewer';
import cfg from '../../constants';
import axios from 'axios';
import { normalizeSSN } from '../../util/normalizers';
import { withRouter } from 'react-router-dom';

class Resume extends React.Component{

  static propTypes = {
    children: PropTypes.any,
    history: PropTypes.any
  }

  constructor(props){
    super(props);
    this.state = {
      form: {
        firstName: "John",
        lastName: "Smith",
        ssn: "123-45-6789",
        birthdate: "1994-02-22"
      }
    }

    this.handleFormValueChange = this.handleFormValueChange.bind(this);
    this.updateFormValue = this.updateFormValue.bind(this);
    this.handleSubmit= this.handleSubmit.bind(this);
  }

  handleFormValueChange(event){
    const {name, value} = event.target;
    this.updateFormValue(name, value);
  }

  updateFormValue(name, value){
    let update = {...this.state.form} || {};
    update[name] = value;
    this.setState({
      form: {
        ...update
      }
    });
  } 

  handleSubmit(event){
    event.preventDefault();
    const {baseUrl, resources} = cfg.api.cla;
    const {form} = this.state;
    axios.post(baseUrl + resources.voters + "?fetch_user=true", form, {
      headers: {
        "Access-Control-Allow-Origin" : "http://digivote.cyber.stmarytx.edu"
      }
    })
    .then(result => {
      const {history} = this.props;
      localStorage.setItem("digivote.voter_id", JSON.stringify(result.data.voter_id));
      history.push('/ballot');
      this.setState({
        response: {
          time: (Date.now()),
          status: "success",
          ...result,
        }
      });
    })
    .catch(error => {
      this.setState({
        response: {
          ...error,
          status: "failed",
          time: (Date.now()),
        },
      });
      alert("Unable to retrieve voter account.");
      console.log(error);
    });

  }

  render(){
    const {form} = this.state;
    return (
      <div>
        Please confirm your information to continue to the ballot.

        <div className="registration-form-wrapper">
          <form onSubmit={this.handleSubmit}>
          <BasicInput
            label="First Name"
            input = {{
              name: "firstName",
              onChange: this.handleFormValueChange,
              placeholder: "John",
              value: form.firstName
            }}
          />
          <BasicInput
            label="Last Name"
            input = {{
              name: "lastName",
              onChange: this.handleFormValueChange,
              placeholder: "Smith",
              value: form.lastName
            }}
          />
          <BasicInput
            label="Social Security Number"
            input={{
              name: "ssn",
              onChange: this.handleFormValueChange,
              placeholder: "000-00-0000",
              value: form.ssn
            }}
            normalize={normalizeSSN}
          />          
          <BasicInput
            label="Birth Date"
            input = {{
              name: "birthdate",
              onChange: this.handleFormValueChange,
              placeholder: "YYYY-MM-DD",
              value: form.birthdate
            }}
          />
          <br/>
          <br/>
          <button onClick={this.handleSubmit}>
            Continue to Ballot
          </button>
          </form>
          {/* Form Values: 
          <StateViewer state={this.state.form}/>
          Response: 
          <StateViewer state={this.state.response}/> */}
        </div>
      </div>
    );
  }
}

export default withRouter(Resume);