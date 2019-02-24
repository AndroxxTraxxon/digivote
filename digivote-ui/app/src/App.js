import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Ballot from './components/Ballot';
import Home from './components/Home';
import Page from './components/Page';
import Registration from './components/Registration';
// import logo from './logo.svg';
import './App.css';
import Election from './components/Election';

class App extends Component {

  constructor(){
    super({});
    if(window.localStorage.digivote){
      this.state = JSON.parse(window.localStorage.digivote);
    }else{
      this.state = {
        voter: {
          firstName: null,
          lastName: null,
          address: {
            streetAddress: null,
            city: null,
            state: null,
            zip: null,
          },
          ssn: null,
          birthdate: null,
        },
        voteKey: null,

      }
    }

  }

  render() {
    return (
      <Router>
        <Page>
          <Switch>
            <Route exact path="/" component={Home}/>
            <Route path="/registration" component={Registration} />
            <Route path="/ballot" component={Ballot} />
            <Route path="/election" component={Election}/>
          </Switch>
        </Page>
      </Router>
    );
  }
}

export default App;
