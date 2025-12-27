<template>
  <PromisedRowComponent :state="promiseState">
    <td>
      <TypeSelect
        v-model="value.payment_type_id"
        :types="paymentTypes"
        @input="update"
      />
    </td>
    <td>
      <TypeSelect
        v-model="value.budget_id"
        :types="budgets"
        @input="update"
      />
    </td>
    <td>
      <TypeSelect
        v-model="value.inner_budget_id"
        :types="innerBudgets"
        @input="update"
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
          @change="update"
          size="sm"
        />
      </template>
    </td>
    <td>
      <b-form-input
        v-model="value.date"
        @change="update"
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
          @change="update"
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
    props: ['value', 'budgets', 'innerBudgets', 'paymentTypes'],
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
    },
    methods: {
      update() {
        this.$emit("change", this.value);
      },
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
        this.update();
      },
    }
  }
</script>
