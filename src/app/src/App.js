import React from 'react';
import { Provider } from 'react-redux';
import './App.css';
import configureStore from './configureStore';
import Main from './components/Main';

function App() {
  const store = configureStore({});

  return (
    <Provider store={store}>
        <div className="App">
          <Main />
        </div>
      </Provider>
  );
}

export default App;
