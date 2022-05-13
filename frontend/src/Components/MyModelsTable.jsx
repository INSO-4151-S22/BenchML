import React, { useMemo, useState, useEffect } from 'react'
import { useTable } from 'react-table'
import { COLUMNS } from './Columns'
import { useAuth0 } from "@auth0/auth0-react";
import axios from 'axios';
import '../css/ModelsTable.min.css'
import "../css/Results.min.css"
import configJson from '../auth_config.json';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import { CopyToClipboard } from "react-copy-to-clipboard";



const baseURL = configJson.baseUrl; 

export function BasicTable(props) {

    const { getAccessTokenSilently } = useAuth0(); 
  
    
    const columns = useMemo(() => COLUMNS, [])
    const data = useMemo(() => props.models, []);
    const [resultsModal, setResultsModal] = useState(false);
    const [status, setStatus] = useState({"info":"", "detail":"", "model_type":""});

    const toggleResults = () => {
        setResultsModal(!resultsModal)
    }

    const getModelResults = async (results) => {
        const t = await getAccessTokenSilently();
        axios.get(baseURL+`/models/${results.mid}/details`,{ headers: { 'Authorization': `Bearer ${t}`}})
        .then((response) => {
            console.log(response.data)
            if("adversarial" === response.data[0].type){
                setStatus({"name":results.name, "original_accuracy":response.data[0].detail, "adversarial_accuracy":response.data[1].detail, "model_type":response.data[0].type})
            }
            else{
                setStatus({"name":results.name, "best_config":response.data[0].detail, "accuracy": response.data[2].detail, "loss":response.data[1].detail, "model_type":response.data[0].type})

            }
        })
        .catch(err => console.log(err))
        
    }

    const setModelResults = (row) => {
        toggleResults();
        getModelResults({'mid':row.original.mid, 'name':row.original.name, 'date':row.original.date, 'model_source':row.original.model_source});
    }


    const [val, setVal]= useState(parseJson())

    function parseJson(){
        try {
          return JSON.stringify(status);
        } catch(ex){
          return "";
        }
    }
    
    const tableInstance = useTable({
        columns,
        data
    })

    const { 
        getTableProps, // table props from react-table
        getTableBodyProps, // table body props from react-table
         headerGroups, // headerGroups, if your table has groupings
         rows, // rows for the table based on the data passed
         prepareRow, // Prepare the row (this function needs to be called for each row before getting the row props)
    } = tableInstance


    const [value, setValue] = React.useState('Controlled');
    
    const handleChange = (event) => {
        setValue(event.target.value);
    }

    


  
    return      (
        <div>
            {
                resultsModal && (
                         <div className="results-modal">
                            <div className="results-overlay">
                                <div className = "results-content">
                                <div className='results'>
                                   <p className='title'> {`${status.name}`} </p>

                                   <CopyToClipboard
                                    text="text"
                                    onCopy={() => {
                                        alert("Copied")
                                    }}>
                                    <span> <TextField
                                    id="standard-multiline-flexible"
                                    label="Results"
                                    multiline
                                    value={parseJson()}
                                    
                                    onChange={handleChange}
                                    variant="standard"
                                    /></span>
                                    </CopyToClipboard>
                                    {/* {`The info is: ${status.info}`}
                                    {`The detail is: ${status.detail}`}
                                    {`The eval type is: ${status.model_type}`} */}
                                    </div>
                                    <button className="close-results"
                                        onClick={toggleResults}>
                                        X
                                    </button>
                                   
                                    <div className='best-trial'>

                                    </div>
                                </div>
                  
                            </div>
                        </div>
                )
            }
            <table   {...getTableProps()}>
            <thead>
                {
                    headerGroups.map((headerGroup) => (
                    <tr {...headerGroup.getHeaderGroupProps()} >
                    {
                        headerGroup.headers.map(column => (
                            <th {...columns.getHeaderProps}>{column.render('Header')}</th>
                        ))
                    }
                    </tr>

                ))}
                
            </thead>
            <tbody {...getTableBodyProps()}>
                {rows.map(row => {
                prepareRow(row)
                return (
                    <tr onClick={() => setModelResults(row)} {...row.getRowProps()}>
                    {row.cells.map(cell => {
                        return (
                        <td
                            {...cell.getCellProps()}
                        >
                            {cell.render('Cell')}
                        </td>
                        )
                    })}
                    </tr>
                )
               })}
            </tbody>

            </table>
        </div>
        
    )
}