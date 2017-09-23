let methods = {
  getListOfCollections (obj) {
    return [
      obj.donations,
      obj.bills,
      obj.paidmonths,
      obj.others
    ];
  },

  computeLeftCost (obj) {
    let left = obj.cost || 0;
    let collections = methods.getListOfCollections(obj);
    collections.forEach((collection) => {
      collection.forEach((obj) => {
        left -= obj.cost;
      })
    });

    return left.toFixed(2);
  }
};

export default methods;
