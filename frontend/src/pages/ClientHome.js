//This contains code for the client page of the web application
import React, { } from "react";

import { Link } from 'react-router-dom';

import "./stylesheets/home.css";

export default function ClientHome() {

  //Check for the name of client htat has logged in.
  let client = "Kunta";

  //The "LOGIN" anchor is just a place holder 
  // but should not have any color on the page.
  
  return (
    <div>
      <div className="bg-img">
        <div className="container">
          <div className="top-nav">
            <a href="#home">HOME</a>
            <a href="#about">ABOUT</a>
            <a href="#contact">CONTACT</a>
            <a href="#contact">LOGIN</a>
          </div>
          <div className="content">
            <h1>Welcome {client} to Jabali supermarket</h1>
            <p>Start your shopping experience below</p>
          </div>
          <div className="button">
            <button><Link to = "/scan">SCAN</Link></button>
          </div>
        </div>
      </div>
    </div>
  );
}