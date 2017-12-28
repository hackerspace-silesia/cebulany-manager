<template lang="pug">
  PromisedComponent(:state="promiseState", show-on-promise)
    Alert(ref="successAlert")
    b-form(@submit="onSubmit")
      b-form-group(label="Nazwa")
        b-form-input(type="text", v-model="name", size="sm")
      b-form-group(label="Data przystąpienia")
        b-form-input(type="date", v-model="join_date", size="sm")
      b-form-checkbox(v-model="is_active") Aktywny?
      b-form-group
        b-button(
          type="submit",
          :disable="promiseState && promiseState.key === 'loading'") Dodaj
</template>

<script>
  import memberService from '@/services/members'

  import Alert from '@/components/Alert';
  import linkVm from '@/helpers/linkVm';

  export default {
    props: ['member', 'update', 'isNew'],
    data () {
      if (this.isNew) {
        return {
          promiseState: null,
          name: '',
          join_date: '',
          is_active: ''
        }
      }

      let member = this.member;
      return {
        promiseState: null,
        name: member.name,
        join_date: member.join_date,
        is_active: member.is_active
      }
    },
    watch: {
      member () {
        if (this.isNew) { return; }
        let member = this.member;
        this.name = member.name;
        this.join_date = member.join_date;
        this.is_active = member.is_active;
      }
    },
    methods: {
      onSubmit (evt) {
        evt.preventDefault();
        let data = {
          name: this.name,
          join_date: this.join_date,
          is_active: this.is_active
        };

        let promise = null;

        if (this.isNew) {
          promise = memberService.create(data);
        } else {
          promise = memberService.update(this.member.id, data);
        }

        linkVm(this, promise)
          .then(resp => {
            this.$emit('update', resp.data);
            this.$refs.successAlert.$emit('turnOn');
          })
      }
    },
    components: {
      Alert
    }
  }
</script>
