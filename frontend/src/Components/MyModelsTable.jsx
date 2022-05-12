import React, { useMemo, useState } from 'react'
import { useTable } from 'react-table'
import { COLUMNS } from './Columns'
import '../css/MyModelsTable.min.css'



export function BasicTable(props) {
    
    const modelDisplay = [];
    
    for (var i=0; i < props.models.length; i++){
        modelDisplay.push({"name":props.models[i].name, "date" : props.models[i].uploaded_at,"model_source":props.models[i].source});
    }

    
    const columns = useMemo(() => COLUMNS, [])
    const data = useMemo(() => modelDisplay, []);
    const [resultsModal, setResultsModal] = useState(false);

    const toggleResults = () => {
        setResultsModal(!resultsModal)
    }

    const tableInstance = useTable({
        columns,
        data
    })

    const { 
        getTableProps, 
        getTableBodyProps,
         headerGroups, 
         rows, 
         prepareRow,
    } = tableInstance

  

    return (
        <div>
            {
                resultsModal && (
                         <div className="modal">
                            <div className="overlay">
                            <div className = "modal-content">
                                {/* <div className="elements-container"> */}
                                <button className="close-results"
                                        onClick={toggleResults}>
                                        X
                                        </button>
                                        <form >
                                    TEXT
                                        
                                    </form>
                                
                                    
                                </div>
                            </div>
                        </div>
                )
            }
            <table {...getTableProps()}>
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
                    <tr onClick={toggleResults} {...row.getRowProps()}>
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