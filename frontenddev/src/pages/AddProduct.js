//So one can choose to either key in the bar code manually or do the scan.
import React, { useEffect, useState, useRef } from 'react';
import { useNavigate } from "react-router-dom";
import axios from 'axios';
import Quagga from 'quagga';

import Form from "react-bootstrap/Form";
import Alert from 'react-bootstrap/Alert';
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import FloatingLabel from 'react-bootstrap/FloatingLabel';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';

import "./stylesheets/scan.css";



export default function AddProduct() {
    const [barcodeData, setBarcodeData] = useState('');
    const [scanActive, setScanActive] = useState(false);
    const [id, setid] = useState('');
    const [pname, setPname] = useState('');
    const [price, setPrice] = useState('');
    const [formField, setFormField] = useState('');
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
                        target: videoRef.current,
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
        Quagga.stop();
        if (videoRef.current && videoRef.current.srcObject) {
            videoRef.current.srcObject = null;
        }
    };


    const handleSubmit = (event) => {
        event.preventDefault();

        axios.post('http://127.0.0.1:5000/product/add', {
            "id": id,
            "barcode": formField,
            "name": pname,
            "price": price,
        })
            .then((response) => {
                console.log(response);
                const msg = response.data.message;
                navigate("/employee", { state: { msg } });
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
                        <FloatingLabel controlId="formId" label="id" className="mb-3">
                            <Form.Control
                                type="number"
                                placeholder="formId"
                                value={id}
                                onChange={(e) => {
                                    setid(e.target.value);
                                }}
                            />
                        </FloatingLabel>
                        <FloatingLabel controlId="formbarcode" label="Product barcode" className="mb-3">
                            <Form.Control
                                type="number"
                                placeholder="67022900"
                                value={formField}
                                onChange={(e) => {
                                    setFormField(e.target.value);
                                }}
                            />
                        </FloatingLabel>
                        <FloatingLabel controlId="formProductname" label="Product name" className="mb-3">
                            <Form.Control
                                type="text"
                                placeholder="Chips"
                                value={pname}
                                onChange={(e) => {
                                    setPname(e.target.value);
                                }}
                            />
                        </FloatingLabel>
                        <FloatingLabel htmlFor="formProductprice" label="Product price (KES)" className="mb-3">
                            <Form.Control
                                type="number"
                                placeholder="120"
                                value={price}
                                onChange={(e) => {
                                    setPrice(e.target.value);
                                }}
                            />
                        </FloatingLabel>
                        <Row>
                            <Button variant="primary" onClick={handleSubmit}>
                                Add product
                            </Button>
                        </Row>
                        <Row></Row>
                        <Row>
                            <Button variant="secondary" href="/employee">
                                Cancel
                            </Button>
                        </Row>
                    </Col>
                </Row>
            </Container>
        </div>
    );
}
