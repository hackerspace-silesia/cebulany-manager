<template>
  <b-row>
    <b-col>
      <h1>Użytkownicy</h1>
      <PromisedComponent :state="promiseState">
        <b-button @click="openCreateUserModal">
          Dodaj użytkownika
        </b-button>
        <UserTable
          :users="users"
          @row-update="update"
          @row-remove="openRemoveUserModal"
          @row-change-password="openChangePasswordModal"
          @row-show-totp="openTOTPModal"
        />
      </PromisedComponent>
    </b-col>
    <b-modal hide-header hide-footer ref="changePasswordModal">
      <ChangePasswordModal
        :user="selectedUser"
        v-if="selectedUser !== null"
        @change="changePassword"
      />
    </b-modal>
    <b-modal hide-header hide-footer ref="removeUserModal">
      <RemoveUserModal
        :user="selectedUser"
        v-if="selectedUser !== null"
        @remove="remove"
      />
    </b-modal>
    <b-modal hide-header hide-footer ref="createUserModal">
      <CreateUserModal @create="create" />
    </b-modal>
    <b-modal hide-header ok-only ref="TOTPModal">
      <TOTPModal
        :user="selectedUser"
        v-if="selectedUser !== null"
      />
    </b-modal>
  </b-row>
</template>

<script>
import UserTable from './UserTable'
import linkVm from '@/helpers/linkVm'

import UserService from '@/services/user'
import ChangePasswordModal from './ChangePasswordModal';
import CreateUserModal from './CreateUserModal';
import RemoveUserModal from './RemoveUserModal';
import TOTPModal from './TOTPModal';

export default {
  components: {
    ChangePasswordModal,
    CreateUserModal,
    RemoveUserModal,
    TOTPModal,
    UserTable
  },
  data () {
    return {
      users: [],
      promiseState: null,
      selectedUser: null,
    }
  },
  created () {
    this.fetchUsers();
  },
  methods: {
    fetchUsers () {
      linkVm(this, UserService.getAll())
        .then((response) => {
          this.users = response.data;
        })
    },
    openChangePasswordModal(user) {
      this.selectedUser = user;
      this.$refs['changePasswordModal'].show();
    },
    openRemoveUserModal(user) {
      this.selectedUser = user;
      this.$refs['removeUserModal'].show();
    },
    openTOTPModal(user) {
      this.selectedUser = user;
      this.$refs['TOTPModal'].show();
    },
    openCreateUserModal() {
      this.$refs['createUserModal'].show();
    },
    create(data) {
      this.$refs['createUserModal'].hide();
      UserService.create(data).then(obj => {
        this.users.push(obj.data);
      });
    },
    update (data) {
      UserService.update(data.id, data);
    },
    changePassword (data) {
      this.$refs['changePasswordModal'].hide();
      UserService.changePassword(data.id, data.password);
    },
    remove (userId) {
      this.$refs['removeUserModal'].hide();
      UserService.delete(userId).then(() => {
        this.users = this.users.filter(obj => obj.id !== userId);
      });
    }
  }
}
</script>

<style>
</style>
