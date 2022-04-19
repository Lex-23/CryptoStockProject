import React, { Component } from "react";
import axiosInstance from "../../axiosApi";
import SaleItem from "../../components/salesDashboard/salesDashboard";
import ReactPaginate from "react-paginate";
import "./Pagination.css";

class SalesDashboardList extends Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            offset: 0,
            salesList: [],
            perPage: 5,
            currentPage: 0,
        };
        this.handlePageClick = this.handlePageClick.bind(this);
        this.getSalesList = this.getSalesList.bind(this)
    }

    async getSalesList(){
        try {
            let response = await axiosInstance.get('/salesdashboard/', {
                params: {
                    limit: this.state.perPage,
                    offset: this.state.offset,
                }
            });
            const salesList = response.data;
            this.setState({
                pageCount: Math.ceil(response.data.count / this.state.perPage),
                salesList: salesList.results,
                isLoaded: true,
            });
            return salesList;
        } catch(error) {
            console.log("Error: ", JSON.stringify(error, null, 4));
            this.setState({
                isLoaded: true,
                error,
            });
            throw error;
        }
    }

    handlePageClick(e) {
        const selectedPage = e.selected;
        const offset = selectedPage * this.state.perPage;
        this.setState(
          {
            currentPage: selectedPage,
            offset: offset,
          },
          () => this.getSalesList()
        );
      }

    componentDidMount(){
        const salesData = this.getSalesList();
        console.log("salesData: ", JSON.stringify(salesData, null, 4));
    }

    render() {
        const { error, isLoaded } = this.state;
        if (error) {
          return <div>Error: {error.message}</div>;
        } else if (!isLoaded) {
          return <div>Loading...</div>;
        } else {
            return (
                <div>
                    <ReactPaginate
                        previousLabel={"previous"}
                        nextLabel={"next"}
                        breakLabel={"..."}
                        breakClassName={"break-me"}
                        pageCount={this.state.pageCount}
                        marginPagesDisplayed={2}
                        pageRangeDisplayed={1}
                        onPageChange={this.handlePageClick}
                        containerClassName={"pagination"}
                        subContainerClassName={"pages pagination"}
                        activeClassName={"active"}
                    />
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
}

export default SalesDashboardList;
