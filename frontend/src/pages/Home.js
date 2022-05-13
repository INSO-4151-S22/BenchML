import React from 'react';
import "../css/Home.min.css";
import { useAuth0 } from '@auth0/auth0-react';
import { Link } from 'react-router-dom';



function Home() {
    const {loginWithRedirect, isAuthenticated} = useAuth0();

    return (
        <div className='container'>
            <div className='intro'>
                <p>Benchmarking and Optimization for your
                Machine Learning Models
                </p>
            </div>
            {isAuthenticated ?
            <Link to="/mymodels" style={{ textDecoration: 'none'}}>
                <button className="start-here">Start Here</button> 
            </Link>
            :
            <div  className="start-here">
                <button
                onClick={() => loginWithRedirect()}>
                <p>Start here</p>
                </button>
            </div>
            
            }
        </div>
    );
}

export default Home;