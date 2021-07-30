import React, {useState, useEffect} from "react";
import { render } from 'react-dom';
import { Redirect } from "react-router-dom";
import { TextField, Button } from '@material-ui/core';
import history from "../history"


var inputEmail = "";
var inputUsername = "";
var inputFirstPassword = "";
var inputSecondPassword = "";

function NewUser(){
    const handleSubmit = () => {
        var isValidUser = false;
        const responseResult = fetch("http://127.0.0.1:8000/create", {
            
        // fill in request


        }).then(response => {
            return response.json();
        }).then(data => {
            // fill in with valid new user info

            if (isValidUser) {
                history.push()
            }
        })
    }


    return (
        <Button variant="contained" color="primary" onClick={handleSubmit}>Sign Up</Button>
    )
}


export default function CreateAccount() {
    const [search, setSearch] = useState([])
    const fetchSearch = async () => {
        const response = await fetch("http://localhost:8000/create")
        const search = await response.json()
        setSearch(search.data)
    }

    useEffect(() => {
        fetchSearch()
    }, [])

    const setEmail = event => {
        inputEmail = event.target.value
    };
    const setUsername = event => {
        inputUsername = event.target.value
    };
    const setFirstPassword = event => {
        inputFirstPassword = event.target.value
    };
    const setSecondPassword = event => {
        inputSecondPassword = event.target.value
    };


    return (
        <div>
            <h3>Sign Up</h3>
            <div className="form-group">
                <label>Email</label><br />
                <TextField id="email" size="small" label="Enter email" variant="outlined" onChange={setEmail} />
            </div>

          <div className="form-group">
                <label>Username</label><br />
                <TextField id="username" size="small" label="Enter username" variant="outlined" onChange={setUsername} />
            </div>

            <div className="form-group">
                <label>Password</label> <br />
                <TextField id="firstpassword" type="password" size="small" label="Enter password" variant="outlined" onChange={setFirstPassword} />
            </div>
            <div className="form-group">
                <label>Reenter Password</label> <br />
                <TextField id="secondpassword" type="password" size="small" label="Enter password" variant="outlined" onChange={setSecondPassword} />
            </div>
            <NewUser/>
        </div>

    )
};
