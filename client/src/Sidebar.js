import React from 'react';
import { Link } from 'react-router-dom';

function Sidebar() {
  return (
    <div className="sidebar">
      <ul>
        <li>
          <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/analytics">Analytics</Link>
        </li>
      </ul>
    </div>
  );
}

export default Sidebar;
