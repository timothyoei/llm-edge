
import './App.css';
import Login from './Components/Login/login';
import Signup from './Components/Signup/signup';
import Chat from './Components/Chatbox/Chat';
import{BrowserRouter as Router, Routes, Route} from "react-router-dom";
import {useState} from 'react';
import StarsCanvas from './Components/Stars';

const App = () => {
  return (
    
    <div className='App'>
      <StarsCanvas/>
      
        <Routes>
          <Route path = "/" element = {<Login/>}/>
          <Route path = "/SignUp" element = {<Signup/>}/>
          <Route path = "/Home" element = {<Chat/>}/>
        </Routes>
      
    </div>
  );
}

export default App;
