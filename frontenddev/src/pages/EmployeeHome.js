//This contains code for the client page of the web application
import React, { } from "react";

import { Link } from 'react-router-dom';

import "./stylesheets/home.css";

export default function ClientHome() {

  let employee = "Kunta";

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
            <h1>Welcome {employee} to Jabali supermarket</h1>
            <p>Start your shopping experience below</p>
          </div>
          <div className="button">
            <button><Link to = "/check">CHECK CUSTOMER</Link></button>
            <button><Link to = "/add">ADD PRODUCT</Link></button>
          </div>
        </div>
      </div>
    </div>
  );
}