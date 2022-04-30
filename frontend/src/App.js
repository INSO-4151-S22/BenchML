import React from 'react';
// import Navbar from "./Components/Navbar/Navbar";
import './css/App.min.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MyModels from './pages/MyModels';
import Home from "./pages/Home";

function App() {
  return (
      <Router>
        <Routes>
          <Route path="/" element={ <Home></Home> }></Route>
          <Route path="/mymodels" element={ <MyModels></MyModels>}></Route>
        </Routes>
      </Router>
     
   
  );
}


export default App;