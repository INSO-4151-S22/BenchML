import React, { useState } from "react";
import "../css/Modal.min.css";
import Dropdown from "./Dropdown";
import configJson from '../auth_config.json'
import { useAuth0 } from "@auth0/auth0-react";
import axios from 'axios';
import { Toaster, toast } from "react-hot-toast";

const baseURL = configJson.baseUrl; 

export default function Modal(props) {
    // Consts used in modal
    const { getAccessTokenSilently } = useAuth0(); 
    const [modal, setModal] = useState(false);
    const toggleModal = () => {
        setModal(!modal)
        // reset modal values
        setType("keras");
        setInputs({});
    }
    const [inputs, setInputs] = useState({});
    const [type, setType] = useState("keras");
    const notifySuccess = () => toast("Model uploaded succesfully!")
    

    const updateType = (newType) => {
        setType(newType);
    }
    const handleChange = (event) => {
        const name = event.target.name;
        const value = event.target.value;
        setInputs(values => ({...values, [name]: value}));
      }


    const postModel = async() => {
        const t = await getAccessTokenSilently();
        // console.log(t);
        // console.log(inputs.filename);
        // console.log(inputs.repourl);
        // console.log(type);

        const pm = async() => {
            const response = await axios.post(baseURL+"/models",
            {
                "name" : inputs.filename,
                "source" : inputs.repourl,
                "type" : type,
                "modules" : [(type == 'pytorch') ? "adversarial" : "optimizer"]
            },
            { headers: { 'Authorization': `Bearer ${t}`}}
            )
            .then((response) => {
                console.log(response);
                return response;
            })
        }
        
        toast.promise(
            
            pm(),

            {
                loading: 'Loading',
                success: (response) => 'Successfully uploaded',
                error: (err) => `There was an error ${err.toJSON().toString()}`,
            },
             {
                style: {
                    minWidth: '250px',
                  },
                  success: {
                    duration: 5000,
                    icon: '✅',
                  },
            }
        )
   
    }

    const handleSubmit = (event) => {
        // console.log(inputs);
        event.preventDefault();
        postModel();
        toggleModal();
        props.setPosted(true);
        props.emptyModels(null);
      }

    return (
        <>
        <Toaster/>
        <button
            onClick={toggleModal}
            className="btn-modal">
            Add new model
        </button>
        {modal && (
            <div className="modal">
            <div className="overlay">
            <div className = "modal-content">
                {/* <div className="elements-container"> */}
                    <div className="top-elements">
                        <form onSubmit={handleSubmit}>
                        <label> File name
                            <input 
                                type="text"
                                name="filename"
                                value={inputs.filename || ""}
                                onChange={handleChange}
                            />
                        </label> 
                        <label> Model JSON URL
                            <input 
                                type="url"
                                name="repourl"
                                value={inputs.repourl || ""}
                                onChange={handleChange}
                            />
                        </label>
                        Select model type
                        <Dropdown  func={setType}/>
                    <div className="bottom-buttons">
                        <button className="close-modal"
                        onClick={toggleModal}>
                        Cancel
                        </button>
                        <input type="submit" value="Submit"/>
                    </div>
                    </form>
                    </div>
                    
                </div>
            </div>
            </div>
        )}
        </>
    );
}