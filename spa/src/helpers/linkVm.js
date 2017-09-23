export default function (vm, promise) {
  vm.is_loading = true;
  vm.is_error = false;
  return promise
    .then((response) => {
      vm.is_loading = false;
      return response;
    })
    .catch((error) => {
      vm.is_loading = false;
      vm.is_error = true;
      throw error;
    });
}
