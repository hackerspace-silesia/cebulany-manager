<template lang="pug">
  b-form
    b-form-group
      b-form-radio(:options="has_month_options")
</template>

<script>
  export default {
    data () {
      return {
        has_month_options: [
          {'text': 'Miesiąc', value: 'month'},
          {'text': 'Zakres Dat', value: 'date_range'}
        ]
      }
    }
  }
</script>
