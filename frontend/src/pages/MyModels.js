import React from 'react';
import Navbar from "../Components/Navbar/Navbar";
import { BasicTable } from "../Components/MyModelsTable";
import Modal from '../Components/Modal';

function MyModels() {
    return (
        <div className="App">
        <h1>My Models</h1>
        <Modal />
        <BasicTable />
      </div>
    );
}

export default MyModels;