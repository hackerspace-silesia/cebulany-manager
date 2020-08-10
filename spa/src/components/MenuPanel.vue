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
        <b-nav-item href="#/budgets">
          Budżety
        </b-nav-item>
        <b-nav-item href="#/payment-types">
          Typy płatności
        </b-nav-item>
        <b-nav-item href="#/summary">
          Podsumowanie
        </b-nav-item>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>
