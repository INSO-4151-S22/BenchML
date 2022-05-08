import React from 'react';
import './css/App.min.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MyModels from './pages/MyModels';
import Home from "./pages/Home";
import { useAuth0 } from '@auth0/auth0-react';
import Navbar from './Components/Navbar/Navbar';

function App() {
    const {
        isLoading,
        isAuthenticated,
        error,
        // user,
        loginWithRedirect,
        // logout,
    } = useAuth0();

    if (isLoading) {
        return <div>Loading...</div>;
      }
      if (error) {
        return <div>Oops... {error.message}</div>;
      }
    
      if (isAuthenticated) {
        return (
            <Router>
                <Navbar />
              <Routes>
                <Route path="/" element={ <Home></Home> }></Route>
                <Route path="/mymodels" element={ <MyModels></MyModels>}></Route>
              </Routes>
            </Router>
    
    
        );
      } else {
        return <button onClick={loginWithRedirect}>Log in</button>;
      }
    }


export default App;