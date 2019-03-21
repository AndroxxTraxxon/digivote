import React from 'react';
import PropTypes from 'prop-types';
import { Route, Switch } from 'react-router-dom';
import Results from './Results';
import Participants from './Participants';

class Election extends React.Component{

  static propTypes = {
    children: PropTypes.any,
  }

  constructor(props){
    super(props);

    this.state = {
      rootPath: "/election/"
    }
  }

  render(){
    console.log(this.props);
    const { children } = this.props;
    const { rootPath } = this.state;
    return (
      <div className="election">
        Election
        <div className="election-head">
          Election Head
          { children }
        </div>
        <Switch>
          <Route path={ rootPath + "participants" } 
            component={ Participants }
          />
          <Route path={ rootPath + "results" }
            component={ Results }
          />
          <Route path={ rootPath } render={ () => (
              <div>
                Election Home
              </div>
            )}
          />
        </Switch>
        
      </div>
    );
  }
}

export default Election;