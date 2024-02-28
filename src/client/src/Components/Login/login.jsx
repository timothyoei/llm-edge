import React from 'react'
import './login.css'
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from 'axios';

const Login = () => {
  const history = useNavigate();
  const [action, setAction] = useState("Login")
  const [User, setUser] = useState('')
  const [Password, setPassword] = useState('')
  const[Email,setEmail] = useState('')

  async function submit(e) {
    e.preventDefault();

    try {
      //port number?
      await axios.post("http://localhost:5001/api/sessions", {
        "email": Email,
        "password": Password
      })
        .then(res => {
          if (res.data === "exist") {
            history("/home", { state: { id: User } })
          }
          else if (res.data === "nonexist") {
            alert("User not found")
          }
        })
        .catch(e => {
          alert("incorrect credentials")
          console.log(e)
        })
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
            <input type="email" onChange={(e) => { setEmail(e.target.value) }} placeholder='Email' />
          </div>
          <div className='input'>
            <input type="password" onChange={(e) => { setPassword(e.target.value) }} placeholder='Password' />
          </div>
        </div>

        <div className='submit-container'>
          <div className={"submit"} onClick={submit/*()=>{ setAction("Login")}*/}>Login</div>

        </div>
      </form>
      <div className='NoAccount'>Don't have an account?<br></br><span><Link to="/SignUp">Sign Up here!</Link></span></div>
      <div className='forgot-password'>Forgot Password? <span>Click Here!</span></div>

    </div>

  )
}

export default Login