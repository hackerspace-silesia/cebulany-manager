<template>
  <b-row>
    <b-col>
      <h1>Transfery</h1>
      <b-form>
        <b-col>
          <date-range-picker v-model="dateRange" />
        </b-col>
      </b-form>
      <PromisedComponent :state="promiseState">
        <InnerTransfersTable
          :inner-transfers="transfers"
          :inner-budgets="innerBudgets"
          :budgets="budgets"
          @row-update="update"
          @row-remove="remove"
        />
      </PromisedComponent>
    </b-col>
  </b-row>
</template>

<script>
import DateRange from '@/models/dateRange';

import InnerTransfersTable from './InnerTransfersTable'
import DateRangePicker from '@/components/inputs/DateRangePicker';
import linkVm from '@/helpers/linkVm'

import InnerTransfersService from '@/services/innerTransfer'
import InnerBudgetsService from '@/services/innerBudget'
import BudgetsService from '@/services/budget'

export default {
  components: {
    InnerTransfersTable,
    DateRangePicker,
  },
  data () {
    return {
      transfers: [],
      budgets: [],
      innerBudgets: [],
      promiseState: null,
      dateRange: DateRange.fromQuery(this.$route.query),
    };
  },
  mounted () {
    const promises = [
      BudgetsService.getAll(),
      InnerBudgetsService.getAll(),
    ];

    const dateRange = this.dateRange;

    linkVm(this, Promise.all(promises))
      .then(([budgetResp, innerBudgetResp]) => {
        this.budgets = budgetResp.data;
        this.innerBudgets = innerBudgetResp.data;
        this.fetchInnerTransfers(dateRange);
      });
  },
  watch: {
    dateRange(val) {
      this.$router.replace({
        name: 'InnerTransfers',
        query: val.toQuery(),
      }).catch(()=>{});

      this.fetchInnerTransfers(val);
    },
    $route() {
      this.dateRange = DateRange.fromQuery(this.$route.query);
    },
  },
  methods: {
    fetchInnerTransfers (dateRange) {
      const query = {
        start_date: dateRange.start,
        end_date: dateRange.end,
      };
      linkVm(this, InnerTransfersService.getAll(query))
        .then((response) => {
          this.transfers = response.data;
        });
    },
    update (data) {
      if (!data.id) {
        InnerTransfersService.post(data).then(obj => {
          this.transfers.unshift(obj.data);
        });
      } else {
        InnerTransfersService.update(data.id, data);
      }
    },
    remove (data) {
      InnerTransfersService.delete(data.id).then(() => {
        this.transfers = this.transfers.filter(obj => obj.id !== data.id);
      });
    }
  }
}
</script>
