import '../../css/Navbar.min.css';
import React, { Component } from 'react';
import { Link } from 'react-router-dom'


function Navbar() {
    const hexColor = {
        color: '#ffffff'
    };

    return(
    <div className='navbar-items'>
        <div className='start'>
            <Link className='Bench' to="/" style={{ textDecoration: 'none'}}>Bench</Link>
            <Link className='ML' to="/" style={{ textDecoration: 'none'}}>ML</Link>
        </div>
        <div className='end'>
            <ul className='models-account'>
                <li className='nav-item'>
                    {/* <NavLink to="/mymodels" activeStyle={{color: "red", text}} */}
                <Link className="nav-item-link" to="/mymodels" style={{ textDecoration: 'none'}}>My Models</Link>
                </li>
                <li className='nav-item'>
                <Link className="nav-item-link" to="/profile" style={{ textDecoration: 'none'}}>My Account</Link>
                </li>
            </ul>
        </div>    
    </div>
    );
}

export default Navbar