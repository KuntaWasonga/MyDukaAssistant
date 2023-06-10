//This contains code for the landing page of the web application
import React, { } from "react";
 
import {Link} from 'react-router-dom';
 
export default function HomePage(){
  let y = 22;

  if (window.location.pathname === "/login") {
    y += 1;
  } else {
    y -=1;
  }
 
  return (
    <div>
        <div className="container h-100">
            <div className="row h-100">
                <div className="col-12">
                    <h1>Welcome to Jabali supermarket {y}</h1>
                    <p><Link to="/login" className="btn btn-success">Scan</Link> | <Link to="/register" className="btn btn-success">register</Link> </p>
                </div>
            </div>
        </div>
    </div>
  );
}