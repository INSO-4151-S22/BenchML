import React, { Component } from 'react';
import '../../css/Navbar.min.css';
import { FaUserAlt } from 'react-icons/fa';
import { IconContext } from 'react-icons';


class Navbar extends Component {
    render() {
        return(
        <div className='NavbarItems'>

            <div className='start'>
                <p className='Bench'>Bench</p>
                <p className='ML'>ML</p>
            </div>

            <div className='end'>
                <p className='MyModels' >My Models</p>
                <IconContext.Provider value={{size: "1rem"}}>
                <FaUserAlt className='user-icon'/>
                </IconContext.Provider>
                
            </div>
            
            
        </div>
          
       
        )
    }
}

export default Navbar