const express = require("express")
const collection = require("./mongo")
const cors = require("cors")
const app = express()
require('dotenv').config();
app.use(express.json())
app.use(express.urlencoded({extended: true}))
app.use(cors())

app.get("/", cors(), (req,res) => {

})

app.post("/",async(req,res)=>{
    const{user,password} = req.body

    try{
        const check = await collection.findOne({user:user})

        if(check){
            res.json("exist")
        }
        else{
            res.json("notexist")
            
        }
    }
    catch(e){
        res.json("notexist")
    }
})


app.post("/Signup",async(req,res)=>{
    const{email,password,user} = req.body

    const data = {
        email:email,
        password:password,
        user:user
    }

    /*try{
        const check = await collection.findOne({email:email})

        if(check){
            res.json("exist")
        }
        else{
            res.json("notexist")
            await collection.insertMany([data])
        }
    }
    catch(e){
        res.json("notexist")
    } */

    try{
        const check = await collection.findOne({user:user})

        if(check){
            res.json("exist")
        }
        else{
            res.json("notexist")
            await collection.insertMany([data])
        }
    }
    catch(e){
        res.json("notexist")
    }
})

app.listen('http://localhost:3000/',()=>{
    console.log("port connected")
})