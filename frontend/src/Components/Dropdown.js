import React, { useState } from "react";
import styled from 'styled-components';

export default function Dropdown() {

    const [isOpen, setIsOpen] = useState(false);
    const [selectedOption, setSelectedOption] = useState(null);
    const toggling = () => setIsOpen(!isOpen);
    const options = ["keras", "pytorch"];

    const onOptionClicked = value => () => {
    setSelectedOption(value);
    setIsOpen(false);
    console.log(selectedOption);
    };

    const Main = styled("div")`
        font-family: sans-serif;
        background: #f0f0f0;
        margin-top: 4%;
        margin-right: 100%;
        `;

    const DropDownContainer = styled("div")`
        width: 10.5em;
        margin: 0 auto;
        `;
    const DropDownHeader = styled("div")`
        margin-bottom: 0.8em;
        padding: 0.4em 2em 0.4em 1em;
        box-shadow: 0 2px 3px rgba(0, 0, 0, 0.15);
        font-weight: 500;
        font-size: 1rem;
        color: #3faffa;
        background: #ffffff;
        color: #1E2019;
        `;
    const DropDownListContainer = styled("div")``;
    const DropDownList = styled("ul")`
        padding: 0;
        margin: 0;
        padding-left: 1em;
        background: #ffffff;
        border: 2px solid #e5e5e5;
        box-sizing: border-box;
        color: #3faffa;
        font-size: 1rem;
        font-weight: 500;
        &:first-child {
        padding-top: 0.8em;
        }
        `;
    const ListItem = styled("li")`
        list-style: none;
        margin-bottom: 0.8em;
        `;
    return(
        <Main>
        <DropDownContainer>
            <DropDownHeader onClick={toggling}>
            {selectedOption || "keras"}
            </DropDownHeader>
            {isOpen && (
            <DropDownListContainer>
            <DropDownList>
              {options.map(option => (
                <ListItem onClick={onOptionClicked(option)} key={Math.random()}>
                  {option}
                </ListItem>
                ))}
            </DropDownList>
            </DropDownListContainer>
            )}
        </DropDownContainer>
        </Main>

    );
}