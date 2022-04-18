import React from "react";

function SaleItem(props) {
  return (
    <div className="container">
      <div className="sale__asset-name">{props.sale.asset.name}</div>
      <div className="sale__asset-desc">{props.sale.asset.description}</div>
      <div className="sale__count">{props.sale.count}</div>
      <div className="sale__price">{props.sale.price}</div>
      <div className="sale__broker">{props.sale.broker.name}</div>
      <br /> <hr />
    </div>
  );
}

export default SaleItem;
