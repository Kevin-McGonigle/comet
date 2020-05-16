import React from 'react';
import {Provider} from 'react-redux';
import './App.css';
import configureStore from './configureStore';
import  { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import Homepage from './components/Homepage/Homepage';
import { MetricsContainer } from './components/Metrics/MetricsContainer';

function App() {
    const store = configureStore({});

  return (
    <Provider store={store}>
      <main>
         <Router>
            <div className="App">
              <Switch>
                <Route exact path="/" component={Homepage} />
                <Route path='/metrics' component={MetricsContainer} />
              </Switch>
            </div>
          </Router>
      </main>
    </Provider>
  );
}

export default App;
