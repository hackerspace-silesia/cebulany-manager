<template>
  <b-container>
    <b-row>
      <b-col>
        <PromisedComponent :state="promiseInnerState">
          <b-form inline="inline">
            <b-form-group label="Zakres">
              <date-picker
                v-model="yearRange"
                type="year"
                value-type="format"
                token="YYYY"
                range-separator=" → "
                :clearable="false"
                range
              />
            </b-form-group>
            <b-form-group label="Typ">
              <TypeSelect
                v-model="paymentTypeId"
                :types="paymentTypes"
              />
            </b-form-group>
            <b-form-group label="Szukaj">
              <b-form-input
                v-model.trim="memberFilter"
                type="text"
                placeholder="Szukaj..."
              />
            </b-form-group>
            <b-form-group label="*">
              <b-button
                id="new-member-form"
                variant="primary"
              >
                Dodaj
              </b-button>
              <b-button @click="excel">
                Excel
              </b-button>
              <b-popover
                target="new-member-form"
                triggers="focus click"
                placement="bottom"
                title="Dodaj nowego członka"
                :show.sync="showNewMemberForm"
              >
                <MemberForm
                  is-new="is-new"
                  @update="createNewMember"
                />
              </b-popover>
            </b-form-group>
          </b-form>
        </PromisedComponent>
      </b-col>
    </b-row><br>
    <b-row>
      <b-col>
        <PromisedComponent :state="promiseState">
          <MembersTable
            :members="members"
            :paidmonths="paidmonths"
            :payment-type-id="paymentTypeId"
            :years="years"
            :member-filter="memberFilter"
            @updateMember="updateMember"
          />
        </PromisedComponent>
      </b-col>
    </b-row>
  </b-container>
</template>
<script>
  import MembersTable from './MembersTable';
  import MemberForm from './MemberForm';
  import TypeSelect from '@/components/inputs/TypeSelect';

  import MembersService from '@/services/members';
  import PaymentService from '@/services/payment';
  import PaymentTypeService from '@/services/paymentType';

  import linkVm from '@/helpers/linkVm';

  export default {
    components: {
      MembersTable,
      MemberForm,
      TypeSelect
    },
    data () {
      let now = new Date();
      return {
        promiseState: null,
        promiseInnerState: null,
        members: {},
        paidmonths: [],
        paymentTypes: {},
        paymentTypeId: null,
        memberFilter: '',
        showNewMemberForm: false,
        yearRange: [`${now.getFullYear()-1}`, `${now.getFullYear()}`],
      }
    },
    computed: {
      years () {
        if (this.paymentTypeId === null) {
          return;
        }
        let years = [];
        let yearStart = parseInt(this.yearRange[0]);
        let yearEnd = parseInt(this.yearRange[1]);
        for (let year = yearStart; year <= yearEnd; year++) {
          years.push(year);
        }
        this.getPaidMonths();
        return years;
      }
    },
    created () {
      this.fetchInit();
    },
    methods: {
      fetchInit () {
        let promises = [
          PaymentTypeService.getAll({has_members: true}),
          MembersService.getAll()
        ];
        linkVm(this, Promise.all(promises), 'promiseInnerState')
          .then(responses => {
            let [paymentTypeResponse, memberResponse] = responses;
            this.paymentTypes = paymentTypeResponse.data;
            let paymentType = this.paymentTypes[0];
            this.paymentTypeId = paymentType ? paymentType.id : null;
            this.members = {};
            memberResponse.data.forEach(member => {
              this.members[member.id] = member;
            });
          })
      },
      getPaidMonths () {
        let promise = PaymentService.getTable({
          payment_type_id: this.paymentTypeId,
          start_year: this.yearRange[0],
          end_year: this.yearRange[1],
        });
        linkVm(this, promise)
          .then(resp => { this.paidmonths = resp.data; });
      },
      updateMember (obj) {
        let newMembers = {};
        newMembers[obj.id] = obj;
        this.members = Object.assign({}, this.members, newMembers);
      },
      createNewMember (obj) {
        this.updateMember(obj);
        this.getPaidMonths();
        this.showNewMemberForm = false;
      },
      excel (obj) {
        let promise = PaymentService.getExcelTable(
          this.yearRange[0], this.yearRange[1], this.paymentTypeId,
        );
        linkVm(this, promise);
      }
    }
  }
</script>
