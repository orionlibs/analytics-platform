import React, { useState} from "react";
import { css } from "@emotion/css";

import { fetchLastLocation } from "./backend/fetchLastLocations";

// This is an example results data structure
const results:any = [
  {
    timestamp: Date.now(),
    address: {
      street: "5th Ave",
      city: "Random City"
    },
    executionTime: 900
  },
  {
    timestamp: Date.now() + 2000,
    address: {
      street: "Main Road",
      city: "New Town"
    },
    executionTime: 400
  }
];
const getStyles = () => ({
  button: css`
    border: 1px solid black;
    background: transparent;
    padding: 5px;
  `,
  container: css`
    margin: 10px;
  `
});

function App() {
  const [response, setResponse] = useState(results);

  const handleOnClick = async () => {
    const timestamp = Date.now();

    await fetchLastLocation().then(res => {
      setResponse({timestamp, ...res})
    })

  };

  const s = getStyles()
  return (
    <div className={s.container}>
      <button className={s.button} onClick={() => handleOnClick()}>Get Last Location</button>
      <table>
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>Street</th>
            <th>City</th>
            <th>Execution Time (ms)</th>
          </tr>
        </thead>
        <tbody>
            <tr>
              <td>{response.timestamp}</td>
              <td>{response?.address?.street}</td>
              <td>{response?.address?.city}</td>
              <td></td>
            </tr>
        </tbody>
      </table>
      <div>
        <div>Fastest:  ms </div>
        <div>Slowest:  ms </div>
        <div>Average:  ms </div>
      </div>
    </div>
  );
}

export default App;
