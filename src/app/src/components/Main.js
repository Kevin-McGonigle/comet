import React from 'react'
import Homepage from './Homepage/Homepage'
import { useLocation } from 'react-router-dom'
import { MetricsContainer } from './Metrics/MetricsContainer';

const Main = (props) => {
  console.log(props)
  const location = useLocation();
  if (location.pathname === "/") {
    return (
      <main>
        <Homepage />
      </main>
    )
  }

  return (
    <Main>
      <MetricsContainer />
    </Main>
  )
}

export default Main