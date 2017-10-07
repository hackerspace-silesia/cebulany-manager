<template lang="pug">
  td(v-if='!value', :class="notPayedInDate ? 'table-danger' : ''") -
  td(v-else, :class="PayedInDate ? 'table-warning' : ''", @click="lol()") {{ Number(value).toFixed() }}
</template>
<script>
  export default {
    props: ['year', 'month', 'member', 'paidmonth', 'dtNow'],
    data () {
      let key = `${this.year}-${this.month}`;
      let dt = `${key}-01`;
      return {
        value: this.paidmonth.months[key],
        notPayedInDate: dt <= this.dtNow && this.member.join_date < dt,
        PayedInDate: dt <= this.dtNow && this.member.join_date > dt
      }
    },
    methods: {
      lol () {
        alert('lol')
      }
    }
  }
</script>
