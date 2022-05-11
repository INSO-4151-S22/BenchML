import React from 'react';
import './css/App.min.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MyModels from './pages/MyModels';
import Home from "./pages/Home";
import Profile from './pages/Profile';
import { useAuth0 } from '@auth0/auth0-react';
import Navbar from './Components/Navbar/Navbar';

function App() {
    const {
        isAuthenticated
    } = useAuth0();

    if (isAuthenticated){
        return (
            <Router>
                <Navbar />
              <Routes>
                <Route path="/" element={ <Home></Home> }></Route>
                
                <Route path="/mymodels" element={ <MyModels></MyModels>}></Route>
                <Route path="/profile" element={ <Profile></Profile>}></Route>
              </Routes>
            </Router>
    
    
        );}
    else{
      return(
        <Router>
          <Navbar />
          <Routes>
            <Route path="/" element={ <Home></Home> }></Route>
          </Routes>
        </Router>
      )
    }
    }


export default App;