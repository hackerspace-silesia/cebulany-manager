<template>
  <span class="attachment-badge" :class="{'text-danger': document.deleted_from_google}">
    <template v-if="document.accounting_record">
      {{ document.accounting_record }}
    </template>
    <template v-else>
      {{ document.filename }}
    </template>
    <template v-if="document.company_name">
      {{ document.company_name }}
    </template>
  </span>
</template>

<script>
  export default {
    props: {
      document: { required: true },
    }
  }
</script>

<style scoped>
  .attachment-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    vertical-align: middle;

    height: 3lh;
    width: 240px;

    padding: 4px;
    border-radius: 0;

    font-size: 7pt;
    font-weight: bold;
    line-height: 1;

    border: 2px dotted grey; 
    border-top-left-radius: 10px;
    border-bottom-left-radius: 10px;
    border-top-right-radius: 10px;
    border-bottom-right-radius: 10px;
  }
</style>