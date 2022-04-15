import React, { Component } from "react";
import axiosInstance from "../axiosApi";

class AuthPing extends Component {
    constructor(props) {
        super(props);
        this.state = {
            message:"",
        };

        this.getMessage = this.getMessage.bind(this)
    }

    async getMessage(){
        try {
            let response = await axiosInstance.get('/auth-ping/');
            const message = response.data;
            this.setState({
                message: message,
            });
            return message;
        } catch(error) {
            console.log("Error: ", JSON.stringify(error, null, 4));
            throw error;
        }
    }

    componentDidMount(){
        const messageData1 = this.getMessage();
        console.log("messageData1: ", JSON.stringify(messageData1, null, 4));
    }

    render(){
        return (
            <div>
                <h2>-{this.state.message}-</h2>
            </div>
        )
    }
}

export default AuthPing;
