// Dashboard.js
import React, { useState } from 'react';
import { Link } from 'react-router-dom'; // Import Link from React Router
import './Dashboard.css';

function Dashboard() {
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);

    const toggleSidebar = () => {
        setIsSidebarOpen(!isSidebarOpen);
    };

    return (
        <div className="container">
            <div className={`sidebar ${isSidebarOpen ? 'open' : ''}`}>
                <ul>
                    <li><Link to="./config">Config</Link></li>
                    <li><Link to="./products">Products</Link></li>
                    <li><Link to="./payment">Payment</Link></li>
                    <li><Link to="./tutorial">Tutorial</Link></li>
                </ul>
            </div>
            <div className="main-content">
                <button className="sidebar-toggle" onClick={toggleSidebar}>
                    {isSidebarOpen ? 'Close Sidebar' : 'Open Sidebar'}
                </button>
                <div className="users">
                    <h2 className="usersh2">Users</h2>
                </div>
                <div className="orders">
                    <h2 className="ordersh2">Orders</h2>
                </div>
            </div>
        </div>
    );
}

export default Dashboard;

