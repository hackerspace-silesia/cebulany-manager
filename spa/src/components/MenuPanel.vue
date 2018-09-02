<template lang="pug">
  b-navbar(toggleable="md" type="dark", variant="dark")
    b-nav-toggle(target="nav_collapse")
    b-navbar-brand(href="#/") Cebulany Manager
    b-collapse(is-nav id="nav_collapse")
      b-navbar-nav
        b-nav-item(href="#/") Przelewy
        b-nav-item(href="#/members") Członkowie
        b-nav-item(href="#/budgets") Budżety
        b-nav-item(href="#/payment-types") Typy płatności
</template>
