import React from "react";
import "./salesDashboard.css";

function SaleItem(props) {
  return (
    <div className="sale-container">
      <div className="sale__asset-name">{props.sale.asset.name}</div>
      <div className="sale__asset-desc">{props.sale.asset.description}</div>
      <div className="sale__count">Count: {props.sale.count}</div>
      <div className="sale__price">Price: {props.sale.price}</div>
      <div className="sale__broker">Saler: {props.sale.broker.name}</div>
    </div>
  );
}

export default SaleItem;
