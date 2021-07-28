import React from "react";
import { render } from 'react-dom';
//import '../node_modules/bootstrap/dist/css/bootstrap.min.css';

import Login from "./Components/Login"
import Search from "./Components/Search"

function App() {
    
    return (
        <div>
            <Login />
        </div>
            )
}

const rootElement = document.getElementById("root")
render(<App />, rootElement)

