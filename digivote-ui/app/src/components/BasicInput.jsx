import React from 'react';
import PropTypes from 'prop-types';

class BasicInput extends React.Component{

  static propTypes = {
    input: PropTypes.shape({
      disabled: PropTypes.bool,
      name: PropTypes.string,
      onChange: PropTypes.func,
      onBlur: PropTypes.func,
      onFocus: PropTypes.func,
      placeholder: PropTypes.string,
      type: PropTypes.string,
      value: PropTypes.any
    }),
    label: PropTypes.string,
  }
  constructor(props){
    super(props);
    this.state = {};
    this.getValue = this.getValue.bind(this);
    this.handleBlur = this.handleBlur.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event){
    let processedEvent = {...event};

    const passedChangeHandler = this.props.onChange || this.props.input.onChange || ((event) => {
      const {value} = event.target;
      this.setState({
        value
      });
    });
    if(this.props.normalize){
      processedEvent.target.value = this.props.normalize(processedEvent.target.value);
    }
    passedChangeHandler(processedEvent);
    
  }

  getValue(){
    return this.props.input.value || this.state.value;
  }

  handleBlur(event){
    if (this.props.validate){
      const error = this.validate(this.getValue());
      if(error){
        this.setState({
          error,
          invalid: true
        })
      }else{
        this.setState({
          error: undefined,
          invalid: false
        })
      }
    }
    if(this.props.onBlur){
      this.props.onBlur(event);
    }
  }

  validate(validators){
    const value = this.getValue();
    if (Array.isArray(validators)) {
      for(let validator of validators){
        const message = validator(value);
        if(message){
          return message;
        }
      }
    } else {
      return validators(value);
    }
  }

  render(){
    return (
      <div className = {"basic-input " + this.props.className}>
        <div className= {"basic-input-label" + this.props.invalid && " invalid"}>
          {this.props.label && <label htmlFor={this.props.input.name}>{this.props.label}</label>}
          {this.state.invalid === true && <div className="basic-input-error">
            <div className="basic-input-errorMessage">{this.state.error}</div>
          </div> }
        </div>
        <input 
          {...this.props.input}
          onChange={this.handleChange}
          value={this.props.input.value || this.state.value || ""}
          onBlur={this.handleBlur}
          type={this.props.input.type || "text"}
        />
      </div>
    );
  }
}

export default BasicInput;