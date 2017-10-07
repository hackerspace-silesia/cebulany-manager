import PaidMonthService from '@/services/paidmonth'
import BillService from '@/services/bill'
import DonationService from '@/services/donation'
import OtherService from '@/services/other'

export default {
  getServiceByType (type) {
    switch (type) {
      case 'paid_month': return PaidMonthService;
      case 'bill': return BillService;
      case 'donation': return DonationService;
      case 'other': return OtherService;
      default: return null;
    }
  }
}
