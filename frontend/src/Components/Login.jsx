import React, {useState, useEffect} from "react";
import { render } from 'react-dom';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { Button, TextField, Link } from '@material-ui/core';
import Search from "./Search"
import CreateUser from "./CreateAccount"
import history from "../history"
import ReactDOM from 'react-dom'
import jwt_decode from "jwt-decode"



var inputUsername = "";
var inputPassword = "";

function SubmitLogin() {
    const LoginContext = React.createContext({
        fetchLogin: () => {}
    });
    const {fetchLogin} = React.useContext(LoginContext);

    const handleSubmit = () => {
        var isValidLogin = true;
        const responseResult = fetch("http://127.0.0.1:8000/", {
            "method": "POST",
            "headers": {
                "Content-Type": "application/json"
            },
            "body": JSON.stringify({"username" : inputUsername, "password" : inputPassword})
        }).then(response => {
            // This gets the response from the fetch
            console.log(response);
            return response.json();
        }).then(data => {
            // This gets the returned result 
            console.log(data);
            var token = JSON.parse(JSON.stringify(data))["token"]
            var decoded = jwt_decode(token)
            console.log(decoded)
            if (!(decoded === "not valid user")) {
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
 
            }

        }).catch(err => {
            console.error(err);
        });
    }
    return (
            <Button variant="contained" color="primary" onClick={handleSubmit}> Submit</Button>
    )
}



function SignUp(){
    const handleSignUp = () => {
        const responseResult = fetch("http://127.0.0.1:8000/create").then(
            response => {
                history.push("/create")
                const elem = (
                <Router>
                    <div>
                        <Route path="/create/">
                            <CreateUser />
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
        Sign Up
        </Link>
    )
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
            <SignUp/>
        </div>
    )
};
