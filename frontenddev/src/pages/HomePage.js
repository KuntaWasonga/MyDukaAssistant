//This contains code for the landing page of the web application
import React, { } from "react";
import { useLocation } from 'react-router-dom';

import Navbar from "react-bootstrap/Navbar";
import NavDropdown from "react-bootstrap/NavDropdown";
import Nav from "react-bootstrap/Nav";
import Container from "react-bootstrap/esm/Container";

import "./stylesheets/home.css";



export default function HomePage() {

  const location = useLocation();
  const alertMessage = location.state?.alertMessage;


  return (
    <div className="box">
      <Navbar expand="lg" bg="grey" variant="light">
        <Container>
          <Navbar.Brand href="/">M-Duka</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="ms-auto pe-3">
              <Nav.Link href="/">Home</Nav.Link>
              <Nav.Link href="#about">About</Nav.Link>
              <NavDropdown title="Register" id="register-nav-dropdown">
                <NavDropdown.Item href="/register">Shopper</NavDropdown.Item>
                <NavDropdown.Item href="/registerE">Employee</NavDropdown.Item>
              </NavDropdown>
              <NavDropdown title="Login" id="login-nav-dropdown">
                <NavDropdown.Item href="/login" >Shopper</NavDropdown.Item>
                <NavDropdown.Item href="/loginE">Employee</NavDropdown.Item>
              </NavDropdown>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      {alertMessage && <div className="alert">{alertMessage}</div>}
      <div className="karibu">
        <h1 className="message">Welcome to Jabali</h1>
      </div>
    </div>
  );
}
