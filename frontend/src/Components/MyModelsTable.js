import React, { useMemo } from 'react'
import { useTable } from 'react-table'
// import MOCK_DATA from './MOCK_DATA.json'
import { COLUMNS } from './Columns'
import '../css/MyModelsTable.min.css'
import axios from 'axios'

const baseURL = "https://benchml.gabrielrosa.dev/models";
export function BasicTable() {
    const [Models, setModels] = React.useState(null);

    React.useEffect(() => {
        axios.get(baseURL).then((response) => {
            setModels(response.data);
            console.log(response);
        });
    }, []);
    const columns = useMemo(() => COLUMNS, [])

    // const tableInstance = useTable({
    //     columns,
    //     Models
    // })

    // const { 
    //     getTableProps, 
    //     getTableBodyProps,
    //      headerGroups, 
    //      rows, 
    //      prepareRow,
    // } = tableInstance

    return (
        <h1>{Models}</h1>

        // <table {...getTableProps()}>
        //     <thead>
        //         {
        //             headerGroups.map((headerGroup) => (
        //             <tr {...headerGroup.getHeaderGroupProps()} >
        //             {
        //                 headerGroup.headers.map(column => (
        //                     <th {...columns.getHeaderProps}>{column.render('Header')}</th>
        //                 ))
        //             }
        //             </tr>

        //         ))}
                
        //     </thead>
        //     <tbody {...getTableBodyProps()}>
        //         {
        //             rows.map(row => {
        //                 prepareRow(row)
        //                 return (
        //                     <tr {...row.getRowProps()}> 
        //                     {
        //                         row.cells.map((cell) => {
        //                             return <td{...cell.getCellProps()}>{cell.render('Cell')}</td>
        //                         })}
                            
        //                     </tr>
        //                 )
        //             })
        //         }
               
        //     </tbody>
        // </table>
    )
}