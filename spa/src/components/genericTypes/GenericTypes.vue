<template lang="pug">
  b-row: b-col
    h1 {{ title }}
    GenericTypeForm(@change="fetch")
    PromisedComponent(:state="promiseState")
      GenericTypeTable(:items="items")
</template>

<script>
import GenericTypeForm from './GenericTypeForm'
import GenericTypeTable from './GenericTypeTable'
import linkVm from '@/helpers/linkVm'

export default {
  props: ['service', 'title'],
  data () {
    return {
      promiseState: null,
      items: []
    }
  },
  components: { GenericTypeForm, GenericTypeTable },
  created () {
    this.fetch();
  },
  watch: {
    '$route' () {
      this.fetch();
    }
  },
  methods: {
    fetch (params) {
      linkVm(this, this.service.getAll(params))
        .then((response) => {
          this.items = response.data;
        })
    }
  }
}
</script>
