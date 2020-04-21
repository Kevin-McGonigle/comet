import React from 'react'
import { Switch, Route } from 'react-router-dom'
import Homepage from './Homepage/Homepage'
import Metrics from './Metrics/Metrics'

const Main = () => (
  <main>
    <Switch>
      <Route exact path='/' component={Homepage}/>
      <Route path='/metrics' component={Metrics}/>
    </Switch>
  </main>
)

export default Main