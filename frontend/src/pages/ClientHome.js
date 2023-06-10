//This contains code for the landing page of the web application
import React, { } from "react";
 
import {Link} from 'react-router-dom';
 
export default function HomePage(){
 
  return (
    <div>
        <div className="container h-100">
            <div className="row h-100">
                <div className="col-12">
                    <h1>Welcome to Jabali supermarket</h1>
                    <p><Link to="/login" className="btn btn-success">Scan</Link></p>
                </div>
            </div>
        </div>
    </div>
  );
}
