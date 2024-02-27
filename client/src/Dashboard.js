import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Sidebar from './Sidebar';
import MainContent from './MainContent';
import './Dashboard.css';

function Dashboard() {
  return (
    <Router>
      <div className="dashboard">
        <Sidebar />
        <Routes>
          <Route path="/" exact component={Home} />
          <Route path="/analytics" component={Analytics} />
        </Routes>
      </div>
    </Router>
  );
}

function Home() {
  return <MainContent title="Home" />;
}

function Analytics() {
  return <MainContent title="Analytics" />;
}

export default Dashboard;
