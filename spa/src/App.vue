<template lang="pug">
  #app
    MenuPanel
    br
    b-container
      router-view
</template>

<script>
import MenuPanel from '@/components/MenuPanel'
export default {
  name: 'app',
  components: {
    MenuPanel
  }
}
</script>

<style>
  .table-sm td { font-size: 8pt; }
  .table-sm th { font-size: 8pt; }
  .monospace { font-family: 'monospace'; }
</style>
