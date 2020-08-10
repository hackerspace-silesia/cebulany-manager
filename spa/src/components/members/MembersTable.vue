<template>
  <div class="members">
    <b-modal
      v-model="showModal"
      title="Edycja"
      size="lg"
      ok-only="ok-only"
    >
      <MemberModal
        v-if="showModal"
        :item="modalMember"
        @update="updateForm"
      />
    </b-modal>
    <table class="table-sm table table-bordered table-condensed table-hover table-members">
      <thead>
        <tr>
          <th rowspan="2">
            Członek
          </th>
          <th
            v-for="year in years"
            colspan="12"
          >
            {{ year }}
          </th>
        </tr>
        <tr>
          <template v-for="year in years">
            <th
              v-for="month in months"
              class="text-center"
            >
              {{ month }}
            </th>
          </template>
        </tr>
      </thead>
      <tbody>
        <template v-for="o in memberList">
          <PaidRow
            :member="o.member"
            :years="years"
            :months="months"
            :paidmonth="o.paidmonth"
            :dt-now="dtNow"
            :payment-type-id="paymentTypeId"
            @updateMember="updateMemberInTable"
          />
        </template>
      </tbody>
    </table>
  </div>
</template>
<script>
  import PaidRow from './PaidRow';
  import MemberModal from './MemberModal';

  export default {
    components: {
      PaidRow,
      MemberModal
    },
    props: ['years', 'members', 'paidmonths', 'updateMember', 'memberFilter', 'paymentTypeId'],
    data () {
      return {
        months: ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
        dtNow: (new Date()).toISOString().slice(0, 10),
        showModal: false,
        modalMember: null
      }
    },
    computed: {
      memberList () {
        const members = this.members;
        const memberFilter = this.memberFilter.toLowerCase();
        const memberList = this.paidmonths
          .map(paidmonth => {
            const member = members[paidmonth.member_id];
            return {
              member: member,
              paidmonth: paidmonth
            };
          })
          .filter(({member}) => {
            const name = member.name.toLowerCase();
            return name.indexOf(memberFilter) !== -1;
          });

        this.fillWithEmptyMembers(members, memberList, memberFilter);
        this.sortMemberList(memberList);
        return memberList;
      }
    },
    methods: {
      updateMemberInTable (data) {
        this.showModal = true;
        this.modalMember = data;
      },
      updateForm (data) {
        this.$emit('updateMember', data);
      },
      fillWithEmptyMembers (members, memberList, memberFilter) {
        Object
          .values(members)
          .filter(member => {
            const name = member.name.toLowerCase();
            if (name.indexOf(memberFilter) === -1) {
              return false;
            }
            const isMemberExists = memberList.find(o => o.member.id === member.id);
            return !isMemberExists;
          })
          .forEach(member => {
            const paidmonth = { months: [] };
            memberList.push({ member, paidmonth });
          });
      },
      sortMemberList (memberList) {
        memberList.sort((a, b) => {
          const memberA = a.member;
          const memberB = b.member;
          const isLower = (attr) => memberA[attr] < memberB[attr] ? -1 : 0;
          const isGreater = (attr) => memberA[attr] > memberB[attr] ? 1 : 0;
          const isDifferent = (attr) => isLower(attr) || isGreater(attr);
          const isDifferentRev = (attr) => isDifferent(attr) * -1;

          return (
            isDifferentRev('is_active') ||
            isDifferent('join_date') ||
            isDifferent('name')
          );
        });
      }
    }
  }
</script>
<style>
 .table-members th,.table-members td {text-align: center; vertical-align: middle !important;}
</style>
<style scoped>
  table { background-color: #fafafa;}
</style>

