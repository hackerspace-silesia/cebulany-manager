<template>
  <b-navbar
    toggleable="md"
    type="dark"
    variant="dark"
  >
    <b-nav-toggle target="nav_collapse" />
    <b-navbar-brand href="#/">
      Cebulany Manager
    </b-navbar-brand>
    <b-collapse
      id="nav_collapse"
      is-nav="is-nav"
    >
      <b-navbar-nav>
        <b-nav-item href="#/">
          Przelewy
        </b-nav-item>
        <b-nav-item href="#/members">
          Członkowie
        </b-nav-item>
        <b-nav-item href="#/payments">
          Płatności
        </b-nav-item>
        <b-nav-item href="#/documents">
          Dokumenty
        </b-nav-item>
        <b-nav-item href="#/budgets">
          Budżety
        </b-nav-item>
        <b-nav-item href="#/inner-budgets">
          Budżety wewnętrzne
        </b-nav-item>
        <b-nav-item href="#/inner-transfers">
          Transfery
        </b-nav-item>
        <b-nav-item href="#/payment-types">
          Typy płatności
        </b-nav-item>
        <b-nav-item href="#/accountancy-types">
          Księgowe typy
        </b-nav-item>
        <b-nav-item href="#/summary">
          Podsumowanie
        </b-nav-item>
        <b-nav-item href="#/users">
          Użytkownicy
        </b-nav-item>
      </b-navbar-nav>

      <b-navbar-nav class="ml-auto">
        <b-nav-text :class="{'text-danger': totalSeconds < 60}">
          Pozostały czas: <span class="monospace">{{ timeLeft }}</span>
        </b-nav-text>
        <b-nav-item @click="logout">
          Wyloguj się
        </b-nav-item>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>
<script>
import stateData from '@/state';
import loginService from '@/services/login';

export default {
  data() {
    return {
      timeLeft: '-',
      totalSeconds: 0,
      timerId: 0,
    }
  },
  mounted() {
    this.timerId = setInterval(() => {
      this.totalSeconds = this.$root.$data.deadline - stateData.now();
      if (this.totalSeconds < 0) {
        this.logout();
      }
      const minutes = this.leftPad(Math.floor(this.totalSeconds / 60));
      const seconds = this.leftPad(this.totalSeconds % 60);
      this.timeLeft = `${minutes}:${seconds}`;
      //this.timeLeft = `${this.totalSeconds}`;
    }, 1000);
  },
  destroyed() {
    if (this.timerId) clearInterval(this.timerId);
  },
  methods: {
    leftPad(x) {
      const s = x.toString();
      return (s.length > 1) ? s : '0' + s;
    },
    logout() {
      loginService.logout();
      this.$emit('logout');
    }
  }
}
</script>
