<template>
  <div>
    <b-form>
      <label>TOTP</label> <b-form-input v-model="user.totp_uri" disabled />
    </b-form>
  </div>
</template>
<script>
  export default {
    props: ['user'],
  }
</script>
