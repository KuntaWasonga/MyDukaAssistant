import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

import {BrowserRouter, Route, Routes} from 'react-router-dom';

import HomePage from "./pages/HomePage";
import ClientHome from "./pages/ClientHome";
import ScanItem from "./pages/ScanItem";
import ViewCart from "./pages/ViewCart";
import EmployeeHome from "./pages/EmployeeHome";
import CheckCustomer from "./pages/CheckCustomer";
import AddProduct from "./pages/AddProduct";
import LoginPage from "./pages/LoginPage";
import RegistrationPage from './pages/Registration';

function App() {
  return (
    <div className="App">
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/client" element={<ClientHome />} />
            <Route path="/scan" element={<ScanItem />} />
            <Route path="/cart" element={<ViewCart />} />
            <Route path="/employee" element={<EmployeeHome />} />
            <Route path="/check" element={<CheckCustomer />} />
            <Route path="/add" element={<AddProduct />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegistrationPage />} />
          </Routes>
        </BrowserRouter>
    </div>
  );
}

export default App;
