 import React, { useEffect, useState } from "react";
 import axios from 'axios';


 export default class Models extends React.Component {
   state = {
     models: []
   }
   componentGetModels() {
     axios.get('http://localhost:800/models').then(res => {
       const models = res.data;
       this.setState({ models });
     })
   }
 }

// export default function Models(){
//   const [models, setModels] = useState([])
//     const fetchModels = async () => {
//       const response = await fetch("http://localhost:8000/")
//       const models = await response.json()
//       setModels(models.data)
//     }

//   useEffect(() => {
//     fetchModels()
//   }, [])
//   return (
//     models
//   )
// } 

