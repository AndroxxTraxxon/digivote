import React from 'react';
import PropTypes from 'prop-types';
import { Route, Switch, withRouter } from 'react-router-dom';
import Results from './Results';
import Demographics from './Demographics';
import axios from 'axios';

class Election extends React.Component{

  static propTypes = {
    children: PropTypes.any,
    history: PropTypes.any
  }

  constructor(props){
    super(props);

    this.state = {
      rootPath: "/election/"
    }

    this.fetchElectionStatus = this.fetchElectionStatus.bind(this);
  }

  componentWillMount(){
    this.fetchElectionStatus();
  }

  fetchElectionStatus(){
    axios.get("https://ctf.cyber.stmarytx.edu/polls/status")
      .then((response) => {
        this.setState({
          status: response.data.status
        });
        // const { history } = this.props;
        // if(response.data.status === "closed"){
        //   history.push("/election/results");
        // }
      })
  }

  render(){
    console.log(this.props);
    const { children } = this.props;
    const { rootPath } = this.state;
    const electionAction = (this.state.status === "closed") ? "Open" : "Close";
    return (
      <div className="election">
        <div className="election-head">
        </div>
        <Switch>
          <Route path={ rootPath + "demographics" } 
            component={ Demographics }
          />
          <Route path={ rootPath + "results" }
            component={ Results }
          />
          <Route path={ rootPath } render={ () => (
              <div>
                Election Home
                <form action={"https://ctf.cyber.stmarytx.edu/polls/" + electionAction.toLowerCase() } method="POST">
                  <input type="submit" value={electionAction + " Election"}/>
                </form>
              </div>
            )}
          />
        </Switch>
        
      </div>
    );
  }
}

export default withRouter(Election);