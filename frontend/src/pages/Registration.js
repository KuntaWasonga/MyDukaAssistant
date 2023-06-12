//This contains code for the register account page of the web application
import React, { } from "react";

import { Link } from 'react-router-dom';

export default function LoginPage() {

	//Add a check: client | employee.
	//Employee: If so, add text box for their ID. If invalid, mention as so once they submit.
	//Client: If so, check if account was created successfully then use success().

	return (
		<div>
			<div className="bg-img">
				<Link to="/login"><input type="button" onclick="success();" value="submit" /> </Link>
			</div>
			<script>
				function success() {
					alert("Your account was created successfully")
				};
			</script>
		</div>
	);
}