import React from 'react';
import PropTypes from 'prop-types';

class StateViewer extends React.Component{

  static propTypes = {
    state: PropTypes.any
  }

  constructor(props){
    super(props);
    this.renderObject = this.renderObject.bind(this);
    this.renderProperty = this.renderProperty.bind(this);
  }

  renderProperty(key, label, value, level){
    const indent = Array(level).fill(null).map((value, index) => (
      <span key={index}>
        &#8286;&nbsp;
      </span>
    ));
    if((/\s/).test(label)){
      label = `"${label}"`;
    }
    let output;
    switch(typeof(value)){
      case "object":
      if(value == null){
        output = `null`;
      }else if (Array.isArray()){
        output = this.renderObject(value, level, ['[', ']']);
      }else{
        output = this.renderObject(value, level);
      }
      break;
      case "number":
      output = value;
      break;
      case "boolean":
      output = value ? 'true':'false';
      break;
      case "undefined":
      output = `undefined`;
      break;
      case "string": 
      output = `"${value}"`;
      break;
      default:
      output = typeof(value);
      break;
    }
    return (
    <span className="state-viewer-property" key={key}>
      <br/>{indent}{label}:&nbsp;{output}
    </span>
    );
    
  }

  renderObject(obj, level=0, [openBracket, closeBracket] = ['{', '}']){
    if(obj && typeof(obj) === 'object'){
      const indent = Array(level).fill(null).map((value, index) => (
        <span key={index}>
          &#8286;&nbsp;
        </span>
      ));
      return (
        <span className = "state-viewer-obj" style={{fontFamily:"'Courier New', Courier, monospace"}}>
          {openBracket}
          {Object.entries(obj).map(([label, value], index) => 
            this.renderProperty(index, label, value, level+1))}
          <br/>{indent}{closeBracket}
        </span>
      );
    }
  }

  render(){

    return(
    <div className={"stateViewer" + this.props.className}>
      {this.renderObject(this.props.state)}
    </div>
    ) 
  }
}

export default StateViewer;