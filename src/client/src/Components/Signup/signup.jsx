import React from 'react'
import './signup.css'
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import StarsCanvas from '../Stars';
import axios from 'axios';

const Signup = () =>{
    const history = useNavigate();
    const [action, setAction] = useState("Sign Up")
    const[User,setUser] = useState('')
    const[Password,setPassword] = useState('')
    const[Email,setEmail] = useState('')

    async function submit(e){
        e.preventDefault();

        try{
            //port number?
            await axios.post("http://localhost:8000/api/users",{
                "username": User,
                "password": Password,
                "email": Email
            })
            .then(res=>{
                if(res.data === "exist") {
                    
                    alert("Username already exists")
                }
                else if(res.data === "nonexist") {
                    history("/home", {state: {id:User}})
                }
            })
            .catch(e=>{
                alert("incorrect credentials")
                console.log(e)
            })
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
                        <input type ="text" onChange = {(e) => {setUser(e.target.value)}} placeholder='Username'/>
                    </div>
                    <div className = 'input'>
                        <input type ="password" onChange = {(e) => {setPassword(e.target.value)}} placeholder='Password'/>
                    </div>
                    <div className = 'input'>
                        <input type ="email" onChange = {(e) => {setEmail(e.target.value)}} placeholder='Email'/>
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