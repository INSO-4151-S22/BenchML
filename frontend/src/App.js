import React from 'react';
import Navbar from "./Components/Navbar/Navbar";
import { BasicTable } from "./Components/MyModelsTable";
import './css/App.min.css';

function App() {
  return (
    <div className="App">
      <Navbar />
      <h1>My Models</h1>
      <BasicTable />
    </div>
  );
}

export default App;