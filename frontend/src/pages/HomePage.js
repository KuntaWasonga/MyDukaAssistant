//This contains code for the landing page of the web application
import React, { } from "react";
 
import {Link} from 'react-router-dom';

import "./stylesheets/home.css";
 
export default function HomePage(){
 
  return (
    <div>
        <div className="bg-img">
          <div className="container">
            <div className="top-nav">
              <a href="#home">HOME</a>
              <a href="#news">ABOUT</a>
              <a href="#contact">CONTACT</a>
              <div class="dropdown">
                <button class="dropbtn">LOGIN</button>
                <div class="dropdown-content">
                  <a href='login'><Link to="/login">Client</Link></a>
                  <a href='login'><Link to="/login">Employee</Link></a>
                </div>
              </div>
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
