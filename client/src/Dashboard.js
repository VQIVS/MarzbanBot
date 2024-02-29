import React from 'react';
import './Dashboard.css';
import { Link } from 'react-router-dom';

function Dashboard() {
    return (
        <div className="container">
            <div className="sidebar">
                <ul>
                    <li><Link to="/dashboard/config">Config</Link></li>
                    <li><Link to="/dashboard/products">Products</Link></li>
                    <li><Link to="/dashboard/payment">Payment</Link></li>
                    <li><Link to="/dashboard/tutorial">Tutorial</Link></li>
                </ul>
            </div>
            <div className="main-content">
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
