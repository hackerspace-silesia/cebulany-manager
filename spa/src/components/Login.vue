<template>
<div>
  <b-jumbotron header="Cebulany Manager" />
  <h3>Login</h3>
  <PromisedComponent
    :state="promiseState"
    show-on-promise="show-on-promise"
  >
    <b-form @submit="onSubmit">
      <b-form-group label="Login">
        <b-form-input v-model.trim="login" />
      </b-form-group>
      <b-form-group label="Hasło">
        <b-form-input
          v-model.trim="password"
          type="password"
        />
      </b-form-group>
      <b-form-group label="Token (2FA)">
        <b-form-input
          v-model.trim="token"
          type="password"
        />
      </b-form-group>
      <b-form-group>
        <b-button
          type="submit"
          variant="primary"
        >
          Zaloguj się
        </b-button>
      </b-form-group>
    </b-form>
  </PromisedComponent>
</div>
</template>
<script>
  import linkVm from '@/helpers/linkVm';
  import loginService from '@/services/login';

  export default {
    props: ['onSuccess'],
    data () {
      return {
        login: '',
        password: '',
        token: '',
        promiseState: null
      }
    },
    mounted () {
      const success = loginService.loginFromSession();
      if (success) {
        this.$emit('onSuccess');
      }
    },
    methods: {
      onSubmit (evt) {
        evt.preventDefault();
        linkVm(this, loginService.getToken(this.login, this.password, this.token))
          .then(({ token, token_time }) => {
            loginService.setTokenIntoSession(token, token_time);
            this.$emit('onSuccess');
          });
      }
    }
  }
</script>
