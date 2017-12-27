export default function (vm, promise, keyState = 'promiseState') {
  vm[keyState] = { key: 'loading' };
  return promise
    .then((response) => {
      vm[keyState] = null;
      return response;
    })
    .catch((error) => {
      if (error.response) {
        vm[keyState] = {
          key: 'error',
          code: error.response.status,
          msg: 'Api coś nie tak.'
        };
      } else if (error.request) {
        vm[keyState] = { key: 'error', msg: 'Problem z połączeniem' };
      } else {
        vm[keyState] = { key: 'error', msg: 'Dziwny błąd' };
      }
      throw error;
    });
}
