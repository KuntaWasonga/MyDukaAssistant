//This contains code for the landing page of the web application
import React, { } from "react";

import { Link } from 'react-router-dom';

import "./stylesheets/home.css";

export default function HomePage() {

  return (
    <div>
      <div className="bg-img">
        <div className="container">
          <div className="top-nav">
            <a href="#home">HOME</a>
            <a href="#about">ABOUT</a>
            <a href="#contact">CONTACT</a>
            <a href="#login"><Link to ="/login">LOGIN</Link></a>
          </div>
          <div className="content">
            <h1>Welcome to Jabali supermarket</h1>
            <p>Your physical shopping assistant</p>
          </div>
        </div>
      </div>
    </div>
  );
}