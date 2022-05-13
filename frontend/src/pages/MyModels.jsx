import React, { useEffect, useState, useRef } from 'react';
import { BasicTable } from "../Components/MyModelsTable";
import configJson from '../auth_config.json';
import { useAuth0 } from "@auth0/auth0-react";
import axios from 'axios';
import Modal from '../Components/Modal';


const baseURL = configJson.baseUrl; 

function MyModels() {
    const { getAccessTokenSilently } = useAuth0(); 
    const [Models, setModels] = useState(null);
    const [hasPosted, setPosted] = useState(false);
    


    useEffect(() => {
        const getModels = async () => {
            const t = await getAccessTokenSilently();
            // console.log(t);
            axios.get(baseURL+"/models",{ headers: { 'Authorization': `Bearer ${t}`}}).then((response) => {
                if (isRendered) {
                    setModels(response.data);
                    console.log(response.data)
                }
                return null;
            }).catch(err => console.log(err));
            return () => {
                isRendered = false;
            }; 
        }
        getModels();
        setPosted(false);
    }, [hasPosted]);

    return (
        <div>
        <h1>My Models</h1>
        <Modal emptyModels={setModels} setPosted={setPosted}/>
        <div className='table-container'>
            {Models ? <BasicTable models={ Models } /> : null }
        </div>
      </div>
    );
}

export default MyModels;