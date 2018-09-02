let methods = {

  computeLeftCost (obj) {
    let left = Number(obj.cost) || 0;
    obj.payments.forEach((obj) => {
      left -= obj.cost;
    });

    obj.left = left;
    return left.toFixed(2);
  }
};

export default methods;
