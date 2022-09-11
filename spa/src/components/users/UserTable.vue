<template>
  <div class="users">
    <b-table
      hover="hover"
      bordered="bordered"
      small="small"
      foot-clone="foot-clone"
      :items="users"
      :fields="fields"
    >
      <template v-slot:cell(username)="row">
        <b-form-input
          v-model.lazy.trim="row.item.username"
          @change="update(row.item)"
        />
      </template>
      <!--
      <template v-slot:cell(is_active)="row">
        <input
          v-model="row.item.is_active"
          type="checkbox"
          :true-value="true"
          :false-value="false"
          @change="update(row.item)"
        >
      </template>
      -->
      <template v-slot:cell(action)="row" >
        <b-button @click="remove(row.item)">
          Skasuj
        </b-button>
        <b-button @click="changePassword(row.item)">
          Zmień hasło
        </b-button>
        <b-button @click="showTOTP(row.item)">
          TOTP
        </b-button>
      </template>
    </b-table>
  </div>
</template>
<script>
  export default {
    props: ['users'],
    data () {
      return {
        fields: [
          {key: 'username', label: 'Nazwa'},
          // {key: 'is_active', label: 'Aktywny'},
          {key: 'action', label: 'Akcje'},
        ]
      }
    },
    methods: {
      update(row) {
        this.$emit('row-update', row);
      },
      remove(row) {
        this.$emit('row-remove', row);
      },
      changePassword(row) {
        this.$emit('row-change-password', row);
      },
      showTOTP(row) {
        this.$emit('row-show-totp', row);
      }
    }
  }
</script>
