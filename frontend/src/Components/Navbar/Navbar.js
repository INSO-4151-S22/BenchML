import React, { Component } from 'react';
import { MenuItems } from "./MenuItems";
import '../../css/Navbar.min.css';

class Navbar extends Component {
    state = { clicked: false }
    render() {
        return(<nav className='NavbarItems'>
            <h1 className='Bench'>Bench</h1>
            <h1 className='ML'>ML</h1>
            
            
            <div className='account-icon' onClick={this.handleClick}>
                <svg xmlns="http://www.w3.org/2000/svg" width="2rem" height="2rem" fill="currentColor" class="bi bi-person" viewBox="0 0 16 16">
                <path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10z"/>
                </svg>
                {/* <i className={this.state.clicked ? 'fas fa-times' : 'bi bi-person'}></i> */}
            </div>
            <div className='list'>
                <ul>
                    {/* <div className=''></div> */}
                    {MenuItems.map((item,index) => {
                        return (
                        <li key={index}>
                            <a className={item.cName} href={item.url}>
                                {item.title}
                            </a>
                        </li>
                        )
                    })}
                </ul>
                </div>
        </nav>
        )
    }
}

export default Navbar