import React, { useEffect, useState, useRef } from 'react';
import Navbar from "../Components/Navbar/Navbar";
import { BasicTable } from "../Components/MyModelsTable";
import configJson from '../auth_config.json';
import { useAuth0 } from "@auth0/auth0-react";
import axios from 'axios';
import Modal from '../Components/Modal';



const baseURL = configJson.baseUrl; 

function MyModels() {
    const { getAccessTokenSilently } = useAuth0(); 
    const [Models, setModels] = useState(null);
    

    let isRendered = useRef(false);

    useEffect(() => {
        isRendered=true;
        const getModels = async () => {
            const t = await getAccessTokenSilently();
            // console.log(t);
            axios.get(baseURL+"/models",{ headers: { 'Authorization': `Bearer ${t}`}}).then((response) => {
                if (isRendered) {
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
        <h1>My Models</h1>
        <Modal />
        {Models ? <BasicTable models={ Models }/> : null }
      </div>
    );
}

export default MyModels;