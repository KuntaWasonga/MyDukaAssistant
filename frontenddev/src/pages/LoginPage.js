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

import "./stylesheets/login.css";
import FloatingLabel from "react-bootstrap/esm/FloatingLabel";



export default function LoginPage() {

  const [userName, setuserName] = useState('');
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

    axios.post('http://127.0.0.1:5000/user/login', {
      "username": userName,
      "password": password
    })
      .then((response) => {
        console.log(response);
        const msg = response["message"]
        navigate("/client", { state: { msg } });
      })
      .catch((error) => {
        setError(error.response.data.message);
      });
  }

  return (
    <div className="box">
      <Modal show={show} onHide={handleClose} className="custom-modal">
        <Modal.Header closeButton>
          <Modal.Title>LOGIN</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Row>
              <Col>
                <FloatingLabel controlId="formUsername" label="Username"
                  className="mb-3">
                  <Form.Control
                    type="text"
                    placeholder="Enter username"
                    value={userName}
                    onChange={(e) => setuserName(e.target.value)}
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
      {error && <Alert variant="danger" className="custom-alert">
        {error}
      </Alert>}
    </div>
  );
}
