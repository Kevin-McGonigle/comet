import React from 'react';
import { Provider } from 'react-redux';
import './App.css';
import configureStore from './configureStore';
import { TreeGraphContainer } from './components/general/TreeGraph/TreeGraphContainer';
import Homepage from './components/Homepage/Homepage';

function App() {
  const store = configureStore({});

  return (
    <Provider store={store}>
        <div className="App">
          <Homepage />
        </div>
      </Provider>
  );
}

export default App;
