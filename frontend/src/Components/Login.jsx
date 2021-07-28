import React, {useState, useEffect} from "react";
import { render } from 'react-dom';
import { BrowserRouter as Router, Route, Switch, Link } from 'react-router-dom';
//import '../../node_modules/bootstrap/dist/css/bootstrap.min.css';
import { Button, TextField } from '@material-ui/core';
import Search from "./Search"
import history from "../history"
import ReactDOM from 'react-dom'


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
            "body": "{}"
        }).then(response => {
            // This gets the response from the fetch
            console.log(response);
            return response.json();
        }).then(data => {
            // This gets the returned result 
            isValidLogin = JSON.parse(JSON.stringify(data))["output"] 
            console.log(data);

            if (isValidLogin) {
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
    return (
        <div>
            <h3>Sign In</h3>
            <p>
            <div className="form-group">
                <label>Username</label><br />
                <TextField id="username" size="small" label="Enter username" variant="outlined" />
            </div>

            <div className="form-group">
                <label>Password</label> <br />
                <TextField id="password" size="small" label="Enter password" variant="outlined" />
            </div>

            <SubmitLogin/>
            </p>
        </div>

    )



};
