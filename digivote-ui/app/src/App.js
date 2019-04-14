import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Ballot from './components/Ballot';
import Home from './components/Home';
import Page from './components/Page';
import Registration from './components/Registration';
import './App.css';
import Election from './components/Election';
import Resume from './components/Resume/Resume';
import Demographics from './components/Election/Demographics';

class App extends Component {

  render() {
    return (
      <Router>
        <Page>
          <Switch>
            <Route exact path="/" component={Home} />
            <Route path="/registration" component={Registration} />
            <Route path="/ballot" component={Ballot} />
            <Route path="/election" component={Election} />
            <Route path="/resume" component={Resume} />
            <Route path="/demographics" component={Demographics} />
          </Switch>
        </Page>
      </Router>
    );
  }
}

export default App;
