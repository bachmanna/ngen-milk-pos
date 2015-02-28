import random
from models import *
from services.member_service import MemberService
from services.milkcollection_service import MilkCollectionService
from configuration_manager import ConfigurationManager


class TestData:
    def __init__(self):
        pass

    def create_members(self):
        mservice = MemberService()
        name = "John" + str(random.randint(0, 9999))
        mobile = str(random.randint(111111111, 999999999))
        member_id = mservice.add(name=name,
                                 cattle_type=CattleType.COW,
                                 mobile=mobile)

        member = mservice.get(member_id)
        print member.id
        print member.name
        print member.cattle_type
        print member.mobile

        collection = {}
        collection['member'] = member
        collection['shift'] = CollectionShift.MORNING
        collection['fat'] = 4.2
        collection['snf'] = 7.9
        collection['qty'] = 1.5
        collection['clr'] = 28.63
        collection['aw'] = 89.24
        collection['rate'] = 26.48
        collection['total'] = collection['rate'] * collection['qty']
        collection['created_by'] = 1

        colService = MilkCollectionService()
        col_id = colService.add(collection)

        col = colService.get(col_id)
        # print_collection(col)

        for x in colService.search(member_id=member_id):
            self.print_collection(x)

        from services.milksale_service import MilkSaleService

        saleService = MilkSaleService()
        sale_id = saleService.add(shift=CollectionShift.MORNING,
                                  qty=random.randint(1, 5) * 2.3,
                                  cattle_type=CattleType.BUFFALO,
                                  rate=random.randint(1, 5) * 12.3,
                                  created_by=1)
        sale = saleService.get(sale_id)
        # print_sale(sale)

        for x in saleService.search(_id=sale_id):
            self.print_sale(sale)


        # rate service test
        from services.rate_service import RateService

        rateService = RateService()
        rateService.set_cow_sale_rate(36.56)
        print "\n\nCow Sale Rate :", rateService.get_cow_sale_rate()

        rateService.set_buffalo_sale_rate(29.33)
        print "\nBuffalo Sale Rate :", rateService.get_buffalo_sale_rate()


    def print_sale(self, sale):
        print "\n\n===========SALE================"
        print "\nId: ", sale.id
        print "\nShift: ", sale.shift
        print "\nCattle: ", sale.cattle_type
        print "\nQty: ", sale.qty
        print "\nRate: ", sale.rate
        print "\nTotal: ", sale.total


    def print_collection(self, col):
        print "\n\n===========COLLECTION================"
        print "\nId: ", col.id
        print "\nShift: ", col.shift
        print "\nMember: ", col.member.name
        print "\nCattle: ", col.member.cattle_type
        print "\nQty: ", col.qty
        print "\nRate: ", col.rate
        print "\nTotal: ", col.total


    def datetime_test(self):
        from datetime import datetime
        from helpers.datetime_util import set_system_datetime

        d = datetime.now()
        print "BEFORE:", d
        time_tuple = (d.year,  # Year
                      d.month,  # Month
                      d.day + 1,  # Day
                      d.hour,  # Hour
                      d.minute,  # Minute
                      d.second,  # Second
                      d.microsecond,  # Millisecond
        )
        set_system_datetime(time_tuple)
        d = datetime.now()
        print "AFTER:", d


    def test_settings(self):
        configManager = ConfigurationManager()
        settings = {}

        settings[SystemSettings.SOCIETY_NAME] = "JEPPIAAR MILK COLLECTION CENTER"
        settings[SystemSettings.SOCIETY_ADDRESS] = "NO.6, Andiyur Post, Uthangarai Taluk, Krishnagiri - 635307."
        settings[SystemSettings.SOCIETY_ADDRESS1] = ""

        settings[SystemSettings.HEADER_LINE1] = "Milk center"
        settings[SystemSettings.HEADER_LINE2] = "address"
        settings[SystemSettings.HEADER_LINE3] = "phone"
        settings[SystemSettings.HEADER_LINE4] = ""

        settings[SystemSettings.FOOTER_LINE1] = ""
        settings[SystemSettings.FOOTER_LINE2] = "Thank you"

        settings[SystemSettings.SCALE_TYPE] = ScaleType.OPAL
        settings[SystemSettings.ANALYZER_TYPE] = AnalyzerType.ULTRA
        settings[SystemSettings.RATE_TYPE] = CollectionRateType.FAT

        settings[SystemSettings.BILL_OVERWRITE] = True
        settings[SystemSettings.MANUAL_FAT] = True
        settings[SystemSettings.MANUAL_SNF] = True
        settings[SystemSettings.MANUAL_QTY] = True
        settings[SystemSettings.PRINT_CLR] = False
        settings[SystemSettings.PRINT_WATER] = False
        settings[SystemSettings.PRINT_BILL] = True
        settings[SystemSettings.QUANTITY_2_DECIMAL] = True
        settings[SystemSettings.EXTERNAL_DISPLAY] = False
        settings[SystemSettings.COLLECTION_PRINTER_TYPE] = "Thermal"
        settings[SystemSettings.DATA_EXPORT_FORMAT] = "PDF"

        configManager.set_all_settings(settings)

        settings = configManager.get_all_settings()
        for k in settings.keys():
            print k, " = ", settings[k]