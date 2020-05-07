import React from 'react'
import { Switch, Route } from 'react-router-dom'
import Homepage from './Homepage/Homepage'
import { MetricsContainer } from './Metrics/MetricsContainer'

const Main = () => (
  <main>
    <Switch>
      <Route exact path='/' component={Homepage}/>
      <Route path='/metrics' component={MetricsContainer}/>
    </Switch>
  </main>
)

export default Main