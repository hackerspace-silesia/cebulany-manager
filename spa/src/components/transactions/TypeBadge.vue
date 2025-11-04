<template>
  <span class="transaction-badge" :style="type | typeStyle">
    {{ type | typeName }}
  </span>
</template>

<script>
  export default {
    filters: {
      typeStyle (type) {
        if (!type || !type.color) {
          return {};
        }
        return {
          background: 'none',
          backgroundColor: `#${type.color}`,
        };
      },
      typeName (type) {
        if (!type || !type.name) {
          return "-";
        }
        return type.name;
      }
    },
    props: {
      type: { required: true },
    }
  }
</script>

<style scoped>
  .transaction-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    vertical-align: middle;

    height: 3lh;
    width: 80px;

    padding: 4px;
    border-radius: 0;

    background: linear-gradient(45deg,
      rgb(177, 177, 177) 0%,
      rgb(46, 46, 46) 100%);
    color: white;

    font-size: 7pt;
    font-weight: bold;
    line-height: 1;
  }

  .transaction-badge:first-child {
    border-top-left-radius: 10px;
    border-bottom-left-radius: 10px;
  }

  .transaction-badge:last-child {
    border-top-right-radius: 10px;
    border-bottom-right-radius: 10px;
  }
</style>