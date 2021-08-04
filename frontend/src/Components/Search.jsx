import React, {useState, useEffect} from "react";
import { render } from 'react-dom';
import { TextField, Link } from '@material-ui/core';
import history from "../history";
import { BrowserRouter as Router, Route } from 'react-router-dom';
import ReactDOM from "react-dom";
import CreateUser from "./CreateAccount";


function AddModel(){
    const handleSignUp = () => {
        const responseResult = fetch("http://127.0.0.1:8000/create_user").then(
            response => {
                history.push("/create_user")
                const elem = (
                <Router>
                    <div>
                        <Route path="/create_user/">
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
        Add new model
        </Link>
    )
}



export default function Search() {
    const [search, setSearch] = useState([])
    const fetchSearch = async () => {
        const response = await fetch("http://localhost:8000/search")
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
                <TextField id="search" size="small" variant="outlined"/> <br/>
                <AddModel />
        </div>
    
    );
}
