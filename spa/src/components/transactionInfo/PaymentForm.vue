<template>
  <PromisedRowComponent :state="promiseState">
    <td>
      <TypeSelect
        v-model="value.payment_type_id"
        :types="paymentTypes"
      />
    </td>
    <td>
      <TypeSelect
        v-model="value.budget_id"
        :types="budgets"
      />
    </td>
    <td>
      <TypeSelect
        v-model="value.inner_budget_id"
        :types="innerBudgets"
      />
    </td>
    <td>
      <template v-if="paymentType && paymentType.has_members">
        <v-select
          size="sm"
          label="name"
          placeholder="członek"
          :value="value.member"
          @search="getMembers"
          @input="selectMember"
          :options="memberOptions"
          :debounce="250"
        />
      </template>
      <template v-else>
        <b-form-input
          v-model.trim.lazy="value.name"
          size="sm"
        />
      </template>
    </td>
    <td>
      <b-form-input
        v-model="value.date"
        size="sm"
        type="date"
      />
    </td>
    <td>
      <b-input-group
        append="zł"
        size="sm"
      >
        <b-form-input
          v-model.trim.lazy="value.cost"
          size="sm"
          type="number"
        />
      </b-input-group>
    </td>
    <td>
      <slot name="actions"></slot>
    </td>
  </PromisedRowComponent>
</template>

<script>
  import TypeSelect from '@/components/inputs/TypeSelect';

  import MemberService from '@/services/members'

  export default {
    components: {TypeSelect},
    props: ['value', 'transaction', 'budgets', 'innerBudgets', 'paymentTypes'],
    data () {
      return {
        promiseState: null,
        memberOptions: [],
      }
    },
    computed: {
      paymentType() {
        return this.paymentTypes[this.value.payment_type_id];
      },
    },
    watch: {
      'value.payment_type_id' () {
        this.value.member = null;
        this.value.member_id = 0;
      },
      transaction: {
        handler(value) {
          this.value.cost = (value.left ? Number(value.left) : 0).toFixed(2);
        },
        deep: true,
      },
    },
    methods: {
      getMembers (search, loading) {
        loading(true);
        MemberService
          .get({query: search})
          .then(response => {
            this.memberOptions = response.data;
            loading(false);
          })
      },
      selectMember (value) {
        this.value.member_id = value.id;
        this.value.member = value;
        this.value.name = "-";
      },
    }
  }
</script>
