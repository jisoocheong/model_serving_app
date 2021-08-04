import React from "react";
import { render } from 'react-dom';
import CreateAccount from "./Components/CreateAccount"
import Login from "./Components/Login"
import Search from "./Components/Search"

function App() {
    
    return (
        <div>
            <Login/>
        </div>
            )
}

const rootElement = document.getElementById("root")
render(<App />, rootElement)


