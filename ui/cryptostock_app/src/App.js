import axiosInstance from "./axiosApi";
import React from "react";
import Login from "./components/login";
import AuthPing from "./components/authPing";
import { Route, Switch, Redirect, Link } from "react-router-dom";
import HomePage from "./pages/home";
import SalesDashboardList from "./pages/salesDashboardList";

class App extends React.Component {

  constructor() {
    super();
    this.handleLogout = this.handleLogout.bind(this);
  }

  async handleLogout() {
    try {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        axiosInstance.defaults.headers['Authorization'] = null;
    }
    catch (e) {
        console.log(e);
    }
  };

  render() {
    return (
      <div className="app">
        <h1>CryptostockProject TEST</h1>
        <nav>
            <Link className="nav-link" to="/">Home</Link>
            <Link className="nav-link" to="/login/">Login</Link>
            <Link className="nav-link" to="/salesdashboard/">Allow sales</Link>
            <Link className="nav-link" to="/auth-ping/">AuthPing</Link>
            <button onClick={this.handleLogout} render={<h2>Logged out</h2>}>Logout</button>
        </nav>
        <main className="main">
          <Switch>
            <Route exact path="/login/" component={Login} />
            <Route exact path="/auth-ping/" component={AuthPing} />
            <Route exact path="/salesdashboard/" component={SalesDashboardList} />
            <Route path="/" component={HomePage} />
            <Redirect to="/" />
          </Switch>
        </main>
      </div>
    );
  }
}

export default App;
