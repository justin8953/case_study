import React from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";
import {Home} from './Home';
import {Dashboard} from './Dashboard';
import './App.css';

function App() {
  return (
    <Router>
        <Route path="/" exact component={Home} />
        <Route path="/dashboard" component={Dashboard} />
      </Router>
  );
}

export default App;
