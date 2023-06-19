//This contains code for the landing page of the web application
import React, { useState } from "react";
import { useLocation } from 'react-router-dom';

import Navbar from "react-bootstrap/Navbar";
import NavDropdown from "react-bootstrap/NavDropdown";
import Nav from "react-bootstrap/Nav";
import Container from "react-bootstrap/esm/Container";

import "./stylesheets/home.css";

import LoginPage from "./LoginPage";

export default function HomePage() {
  const [showLoginModal, setShowLoginModal] = useState(false);

  const handleOpenLoginModal = () => {
    setShowLoginModal(true);
  }
  const handleCloseLoginModal = () => {
    setShowLoginModal(false);
  }

  const location = useLocation();

  const alertMessage = location.state?.alertMessage;

  { alertMessage && <div className="alert">{alertMessage}</div> }
  return (
    <div className="box">
      <Navbar expand="lg" bg="grey" variant="light">
      <Container>
        <Navbar.Brand href="#home">M-Duka</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ms-auto pe-3">
            <Nav.Link href="#home">Home</Nav.Link>
            <Nav.Link href="#about">About</Nav.Link>
            <NavDropdown title="Register" id="register-nav-dropdown">
              <NavDropdown.Item href="#shopper">Shopper</NavDropdown.Item>
              <NavDropdown.Item href="#employee">Employee</NavDropdown.Item>
            </NavDropdown>
            <NavDropdown title="Login" id="login-nav-dropdown">
              <NavDropdown.Item href="###" onClick={handleOpenLoginModal}>Shopper</NavDropdown.Item>
              <NavDropdown.Item href="#employee">Employee</NavDropdown.Item>
            </NavDropdown>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
      { alertMessage && <div className="alert">{alertMessage}</div> }
      <div className="karibu">
      <h1 className="message">Welcome to Jabali</h1>
      </div>
      {showLoginModal && (
      <LoginPage show={showLoginModal} onClose={handleCloseLoginModal} />
      )}
    </div>
  );
}