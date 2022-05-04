import React, { useState } from "react";
import "../css/Modal.min.css";
import Dropdown from "./Dropdown";


export default function Modal() {
    // Consts used in modal
    const [modal, setModal] = useState(false);
    const toggleModal = () => {
        setModal(!modal)
    }
    const [inputs, setInputs] = useState({});
    const handleChange = (event) => {
        const name = event.target.name;
        const value = event.target.value;
        setInputs(values => ({...values, [name]: value}))
      }

    const onOptionClicked = value => () => {
    setSelectedOption(value);
    setIsOpen(false);
    console.log(selectedOption);
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        alert(inputs);
      }

    if(modal) {
        document.body.classList.add('active-modal')
    } else {
        document.body.classList.remove('active-modal')
    }
    return (
        <>
        <button
            onClick={toggleModal}
            className="btn-modal">
            Add new model
        </button>
        {modal && (
            <div className="modal">
            <div className="overlay"></div>
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
                        <label> Git Repository URL
                            <input 
                                type="url"
                                name="repourl"
                                value={inputs.repourl || ""}
                                onChange={handleChange}
                            />
                        </label>
                        <Dropdown />
                    </form>
                    </div>
                    <div className="bottom-buttons">
                        <button className="close-modal"
                        onClick={toggleModal}>
                        Cancel
                        </button>
                        <input type="submit" value="Submit" />
                    </div>
                {/* </div> */}
            </div>
            </div>
        )}
        </>
    );
}