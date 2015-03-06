from services.rate_service import RateService
from models import *

class FATRateCalculator(object):
  def get_rate(self, cattle_type, fat, snf):
    rate_service = RateService()
    rate_list = rate_service.get_fat_collection_rate(cattle_type)
    if not rate_list or len(rate_list) == 0:
      return 0.0
    for x in rate_list:
      if fat >= x.min_value and fat <= x.max_value:
        return x.rate/10.0
    return 0.0

class FATSNFRateCalculator(object):
  def get_rate(self, cattle_type, fat, snf):
    return 0

class TS1RateCalculator(object):
  def get_rate(self, cattle_type, fat, snf):
    return 0

class TS2RateCalculator(object):
  def get_rate(self, cattle_type, fat, snf):
    rate_service = RateService()
    ts1 = (fat + snf)
    rate_list = rate_service.get_ts2_collection_rate(cattle_type)
    if not rate_list or len(rate_list) == 0:
      return 0
    for x in rate_list:
      if ts1 >= x.min_value and ts1 <= x.max_value:
        return x.rate/10.0
    return 0.0

#Rate calculator setup
rate_calculator = {
                    CollectionRateType.FAT: FATRateCalculator(),
                    CollectionRateType.FAT_AND_SNF: FATSNFRateCalculator(),
                    CollectionRateType.TS_1: TS1RateCalculator(),
                    CollectionRateType.TS_2: TS2RateCalculator(),
                  }

class RateCalc(object):
  def __init__(self, rate_type):
    self.calc = rate_calculator[rate_type]

  def get_rate(self, cattle_type, fat, snf):
    return self.calc.get_rate(cattle_type, fat, snf)