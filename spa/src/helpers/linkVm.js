export default function (vm, promise) {
  vm.promiseState = { key: 'loading' };
  return promise
    .then((response) => {
      vm.promiseState = null;
      return response;
    })
    .catch((error) => {
      if (error.response) {
        vm.promiseState = {
          key: 'error',
          code: error.response.status,
          msg: 'Api coś nie tak.'
        };
      } else if (error.request) {
        vm.promiseState = { key: 'error', msg: 'Problem z połączeniem' };
      } else {
        vm.promiseState = { key: 'error', msg: 'dziwny błąd' };
      }
      throw error;
    });
}
