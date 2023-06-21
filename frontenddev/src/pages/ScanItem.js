import React, { useEffect, useState, useRef } from 'react';
import { useNavigate } from "react-router-dom";
import axios from 'axios';
import Quagga from 'quagga';

import Form from "react-bootstrap/Form";
import Alert from 'react-bootstrap/Alert';
import Container from 'react-bootstrap/esm/Container';
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import FloatingLabel from 'react-bootstrap/esm/FloatingLabel';
import Button from 'react-bootstrap/Button';



export default function ScanItem() {
  const [barcodeData, setBarcodeData] = useState('');
  const [scanActive, setScanActive] = useState(false)
  const [formField, setFormField] = useState('');
  const [responseData, setResponseData] = useState({});
  const [error, setError] = useState('');

  const navigate = useNavigate();
  const videoRef = useRef(null);


  useEffect(() => {
    if (scanActive) {
      Quagga.init(
        {
          inputStream: {
            name: 'Live',
            type: 'LiveStream',
            target: document.querySelector('#barcode-scanner'),
            constraints: {
              width: { max: 500 },
              height: { max: 250 },
              facingMode: 'environment', // or 'user' for front camera
            },
          },
          decoder: {
            readers: ['ean_reader'], // specify the barcode types you want to scan (e.g., EAN)
          },
        },
        (err) => {
          if (err) {
            console.error('Error initializing Quagga:', err);
            return;
          }
          Quagga.start();
        }
      );

      Quagga.onDetected((result) => {
        const barcode = result.codeResult.code;
        console.log('Barcode detected:', barcode);

        setBarcodeData(barcode);
        setFormField(barcode);
      });

      return () => {
        Quagga.stop();
      };
    }
  }, [scanActive]);

  const startScan = () => {
    if (scanActive) {
      setError('Scan is active');
      return;
    }
    setScanActive(true);
  };

  const stopScan = () => {
    setScanActive(false);
  };

  //Once we get the barcode, fetch product data from backend
  const getData = () => {
    axios.get(`http://127.0.0.1:5000/product/scan/${formField}`)
      .then((response) => {
        const responseData = response.data;
        setResponseData(responseData);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  }

  const handleSubmit = (event) => {
    event.preventDefault();

    axios.put(`http://127.0.0.1:5000/updateCart/${formField}`)
      .then((response) => {
        console.log(response);
        const msg = response.data.message;
        navigate("/client", { state: { msg } });
      })
      .catch((error) => {
        setError(error.response.data.message);
      });
  };

  return (
    <div className='background'>
      {error && <Alert variant="danger">{error}</Alert>}
      <Container>
        <Row>
          <Col sm={7}>
            <div className="barcode-scanner">
              <div id="barcode-scanner" style={{ width: '100%', height: '100%' }} ref={videoRef} />
            </div>
            <div className="position-absolute alignitems-center bottom-0">
              <Row className="mt-3">
                <Button variant="success" onClick={startScan}>Start Scan</Button>
                <Button variant="danger" onClick={stopScan}>Close Scan</Button>
              </Row>
            </div>
          </Col>
          <Col sm={5}>
              <FloatingLabel controlId="formbarcode" label="Barcode" className="mb-3">
                <Form.Control
                  type="number"
                  placeholder="Barcode"
                  value={formField}
                  onChange={(e) => {
                    setFormField(e.target.value);
                    getData();
                  }}
                />
              </FloatingLabel>
            {responseData &&
              <div>
                <Row>
                  <Col> {responseData.name} </Col>
                </Row>
                <Row>
                  <Col> {responseData.price} </Col>
                </Row>
                <Row>
                  <Col><Button href="/client">Just checking</Button></Col>
                  <Col><Button onClick={handleSubmit}>Add to cart</Button></Col>
                  <Col><Button href="/checkout">Checkout</Button></Col>
                </Row>
                <Row>
                  <Col><Button variant="success" onClick={startScan}>Start Scan</Button></Col>
                  <Col><Button variant="danger" onClick={stopScan}>Close Scan</Button></Col>
                </Row>
              </div>}
          </Col>
          </Row>
      </Container>
    </div>
  );
}
