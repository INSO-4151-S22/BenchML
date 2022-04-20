import React, { useMemo, useState, useEffect } from 'react'
import { useTable } from 'react-table'
// import MOCK_DATA from './MOCK_DATA.json'
import { COLUMNS } from './Columns'
import '../css/MyModelsTable.min.css'
import axios from 'axios'

export function BasicTable() {
    const [models, setModels] = useState(null);
    useEffect(() => {
        axios.get("http://localhost:8000/mymodels").then((response) => {
            setModels(response.data);
        });
    }, []);
    const columns = useMemo(() => COLUMNS, [])
    const data = useMemo(() => models.data, [])

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
                {
                    rows.map(row => {
                        prepareRow(row)
                        return (
                            <tr {...row.getRowProps()}> 
                            {
                                row.cells.map((cell) => {
                                    return <td{...cell.getCellProps()}>{cell.render('Cell')}</td>
                                })}
                            
                            </tr>
                        )
                    })
                }
               
            </tbody>
        </table>
    )
}