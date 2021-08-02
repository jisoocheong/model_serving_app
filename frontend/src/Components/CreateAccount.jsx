import React, {useState, useEffect} from "react";
import { render } from 'react-dom';
import { Redirect } from "react-router-dom";
import { TextField, Button, Link } from '@material-ui/core';
import history from "../history"
import { BrowserRouter as Router, Route } from 'react-router-dom';
import Search from "./Search"
import Login from "./Login"
import ReactDOM from 'react-dom'


var inputEmail = "";
var inputUsername = "";
var inputFirstPassword = "";
var inputSecondPassword = "";

function NewUser(){
    const handleSubmit = () => {

        const responseResult = fetch("http://127.0.0.1:8000/create", {
            "method": "POST",
            "headers": {
            "Content-Type": "application/json"
        },
            "body": JSON.stringify({"email" : inputEmail, "username" : inputUsername, "first_password": inputFirstPassword, "second_password": inputSecondPassword})

        }).then(response => {
            return response.json();
        }).then(data => {
            console.log(data);
           const userAdded = JSON.parse(JSON.stringify(data))["result"]
            

            if (userAdded) {
                history.push('/search/');
                
                const elem = (
                    <Router>
                        <div>
                            <Route path="/search/">
                                <Search />
                            </Route>
                        </div>
                    </Router>
                );
                ReactDOM.render(elem, document.getElementById("root"))
                
                alert("Successfully added as new user")
            } else {
                alert("Could not add as new user")                
            }
        })
    }


    return (
        <Button variant="contained" color="primary" onClick={handleSubmit}>Sign Up</Button>
    )
}

function LoginPage(){
    const handleSignUp = () => {
        const responseResult = fetch("http://127.0.0.1:8000/").then(
            response => {
                history.push("/")
                const elem = (
                <Router>
                    <div>
                        <Route path="/">
                            <Login/>
                        </Route>
                    </div>
                </Router>
            );
            ReactDOM.render(elem, document.getElementById("root"))

       
            
            }).catch(err => {
            console.error(err);
        });
    }
    
    return (
        <Link onClick={handleSignUp}> 
        Back to Login Page
        </Link>
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
            <LoginPage />
        </div>

    )
};
