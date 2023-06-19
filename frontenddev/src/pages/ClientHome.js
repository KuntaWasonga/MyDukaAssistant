//This contains code for a user page of the web application
import React, { useState } from "react";
import { useLocation, useNavigate } from 'react-router-dom';
import axios from "axios";

import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";
import Container from "react-bootstrap/esm/Container";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import Button from "react-bootstrap/Button";

import "./stylesheets/employee.css";

export default function EmployeeHome() {

  const location = useLocation();
  const alertMessage = location.state?.alertMessage;

  const navigate = useNavigate();

  const [error, setError] = useState('');

  const logout = () => {
    axios.post('http://127.0.0.1:5000/user/logout', {
    })
      .then((response) => {
        console.log(response);
        const msg = response["message"]
        navigate("/", { state: { msg } });
      })
      .catch((error) => {
        setError(error.message);
      });
  }


  return (
    <div className="box">
      <Navbar expand="lg" bg="grey" variant="light">
        <Container>
          <Navbar.Brand href="/">M-Duka</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="ms-auto pe-3">
              <Nav.Link href="/">Profile</Nav.Link>
              <Nav.Link href="/about">About</Nav.Link>
              <Nav.Link href="/logout" onClick={logout}>Logout</Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      {alertMessage && <div className="alert">{alertMessage}</div>}
      <div className="karibu">
        <h1 className="message">Welcome to Jabali</h1>
      </div>
      <Row className="justify-content-md-center">
        <Col xs lg="2"><Button className="check" href="/scan">
          SCAN ITEM
        </Button>
        </Col>
        <Col md = "auto"></Col>
        <Col xs lg = "2">
        <Button className="add" href="/add">
          
        </Button>
        </Col>
      </Row>
    </div>
  );
}
