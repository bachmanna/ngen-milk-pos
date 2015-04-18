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
        query = query.order_by(FATCollectionRate.id)
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
        query = query.order_by(FATAndSNFCollectionRate.fat_value)
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
        FATCollectionRate.query.filter_by(cattle_type=cattle_type).delete()
        for x in data:
            fatcolrate = FATCollectionRate(cattle_type=cattle_type,
                                           min_value=x['min_value'],
                                           max_value=x['max_value'],
                                           rate=x['rate'])
            db.session.add(fatcolrate)
        db.session.commit()

    def set_fat_and_snf_collection_rate(self, cattle_type, data):
        FATAndSNFCollectionRate.query.filter_by(cattle_type=cattle_type).delete()
        db.session.commit()
        for x in data:
          x["cattle_type"] = cattle_type
        smt = FATAndSNFCollectionRate.__table__.insert()
        db.engine.execute(smt, data)

    def save_fat_and_snf_collection_rate(self, cattle_type, fat_value, snf_value, rate):
        entity = FATAndSNFCollectionRate.query.filter_by(cattle_type=cattle_type, 
                                                         fat_value=fat_value, 
                                                         snf_value=snf_value).first()
        if entity and entity.id:
            entity.rate = rate
        else:
            entity = FATAndSNFCollectionRate(cattle_type=cattle_type, fat_value=fat_value,
                                             snf_value=snf_value, rate=rate)
            db.session.add(entity)
        db.session.commit()

    def set_ts1_collection_rate(self, cattle_type, data):
        TS1CollectionRate.query.filter_by(cattle_type=cattle_type).delete()
        for x in data:
            entity = TS1CollectionRate(cattle_type=cattle_type,
                                        min_fat = x["min_fat"],
                                        max_fat = x["max_fat"],
                                        fat_rate = x["fat_rate"],
                                        min_snf = x["min_snf"],
                                        max_snf = x["max_snf"],
                                        snf_rate = x["snf_rate"])
            db.session.add(entity)
        db.session.commit()


    def save_ts1_collection_rate(self, id, cattle_type, data):
        entity = None
        if id and int(id):
            entity = TS1CollectionRate.query.filter_by(id=id,cattle_type=cattle_type).first()
        if not entity:
            entity = TS1CollectionRate(cattle_type=cattle_type,
                                        min_fat = data["min_fat"],
                                        max_fat = data["max_fat"],
                                        fat_rate = data["fat_rate"],
                                        min_snf = data["min_snf"],
                                        max_snf = data["max_snf"],
                                        snf_rate = data["snf_rate"])
            db.session.add(entity)
        else:
            entity.min_fat = data["min_fat"]
            entity.max_fat = data["max_fat"]
            entity.fat_rate = data["fat_rate"]

            entity.min_snf = data["min_snf"]
            entity.max_snf = data["max_snf"]
            entity.snf_rate = data["snf_rate"]
        db.session.commit()

    def set_ts2_collection_rate(self, cattle_type, data):
        TS2CollectionRate.query.filter_by(cattle_type=cattle_type).delete()
        for x in data:
            entity = TS2CollectionRate(cattle_type=cattle_type,
                                              min_value=x['min_value'],
                                              max_value=x['max_value'],
                                              rate=x['rate'])
            db.session.add(entity)
        db.session.commit()

    def save_ts2_collection_rate(self, cattle_type, id, min_value, max_value, rate):
        entity = TS2CollectionRate.query.filter_by(cattle_type=cattle_type, 
                                                 min_value=min_value, 
                                                 max_value=max_value).first()
        if entity and entity.id:
            entity.rate = rate
        else:
            entity = TS2CollectionRate(cattle_type=cattle_type, min_value=min_value,
                                             max_value=max_value, rate=rate)
            db.session.add(entity)
        db.session.commit()
