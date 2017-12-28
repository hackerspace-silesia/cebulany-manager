<template lang="pug">
  b-alert(
      :variant="variant", :show="counter", dismissible,
      @dismissed="counter = 0", @dismiss-count-down="countDown")
    template OK!
</template>
<script>
  export default {
    props: {
      variant: {
        type: String,
        default: 'success'
      }
    },
    data () {
      return {
        counter: 0
      }
    },
    created () {
      this.$on('turnOn', this.turnOn);
    },
    methods: {
      countDown (counter) { this.counter = counter; },
      turnOn () { this.counter = 5; }
    }
  }
</script>
