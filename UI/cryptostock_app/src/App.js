import React from "react";
import "./App.css";

import Login from "./components/Login/Login";
import Header from "./components/Header/Header";

import { Route, Switch, Redirect } from "react-router-dom";
import HomePage from "./pages/home";

class App extends React.Component {
  render() {
    return (
      <div className="app">
        <Header></Header>
        <main className="main">
          <Switch>
            <Route path="/login" component={Login} />
            <Route exact path="/" component={HomePage} />
            <Redirect to="/" />
          </Switch>
        </main>
      </div>
    );
  }
}

export default App;
