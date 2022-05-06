import React, { useMemo, useEffect, useState, useRef } from 'react'
import { useTable } from 'react-table'
import MOCK_DATA from './MOCK_DATA.json'
import { COLUMNS } from './Columns'
import '../css/MyModelsTable.min.css'


export function BasicTable(props) {
    
    const modelDisplay = [];
    for (var i=0; i < props.models.length; i++){
        modelDisplay.push({"name":props.models[i].name, "date" : props.models[i].uploaded_at,"description":props.models[i].source});
    }

    
    const columns = useMemo(() => COLUMNS, [])
    const data = useMemo(() => modelDisplay, []);

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
                {rows.map(row => {
                prepareRow(row)
                return (
                    <tr {...row.getRowProps()}>
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
    )
}