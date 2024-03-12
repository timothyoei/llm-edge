import React from 'react'
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from 'axios';

import './Login.css'

const Login = () => {
  const navigate = useNavigate();
  const [action, setAction] = useState("Login")
  const [User, setUser] = useState('')
  const [Password, setPassword] = useState('')

  async function submit(e) {
    e.preventDefault();

    try {
      await axios.post("http://localhost:8000/api/sessions", {
        "username": User,
        "password": Password
      })
        .then(res => {
          if (res.status === 200) {
            navigate("/home", {state: {user: res.data.user, token: res.data.token}})
          } else if (res.status === 400) {
            console.log(res.data.error);
          } else if (res.status === 401) {
            console.log(res.data.error);
          } else if (res.status === 404) {
            console.log(res.data.error);
          }
        }).catch(e => {console.log(e)})
    }
    catch (e) {
      console.log(e);
    }
  }

  return (
    <div className='container'>
      <div className=' header'>
        <div className='text'>{action}</div>
        <div className='underline'></div>
      </div>
      <form action="POST">
        <div className='inputs'>
          <div className='input'>
            <input type="test" onChange={(e) => {setUser(e.target.value)}} placeholder='Username'/>
          </div>
          <div className='input'>
            <input type="password" onChange={(e) => {setPassword(e.target.value)}} placeholder='Password'/>
          </div>
        </div>
        <div className='submit-container'>
          <div className={"submit"} onClick={submit}>Login</div>
        </div>
      </form>
      <div className='NoAccount'>Don't have an account?<br></br><span><Link to="/SignUp">Sign Up here!</Link></span></div>
      <div className='forgot-password'>Forgot Password? <span>Click Here!</span></div>
    </div>
  )
}

export default Login