<template>
  <PromisedRowComponent :state="promiseState">
    <td>
      <TypeSelect
        v-model="paymentTypeId"
        :types="paymentTypes"
      />
    </td>
    <td>
      <TypeSelect
        v-model="budgetId"
        :types="budgets"
      />
    </td>
    <td>
      <TypeSelect
        v-model="innerBudgetId"
        :types="innerBudgets"
      />
    </td>
    <td>
      <template v-if="paymentType && paymentType.has_members">
        <v-select
          size="sm"
          label="name"
          placeholder="członek"
          :value="member"
          @search="getMembers"
          @input="selectMember"
          :options="memberOptions"
          :debounce="250"
        />
      </template>
      <template v-else>
        <b-form-input
          v-model.trim="name"
          size="sm"
        />
      </template>
    </td>
    <td>
      <b-form-input
        v-model="date"
        size="sm"
        type="date"
      />
    </td>
    <td>
      <b-input-group
        right="zł"
        size="sm"
      >
        <b-form-input
          v-model.trim="cost"
          size="sm"
          type="number"
        />
      </b-input-group>
    </td>
    <td>
      <b-btn
        size="sm"
        variant="primary"
        @click="addType()"
      >
        dodaj
      </b-btn>
    </td>
  </PromisedRowComponent>
</template>

<script>
  import TypeSelect from '@/components/inputs/TypeSelect';

  import MemberService from '@/services/members'
  import PaymentService from '@/services/payment'
  import linkVm from '@/helpers/linkVm'

  export default {
    components: {TypeSelect},
    props: ['item', 'budgets', 'innerBudgets', 'paymentTypes'],
    data () {
      let suggestion = this.item.suggestion !== null ? this.item.suggestion : {
        budget_id: 0,
        inner_budget_id: 0,
        type_id: 0,
        type_name: '',
        member: null,
      };

      return {
        promiseState: null,
        budgetId: suggestion.budget_id,
        budget: this.budgets[suggestion.budget_id] || null,
        innerBudgetId: suggestion.inner_budget_id,
        innerBudget: this.innerBudgets[suggestion.inner_budget_id] || null,
        paymentTypeId: suggestion.type_id,
        paymentType: this.paymentTypes[suggestion.type_id] || null,
        cost: this.item.left || 0,
        name: suggestion.type_name,
        member: suggestion.member,
        memberOptions: [],
        date: this.item.date || (new Date()).toISOString().slice(0, 10)
      }
    },
    watch: {
      budgetId (value) {
        this.budget = this.budgets[value];
      },
      paymentTypeId (value) {
        this.paymentType = this.paymentTypes[value];
      },
      item: {
        handler(value) {
          this.cost = value.left || 0;
        },
        deep: true,
      }
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
        this.member = value;
      },
      addType () {
        let name;
        let memberId;
        if (this.paymentType.has_members) {
          memberId = this.member.id;
          name = '-';
        } else {
          memberId = null;
          name = this.name;
        }

        let promise = PaymentService.post({
          transaction_id: this.item.id,
          member_id: memberId,
          budget_id: this.budgetId,
          inner_budget_id: this.innerBudgetId,
          payment_type_id: this.paymentTypeId,
          name: name,
          date: this.date,
          cost: this.cost
        });

        linkVm(this, promise).then(response => {
          this.item.left -= Number(response.data.cost) || 0;
          this.item.payments.push(response.data);
          this.cost = this.item.left;
        })
      }
    }
  }
</script>
