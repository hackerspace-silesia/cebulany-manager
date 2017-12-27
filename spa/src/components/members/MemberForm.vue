<template lang="pug">
  PromisedComponent(:state="promiseState", show-on-promise)
    b-alert(variant="success", :show="success") OK!
    b-form(@submit="onSubmit")
      b-form-group(label="Nazwa")
        b-form-input(type="text", v-model="name", size="sm")
      b-form-group(label="Data przystąpienia")
        b-form-input(type="date", v-model="join_date", size="sm")
      b-form-checkbox(v-model="is_active") Aktywny?
      b-form-group
        b-button(type="submit", :disable="promiseState && promiseState.key === 'loading'") Dodaj
</template>

<script>
  import memberService from '@/services/members'
  import linkVm from '@/helpers/linkVm';

  export default {
    props: ['member', 'update'],
    data () {
      let member = this.member;
      return {
        promiseState: null,
        name: member.name || '',
        join_date: member.join_date || new Date(),
        is_active: member.is_active,
        success: false
      }
    },
    watch: {
      member () {
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

        linkVm(this, memberService.update(
          {
            id: this.member.id,
            data: data
          }
        ))
          .then(resp => {
            this.success = true;
            this.$emit('update', resp.data);
          })
      }
    }
  }
</script>
