import logo from './logo.svg';
import './App.css';

import {BrowserRouter, Routes, Route} from 'react-router-dom';

import HomePage from "./pages/HomePage";
import ClientHome from "./pages/ClientHome";
import ScanItem from "./pages/ScanItem";
import ViewCart from "./pages/ViewCart";
import EmployeeHome from "./pages/EmployeeHome";
import CheckCustomer from "./pages/CheckCustomer";
import AddProduct from "./pages/AddProduct";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
      </header>
      <div className="container">
        <BrowserRouter>
          <Route path="/" element={<HomePage />} />
          <Route path="/client" element={<ClientHome />} />
          <Route path="/scan" element={<ScanItem />} />
          <Route path="/cart" element={<ViewCart />} />
          <Route path="/employee" element={<EmployeeHome />} />
          <Route path="/check" element={<CheckCustomer />} />
          <Route path="/client" element={<AddProduct />} />
        </BrowserRouter>
      </div>
    </div>
  );
}

export default App;
