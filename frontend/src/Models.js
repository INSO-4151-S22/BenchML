import React, { useEffect, useState } from "react";

const ModelsContext = React.createContext({
  models: [], fetchModels: () => {}
})
export default function Models(){
  const [models, setModels] = useState([])
    const fetchModels = async () => {
      const response = await fetch("http://localhost:8000/")
      const models = await response.json()
      setModels(models.data)
    }

  useEffect(() => {
    fetchModels()
  }, [])
  return (
    models
  )
} 

