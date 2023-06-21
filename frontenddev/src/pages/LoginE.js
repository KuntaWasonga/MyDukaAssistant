//This contains code for the login page of the web application
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from 'axios';

//import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Alert from 'react-bootstrap/Alert';
import FloatingLabel from "react-bootstrap/esm/FloatingLabel";

import "./stylesheets/login.css";



export default function LoginPageE() {

  const [employeeID, setemployeeID] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  //Handle the modal element
  const [show, setShow] = useState(true);

  const navigate = useNavigate();

  const handleClose = () => {
    setShow(false);
    navigate("/");
  };

  const handleSubmit = (event) => {

    axios.post('http://127.0.0.1:5000/employee/login', {
      "employee_id": employeeID,
      "password": password
    })
      .then((response) => {
        console.log(response);
        const msg = response.data.message;
        navigate("/employee", { state: { msg } });
      })
      .catch((error) => {
        setError(error.response.error);
      });
  }

  return (
    <div className="box">
      {error && <Alert variant="danger">{error}</Alert>}
      <Modal show={show} onHide={handleClose} className="custom-modal">
        <Modal.Header closeButton>
          <Modal.Title>LOGIN</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Row>
              <Col>
                <FloatingLabel controlId="formUsername" label="EmployeeID"
                  className="mb-3">
                  <Form.Control
                    type="number"
                    placeholder="Enter employeeID"
                    value={employeeID}
                    onChange={(e) => setemployeeID(e.target.value)}
                  />
                </FloatingLabel>
              </Col>
            </Row>
            <Row>
              <Col>
                <FloatingLabel controlId="formPassword"
                  label="Password">
                  <Form.Control
                    type="password"
                    placeholder="Enter password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                </FloatingLabel>
              </Col>
            </Row>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Close
          </Button>
          <Button variant="primary" onClick={handleSubmit}>
            Login
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
}
