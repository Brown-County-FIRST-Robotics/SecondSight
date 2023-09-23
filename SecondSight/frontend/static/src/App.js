import './App.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from './pages';
import Info from './pages/info';
import Color from './pages/color';
import Config from './pages/config';

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/info" element={<Info />} />
        <Route path="/color" element={<Color />} />
        <Route path="/config" element={<Config />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;


