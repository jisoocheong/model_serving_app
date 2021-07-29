import React, {useState, useEffect} from "react";
import { render } from 'react-dom';
import { Redirect } from "react-router-dom";
import { TextField } from '@material-ui/core';
import '../../node_modules/bootstrap/dist/css/bootstrap.min.css';
    

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
                <TextField id="search" size="small" variant="outlined"/>
        </div>
    
    );
}
