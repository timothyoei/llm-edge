import React from 'react';
import ReactDOM from 'react-dom/client';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

import './index.css';
import App from './App';
import Signup from './Components/Signup';
import Home from './Components/Home';

const router = createBrowserRouter([
  {
    path: "/",
    element: <App/>,
  },
  {
    path: "signup",
    element: <Signup/>,
  },
  {
    path: "home",
    element: <Home />
  }
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <RouterProvider router= {router}/>
);