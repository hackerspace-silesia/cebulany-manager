<template lang="pug">
  PromisedComponent(:state="promiseState", show-on-promise)
    Alert(ref="successAlert")
    b-form(@submit="onSubmit")
      b-form-group(label="Nazwa", label-size="sm")
        b-form-input(type="text", v-model="name", size="sm")
      b-form-group(label="Data przystąpienia", label-size="sm")
        b-form-input(type="date", v-model="join_date", size="sm")
      label
        input(type="checkbox", v-model="is_active") 
        span Aktywny?
      b-form-group
        b-button(
          type="submit",
          :disable="promiseState && promiseState.key === 'loading'") {{ isNew? 'Dodaj' : 'Aktualizuj' }}
</template>

<script>
  import memberService from '@/services/members'

  import Alert from '@/components/Alert';
  import linkVm from '@/helpers/linkVm';

  export default {
    props: {
      member: Object,
      isNew: Boolean
    },
    data () {
      if (this.isNew) {
        return {
          promiseState: null,
          name: '',
          join_date: '',
          is_active: true
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
        if (this.isNew) {
          this.name = '';
          this.join_date = '';
          this.is_active = true;
        }
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
