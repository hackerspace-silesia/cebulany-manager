<template lang="pug">
  b-navbar(toggleable="md" type="dark", variant="dark")
    b-nav-toggle(target="nav_collapse")
    b-navbar-brand(href="#/") Cebulany Manager
    b-collapse(is-nav id="nav_collapse")
      b-nav(is-nav-bar)
        b-nav-item(href="#/") Przelewy
        b-nav-item(href="#/members") Członkowie
        b-nav-item(href="#/bills") Rachunki
        b-nav-item(href="#/donations") Darowizny
        b-nav-item(href="#/others") Inne płatności
</template>
