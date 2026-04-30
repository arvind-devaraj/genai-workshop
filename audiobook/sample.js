const TAX_RATES = {
  USA: 0.07,
  CAN: 0.12,
};
const DEFAULT_TAX_RATE = 0.15;

function isValidOrder(order) {
  return order.id != null && order.amount > 0;
}

function calculateTax(amount, country) {
  return amount * (TAX_RATES[country] ?? DEFAULT_TAX_RATE);
}

function buildProcessedOrder(order) {
  const tax = calculateTax(order.amount, order.country);
  const total = order.amount + tax;
  return {
    orderId: order.id,
    total,
    tax,
    formattedDate: new Date().toISOString(),
    isHighValue: total > 1000,
  };
}

function processOrders(orders) {
  return orders
    .filter(order => isValidOrder(order) && order.status === 'pending')
    .map(buildProcessedOrder);
}

module.exports = processOrders;
