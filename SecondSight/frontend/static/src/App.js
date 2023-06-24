import logo from './logo.svg';
import './App.css';
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const App = () => {
  const [hue, setHue] = useState(0);
  const [saturation, setSaturation] = useState(0);
  const [value, setValue] = useState(0);

  const handleHueChange = (event) => {
    setHue(event.target.value);
    const post_data = { cube_hsv: [parseInt(hue, 10), parseInt(saturation, 10), parseInt(value, 10)] };
    axios.post('http://localhost:8000/config', post_data)
        .then(response => { console.log("POST", response)});
  };

  const handleSaturationChange = (event) => {
    setSaturation(event.target.value);
    const post_data = { cube_hsv: [parseInt(hue, 10), parseInt(saturation, 10), parseInt(value, 10)] };
    axios.post('http://localhost:8000/config', post_data)
        .then(response => { console.log("POST", response)});
  };

  const handleValueChange = (event) => {
    setValue(event.target.value);
    const post_data = { cube_hsv: [parseInt(hue, 10), parseInt(saturation, 10), parseInt(value, 10)] };
    axios.post('http://localhost:8000/config', post_data)
        .then(response => { console.log("POST", response)});
  };

  useEffect(()=>{
    axios.get('http://localhost:8000/config/cube_hsv').then(response => {
      console.log("SUCCESS", response)
      setHue(response.data[0])
      setSaturation(response.data[1])
      setValue(response.data[2])
    }).catch(error => {
      console.log(error)
    })

  }, [])

  return (
    <div>
      <div>
        <h3>Live Streaming</h3>
        <img style={{ width: 640, height: 480 }} src="http://localhost:8000/preview_image" width="100%">
        </img>
      </div>
      <div>
        <label htmlFor="hueSlider">Hue</label>
        <input
          type="range"
          id="hueSlider"
          min={0}
          max={255}
          value={hue}
          onChange={handleHueChange}
        />
        <span>{hue}</span>
      </div>
      <div>
        <label htmlFor="saturationSlider">Saturation</label>
        <input
          type="range"
          id="saturationSlider"
          min={0}
          max={255}
          value={saturation}
          onChange={handleSaturationChange}
        />
        <span>{saturation}</span>
      </div>
      <div>
        <label htmlFor="valueSlider">Value</label>
        <input
          type="range"
          id="valueSlider"
          min={0}
          max={255}
          value={value}
          onChange={handleValueChange}
        />
        <span>{value}</span>
      </div>
    </div>
  );
};

export default App;

