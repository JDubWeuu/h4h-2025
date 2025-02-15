import React from "react";
import "./Navbar.css"; 

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <h1>Visionary</h1>
      </div>

      <ul className="navbar-links">
        <li><a href="#home">who are we?</a></li>
        <li><a href="#about">about</a></li>
      </ul>
    </nav>
  );
};

export default Navbar;
