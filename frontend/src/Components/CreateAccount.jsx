import React, {useState, useEffect} from "react";
import { render } from 'react-dom';
import { Redirect } from "react-router-dom";
import { TextField } from '@material-ui/core';
    

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
    return (
        <div>
                <h3>Search for a model</h3>
                <label htmlFor="model">Model:</label><br/>
                <TextField id="search" size="small" variant="outlined"/>
        </div>
    
    );
}



export default function Login() {
    const [login, setLogin] = useState([]);
    const fetchLogin = async () => {
        const response = await fetch("http://127.0.0.1:8000/");
        const login_input = await response.json();
        setLogin(login_input.data);
    };
    useEffect(() => {
        fetchLogin();
    }, []);



    const setUsername = event => {
        inputUsername = event.target.value
    };

    const setPassword = event => {
        inputPassword = event.target.value
    };

    return (
        <div>
            <h3>Sign In</h3>
            <div className="form-group">
                <label>Username</label><br />
                <TextField id="username" size="small" label="Enter username" variant="outlined" onChange={setUsername} />
            </div>

            <div className="form-group">
                <label>Password</label> <br />
                <TextField id="password" type="password" size="small" label="Enter password" variant="outlined" onChange={setPassword} />
            </div>
            <SubmitLogin/>
        </div>

    )



};
