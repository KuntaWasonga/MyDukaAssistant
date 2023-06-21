//Be a modal table with

//BUTTON: CHECKOUT, JUST CHECKING

//This contains code for the login page of the web application
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from 'axios';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import Alert from 'react-bootstrap/Alert';
import Table from 'react-bootstrap/Table';

import "./stylesheets/login.css";

export default function ViewCart() {
  const [show, setShow] = useState(true);
  const [data, setData] = useState([]);
  const [total, setTotal] = useState('')
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleClose = () => {
    setShow(false);
    navigate("/client");
  };

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = () => {
    axios.get('http://127.0.0.1:5000/viewcart')
      .then((response) => {
        setData(response.data.Items);
        setTotal(response.data.TOTAL);
      })
      .catch((error) => {
        setError('Error retrieving data from the backend.');
      });
  }

  return (
    <div className="box">
      <Modal show={show} onHide={handleClose} className="custom-modal">
        <Modal.Header closeButton>
          <Modal.Title>YOUR CART</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {error ? (
            <Alert variant="danger" className="custom-alert">
              {error}
            </Alert>
          ) : (
            <Table striped bordered hover>
              <thead>
                <tr>
                  <th>Product</th>
                  <th>Quantity</th>
                  <th>Price</th>
                  <th>Total</th>
                </tr>
              </thead>
              <tbody>
                {data.map((item, index) => (
                  <tr key={index}>
                    <td>{item.product}</td>
                    <td>{item.quantity}</td>
                    <td>{item.price}</td>
                    <td>{item.Total}</td>
                  </tr>))}
                  <tr>
                    <td colSpan={3}>TOTAL</td>
                    <td>{total}</td>
                  </tr>
              </tbody>
            </Table>
          )}
        </Modal.Body>
        <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
            Just
          </Button>
          <Button variant="primary" href="/checkout">
            Check Out
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
}
