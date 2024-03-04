import React from 'react';
import { Link } from 'react-router-dom';

function Nav() {
    return (
        <div className="sidebar">
            <ul>
                <li><Link to="/dashboard/config">Config</Link></li>
                <li><Link to="/dashboard/products">Products</Link></li>
                <li><Link to="/dashboard/payment">Payment</Link></li>
                <li><Link to="/dashboard/tutorial">Tutorial</Link></li>
            </ul>
        </div>
    );
}

export default Nav;
