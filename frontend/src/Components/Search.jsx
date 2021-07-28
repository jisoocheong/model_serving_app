import React, {useState, useEffect} from "react";
import { render } from 'react-dom';
import { Redirect } from "react-router-dom";
import { TextField } from '@material-ui/core';
import '../../node_modules/bootstrap/dist/css/bootstrap.min.css';
    

export default function Search() {
    const [search, setSearch] = useState([])
    const fetchSearch = async () => {
        const response = await fetch("http://localhost:8000/next")
        const search = await response.json()
        setSearch(search.data)
    }
    useEffect(() => {
        fetchSearch()
    }, [])
    return (
        <div>
            <p>
                <h3>Search for a model</h3>
                <label for="model">Model:</label><br/>
                <TextField id="search" variant="outlined"/>
            </p>
        </div>
    
    );
}
