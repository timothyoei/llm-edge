import{ BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useState } from 'react';

import './App.css';
import Login from './Components/Login';
import Signup from './Components/Signup';
import Home from './Components/Home';
import StarsCanvas from './Components/Stars';

const App = () => {
  return (
    <div className='App'>
      <StarsCanvas/>
        <Routes>
          <Route path = "/" element = {<Login/>}/>
          <Route path = "/signup" element = {<Signup/>}/>
          <Route path = "/home" element = {<Home/>}/>
        </Routes>
    </div>
  );
}

//michael 

export default App;