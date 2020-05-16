import React from 'react';
import {Provider} from 'react-redux';
import './App.css';
import configureStore from './configureStore';
import  { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import Main from './components/Main';

function App() {
    const store = configureStore({});

  return (
    <Provider store={store}>
        <div className="App">
          <Main store={store}/>
        </div>
        <Router>
          <Switch>
            <Route exact path='/' />
          </Switch>
          <Switch>
            <Route path='/metrics' />
          </Switch>
        </Router>
      </Provider>
  );
}

export default App;
