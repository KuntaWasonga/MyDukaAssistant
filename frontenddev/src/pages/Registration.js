//This contains code for the register account page of the web application
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Alert from 'react-bootstrap/Alert';

import "./stylesheets/registration.css";



export default function RegistrationPage() {

  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const navigate = useNavigate();

  const handleSubmit = (event) => {
    event.preventDefault();

    axios.post('http://127.0.0.1:5000/user/register', {
      "firstname": firstName,
      "lastname": lastName,
      "email": email,
      "password": password,
    })
      .then((response) => {
        console.log(response);
        const msg = response.data.message;
        navigate("/", { state: { msg } });
        setFirstName('');
        setLastName('');
        setPassword('');
        setError('');
      })
      .catch((error) => {
        setError(error.response.data.error);
      });
  }

  return (
    <div>
      <div className="alert-container">
        {error && (
          <Alert variant="danger" className="custom-alert">
            {error}
          </Alert>
        )}
      </div>
      <Container fluid>
        <Row>
          <Col sm={5}>
            
          </Col>
          <Col sm={7}>
            <div className="reg-container">
              <Form>
                <Row className="mb-3">
                  <Col>
                    <Form.Label>First name</Form.Label>
                    <Form.Control placeholder="First name"
                      value={firstName}
                      onChange={(e) => setFirstName(e.target.value)} />
                  </Col>
                  <Col>
                    <Form.Label>Last name</Form.Label>
                    <Form.Control placeholder="Last name"
                      value={lastName}
                      onChange={(e) => setLastName(e.target.value)} />
                  </Col>
                </Row>
                <Form.Group className="mb-3" controlId="formGroupEmail">
                  <Form.Label>Email address</Form.Label>
                  <Form.Control type="email" placeholder="Enter email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)} />
                </Form.Group>
                <Form.Group className="mb-3" controlId="formGroupPassword">
                  <Form.Label>Password</Form.Label>
                  <Form.Control type="password" placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)} />
                </Form.Group>
                <Button variant="primary" onClick={handleSubmit}>Submit</Button>
                <Button variant="secondary" href="/">Close</Button>
              </Form>
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  );
}
