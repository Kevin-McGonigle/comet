import React from 'react';
import { Provider } from 'react-redux';
import './App.css';
import configureStore from './configureStore';
import { TreeGraphContainer } from './components/general/TreeGraph/TreeGraphContainer';

function App() {
  const store = configureStore({});

  return (
    <Provider store={store}>
        <div className="App">
            <TreeGraphContainer />
        </div>
      </Provider>
  );
}

export default App;
