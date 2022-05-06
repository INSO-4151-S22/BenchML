import React, { useEffect, useState, useRef } from 'react'
import Navbar from "../Components/Navbar/Navbar";
import { BasicTable } from "../Components/MyModelsTable";
import configJson from '../auth_config.json'
import { useAuth0 } from "@auth0/auth0-react";
import axios from 'axios';


const baseURL = configJson.baseUrl; 

function MyModels() {
    const { getAccessTokenSilently } = useAuth0(); 
    const [Models, setModels] = useState(null);

    let isRendered = useRef(false);
    // const getModels = async () => {
    //     const t = await getAccessTokenSilently();
    //     console.log(t);
    //     axios.get(baseURL,{ headers: { 'Authorization': `Bearer ${t}`}}).then((response) => {
    //         setModels(response.data);
    //         console.log(response);
    //     });

    //   };

    useEffect(() => {
        isRendered=true;
        const getModels = async () => {
            const t = await getAccessTokenSilently();
            console.log(t);
            axios.get(baseURL,{ headers: { 'Authorization': `Bearer ${t}`}}).then((response) => {
                if (isRendered) {
                    // console.log(response);
                    setModels(response.data);
                    
                }
                return null;
            }).catch(err => console.log(err));
            return () => {
                isRendered = false;
            }; 
        }
        getModels();

    }, []);

    return (
        <div className="App">
        <Navbar />
        <h1>My Models</h1>
        {Models ? <BasicTable models={ Models }/> : null }
      </div>
    )
}

export default MyModels;