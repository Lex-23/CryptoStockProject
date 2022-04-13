import React, { Component } from "react";
import authHeader from "../../services/auth-header";

import axios from "axios";

const user = JSON.parse(localStorage.getItem("user"));

class HomePage extends React.Component {
    render() {
      return <h1>Hello, React</h1>;
    }
  }

export default HomePage;
