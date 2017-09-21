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
