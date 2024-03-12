import React from 'react'
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from 'axios';

import './Signup.css'
import StarsCanvas from './Stars';

const Signup = () =>{
    const navigate = useNavigate();
    const [action, setAction] = useState("Sign Up")
    const[User, setUser] = useState('')
    const[Password, setPassword] = useState('')

    async function submit(e){
      e.preventDefault();

      try {
        await axios.post("http://localhost:8000/api/users", {
          "username": User,
          "password": Password,
        })
        .then(res => {
          if (res.status === 201) {
            navigate("/")
          } else if(res.status === 400) {
            console.log(res.data.error);
          } else if (res.status === 409) {
            console.log(res.data.error);
          }
        }).catch(e => {console.log(e)})
      }
      catch{
          console.log(e);
      }
    }

    return (
        <div >
          <StarsCanvas/>
          <div className = 'container'> 
            <div className = ' header'>
              <div className = 'text'>{action}</div>
              <div className = 'underline'></div>
            </div>
              <form action = "POST">
                <div className = 'inputs'>
                  <div className = 'input'>
                    <input type ="text" onChange={(e) => {setUser(e.target.value)}} placeholder='Username'/>
                  </div>
                  <div className = 'input'>
                    <input type ="password" onChange={(e) => {setPassword(e.target.value)}} placeholder='Password'/>
                  </div>
                </div>
                <div className = 'submit-container'>
                  <div className = {"submit"} onClick={submit/*()=>{ setAction("Sign Up")}*/}>Sign Up</div>  
                </div>
              </form>
              <div className = 'NoAccount'>Already have an account?<br></br><span><Link to = "/">Login here!</Link></span></div>
          </div>
        </div>
    )
}

export default Signup 