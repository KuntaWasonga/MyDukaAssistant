//This contains code for the landing page of the web application
import React, { } from "react";

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
 
//import {Link} from 'react-router-dom';
 
export default function LoginPage(){

  //This is a form that should pop up on the 
  //Check if user in employee or client database.
  //Check for the necessary password with the hash key.
  //If employee, go to employee home page.
  //If client, go to client home page.

  return (
    <Container>
      <Row>
        <Col sm={5}>
          image
        </Col>
        <Col sm={7}>
          loginform
        </Col>
      </Row>
    </Container>
  );
}