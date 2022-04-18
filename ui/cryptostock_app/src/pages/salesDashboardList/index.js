import React, { Component } from "react";
import axiosInstance from "../../axiosApi";
import SaleItem from "../../components/salesDashboard/salesDashboard";

class SalesDashboardList extends Component {
    constructor(props) {
        super(props);
        this.state = {
            salesList: [],
        };

        this.getSalesList = this.getSalesList.bind(this)
    }

    async getSalesList(){
        try {
            let response = await axiosInstance.get('/salesdashboard/');
            const salesList = response.data;
            this.setState({
                salesList: salesList.results,
            });
            return salesList;
        } catch(error) {
            console.log("Error: ", JSON.stringify(error, null, 4));
            throw error;
        }
    }

    componentDidMount(){
        const salesData = this.getSalesList();
        console.log("salesData: ", JSON.stringify(salesData, null, 4));
    }

    render() {

        //else if (!isLoaded) {
        //    return <div>Loading...</div>;
        //}

            return (
                <div>
                    <div className="sale">
                        <div className="container">
                            {this.state.salesList.map((sale) => (
                                <SaleItem key={sale.id} sale={sale} />
                            ))}
                        </div>
                    </div>
                </div>
            );

    }
}

export default SalesDashboardList;
