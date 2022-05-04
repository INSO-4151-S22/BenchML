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
                <p className='Bench'>Bench</p>
                <p className='ML'>ML</p>
            </div>
            <div className='end'>
                <ul className='models-account'>
                    <li className='nav-item'>
                        {/* <NavLink to="/mymodels" activeStyle={{color: "red", text}} */}
                    <Link className="nav-item-link" to="/mymodels" style={{ textDecoration: 'none'}}>My Models</Link>
                    </li>
                    <li className='nav-item'>
                    <Link className="nav-item-link" to="/" style={{ textDecoration: 'none'}}>My Account</Link>
                    </li>
                </ul>
            </div>    
        </div>
        );
    }

export default Navbar;