import React from 'react';
import './Dashboard.css';
import Nav from './Nav'; 

function Dashboard() {
    return (
        <div className="container">
            <Nav />
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
