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



export default function RegistrationPageE() {

  const [employeeID, setemployeeID] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const navigate = useNavigate();

  const handleSubmit = async (event) => {

    axios.post('http://127.0.0.1:5000/employee/register', {
      "employeeID": employeeID,
      "email": email,
      "password": password,
    })
      .then((response) => {
        console.log(response);
        const msg = response["message"];
        navigate("/", { state: { msg } });
        // Reset the form input values and clear any previous errors
        setemployeeID('');
        setPassword('');
        setError('');
      })
      .catch((error) => {
        // Handle the error response from the backend
        setError(error.message);
      });
  }

  return (
    <div>
      <Container fluid>
        <Row>
          <Col sm={5}>
            image
          </Col>
          <Col sm={7}>
            <div className="reg-container">
              <Form onSubmit={handleSubmit}>
                {error && <Alert variant="danger">{error}</Alert>}
                <Row className="mb-3">
                    <Form.Label>employeeID</Form.Label>
                    <Form.Control placeholder="EmployeeID"
                      value={employeeID}
                      onChange={(e) => setemployeeID(e.target.value)} />
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
                <Button type="submit">Submit</Button>
              </Form>
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  );
}
