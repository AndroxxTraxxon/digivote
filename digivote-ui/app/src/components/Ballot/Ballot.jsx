import React from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import cfg from '../../constants';
import { withRouter } from 'react-router-dom';
class Ballot extends React.Component{

  static propTypes = {
    children: PropTypes.any,
  }

  constructor(props){
    super(props);

    this.state = {
      form: {},
      ballot: []
    };

    this.fetchBallot = this.fetchBallot.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleFormValueChange = this.handleFormValueChange.bind(this);
    this.updateFormValue = this.updateFormValue.bind(this);
  }

  componentWillMount(){
    this.fetchBallot();
    const voter_id  = JSON.parse(localStorage.getItem("digivote.voter_id"));
    if(voter_id == null){
      const { history } = this.props;
      history.push("/registration");
    }
    this.setState({
      voter_id
    });
  }

  handleFormValueChange(event){
    const {name, value} = event.target;
    console.log(`Changing ${name} to ${value}`);
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

  fetchBallot(){
    const { baseUrl, resources } = cfg.api.ctf;
    axios.get(baseUrl + resources.ballot)
    .then((result) => {
      this.setState({
        ballot: result.data.items
      });
    }).catch((error) => {

    })
  }

  handleSubmit(event){
    event.preventDefault();
    const { baseUrl, resources } = cfg.api.ctf;
    const { form, voter_id} = this.state;
    axios.post(baseUrl + resources.vote, {
      form,
      voter: voter_id
    }).then(result => {
      const { history } = this.props;
      if(result.status === 200){
        alert("Vote accepted");
        localStorage.removeItem("digivote.voter_id");
        history.push("/");
      }else{
        alert(result.data);
      }
    })
  }

  render(){
    return (
      <div className="Ballot">
        <div className="Title">Please make select your votes.</div>
        {/* <br/>
        {voter_id}
        <br/> */}
        <form onSubmit={this.handleSubmit}>        
          {this.state.ballot.map((item, index) => 
            <div key={index} className="basic-input">
            <label htmlFor={item.title}>{item.title}</label>
              <select name={item.title} 
              value = {this.state.form[item.title]} 
              onChange={this.handleFormValueChange}>
                <option key={-1} value={undefined}>--Select an Option--</option>
                {item.options.map((option, opt_index) => 
                  <option key={opt_index} value={option}>{option}</option>
                )}
              </select>
            </div>
          )}
          <br/>
          <input type="submit" value="Submit Vote"/>
        </form>
        {/* <StateViewer state={this.state.form}/> */}
      </div>
    );
  }
}

export default withRouter(Ballot);