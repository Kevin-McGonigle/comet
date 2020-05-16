import React from 'react'
import Homepage from './Homepage/Homepage'
import { useLocation } from 'react-router-dom'

const Main = (props) => {
  const location = useLocation();
  console.log(location.pathname);
  if (location.pathname === '/metrics') 
    console.log("metrics props", props)
    console.log("yes")
  return (
  <main>
    {
      <Homepage />
    }
  </main>
  )}

export default Main