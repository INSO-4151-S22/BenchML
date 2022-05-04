import React from 'react';
import "../css/Home.min.css";

function Home() {
    return (
        <div className='container'>
            <div className='intro'>
            <p>Benchmarking and Optimization for your
               Machine Learning Models
            </p>
            </div>
            <button
            className="start-here">
            Start here
        </button>
        </div>
    );
}

export default Home;