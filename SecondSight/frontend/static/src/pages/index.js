import React, { useEffect, useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import axios from 'axios';

const Home = () => {

  const [isLoading, setLoading] = useState(true);
  const [configRequired, setConfig] = useState();

  useEffect(() => {
    axios.get('http://localhost:8000/config').then(response => {
      console.log("SUCCESS", response);
      setConfig(response.data["config_required"]);
      setLoading(false);
    }).catch(error => {
      console.log(error)
    })
  }, []);

  if (isLoading) {
    return <div className="App">Loading...</div>
  }

  if (configRequired) {
    return (
      <Navigate replace to="/config" />
    );
  }

  return (
    <h1>This is the default page</h1>
  );
};

export default Home;

