import React from 'react';
import Navbar from "../Components/Navbar/Navbar";
import { BasicTable } from "../Components/MyModelsTable";

function MyModels() {
    return (
        <div className="App">
        <Navbar />
        <h1>My Models</h1>
        <BasicTable />
      </div>
    )
}

export default MyModels;