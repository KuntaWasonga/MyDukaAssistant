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

//import { Link } from 'react-router-dom';
export default function LoginPage() {

  const [userName, setuserName] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  //Handle the modal element
  const [show, setShow] = useState(true);
  const handleShow = () => setShow(true);

  const navigate = useNavigate();

  const handleClose = () => {
    onClose();
    setShow(false);
    navigate(-1); // Navigate back to the previous page
  };

  const handleSubmit = async (event) => {

    axios.post('http://127.0.0.1:5000/login', {
      "username": userName,
      "password": password
    })
      .then((response) => {
        console.log(response);
        const msg = response["message"]
        navigate("/", { state: { msg } });
      })
      .catch((error) => {
        // Handle the error response from the backend
        setError(error.message);
      });
  }

  return (
    <>
      <Modal show={show} onHide={handleClose} className="custom-modal">
        <Modal.Header closeButton>
          <Modal.Title>LOGIN</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            {error && <Alert variant="danger">{error}</Alert>}
            <Row>
              <Col>
                <Form.Group controlId="formUsername">
                  <Form.Label>Username</Form.Label>
                  <Form.Control
                    type="text"
                    placeholder="Enter username"
                    value={userName}
                    onChange={(e) => setuserName(e.target.value)}
                  />
                </Form.Group>
              </Col>
            </Row>
            <Row>
              <Col>
                <Form.Group controlId="formPassword">
                  <Form.Label>Password</Form.Label>
                  <Form.Control
                    type="password"
                    placeholder="Enter password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                </Form.Group>
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
    </>
  );
}
