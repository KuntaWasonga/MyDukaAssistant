//This contains code for the register account page of the web application
import React, { } from "react";

import { Link } from 'react-router-dom';

export default function RegistrationPage() {

	//Add a check: client | employee.
	//Employee: If so, add text box for their ID. If invalid, mention as so once they submit.
	//Client: If so, check if account was created successfully then use success().

	return (
		<div>
			<form action="registration" style="border:1px solid #ccc">
				<div className="container">
					<h1>SIGN UP</h1>
					<p>Kindly fill this to create an account</p>

					<hr>
					<label><b>E-mail</b></label>
					<input type="text" placeholder="Enter e-mail address"
					name="email" required/>

					<label><b>Password</b></label>
					<input type="text" placeholder="Enter a password"
					name="password" required/>

					<label><b>E-mail</b></label>
					<input type="text" placeholder="Repeat password"
					name="rpassword" required/>

					<label>
						<input type="checkbox" checked="checked"
						name="remember" style="margin-bottom:15px"/>
					</label>

					<p>By creating an account you agree to our
						<a href="#terms" style="color:dodgerblue">Terms & Privacy</a>
					</p>

					<div>
						<button type="button" class="cancelbtn"></button>
						<button type="submit" class="signupbtn"></button>
					</div>
					</hr>
				</div>
			</form>
		</div>
	);
}