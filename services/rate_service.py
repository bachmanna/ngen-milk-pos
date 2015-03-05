from models import *
from db_manager import db
from configuration_manager import ConfigurationManager


class RateService:
    def __init__(self):
        self.configManager = ConfigurationManager()

    #### SALE RATES ######
    def get_cow_sale_rate(self):
        return self.configManager.get(SalesRate.COW)

    def get_buffalo_sale_rate(self):
        return self.configManager.get(SalesRate.BUFFALO)

    def set_cow_sale_rate(self, cow_rate_value):
        self.configManager.set(SalesRate.COW, cow_rate_value)

    def set_buffalo_sale_rate(self, buffalo_rate_value):
        self.configManager.set(SalesRate.BUFFALO, buffalo_rate_value)


    #### COLLECTION RATES ######
    def get_fat_collection_rate(self, cattle_type):
        query = FATCollectionRate.query.filter_by(cattle_type=cattle_type)
        lst = query.all()
        return lst

    def add_fat_collection_rate(self, cattle_type, id, min_value, max_value, rate):
        entity = FATCollectionRate(id=id,cattle_type=cattle_type,min_value=min_value, max_value=max_value, rate=rate)
        db.session.add(entity)
        db.session.commit()
        return entity.id

    def update_fat_collection_rate(self, cattle_type, id, min_value, max_value, rate):
        entity = FATCollectionRate.query.filter_by(id=id).first()
        if entity:
            entity.min_value=min_value
            entity.max_value=max_value
            entity.rate = rate
            db.session.commit()
        else:
            self.add_fat_collection_rate(cattle_type, id, min_value, max_value, rate)

    def get_fat_and_snf_collection_rate(self, cattle_type):
        query = FATAndSNFCollectionRate.query.filter_by(cattle_type=cattle_type)
        lst = query.all()
        return lst

    def get_ts1_collection_rate(self, cattle_type):
        query = TS1CollectionRate.query.filter_by(cattle_type=cattle_type)
        lst = query.all()
        return lst

    def get_ts2_collection_rate(self, cattle_type):
        query = TS2CollectionRate.query.filter_by(cattle_type=cattle_type)
        lst = query.all()
        return lst

    def set_fat_collection_rate(self, cattle_type, data):
        FATCollectionRate.drop_table(with_all_data=True)
        db.create_tables()
        for x in data:
            fatcolrate = FATCollectionRate(cattle_type=cattle_type,
                                           min_value=x['min_value'],
                                           max_value=x['max_value'],
                                           rate=x['rate'])
            db.session.add(fatcolrate)
        db.session.commit()

    def set_fat_and_snf_collection_rate(self, cattle_type, data):
        FATAndSNFCollectionRate.drop_table(with_all_data=True)
        db.create_tables()
        for x in data:
            fatsnfcolrate = FATAndSNFCollectionRate(cattle_type=cattle_type,
                                                    fat_value=x['fat_value'],
                                                    snf_value=x['snf_value'],
                                                    rate=x['rate'])
            db.session.add(fatsnfcolrate)
        db.session.commit()

    def set_ts1_collection_rate(self, cattle_type, data):
        TS1CollectionRate.drop_table(with_all_data=True)
        db.create_tables()
        for x in data:
            fatsnfcolrate = TS1CollectionRate(cattle_type=cattle_type,
                                              fat_value=x['fat_value'],
                                              snf_value=x['snf_value'],
                                              fat_rate=x['fat_rate'],
                                              snf_rate=x['snf_rate'])
        commit()

    def set_ts2_collection_rate(self, cattle_type, data):
        TS2CollectionRate.drop_table(with_all_data=True)
        db.create_tables()
        for x in data:
            fatsnfcolrate = TS2CollectionRate(cattle_type=cattle_type,
                                              min_value=x['min_value'],
                                              max_value=x['max_value'],
                                              rate=x['rate'])
            db.session.add(fatsnfcolrate)
        db.session.commit()