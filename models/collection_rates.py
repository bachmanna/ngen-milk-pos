from db_manager import db
from pony.orm import Required

class FATCollectionRate(db.Entity):
	cattle_type = Required(str, 8)
	fat_value = Required(float)
	rate = Required(float)

class FATAndSNFCollectionRate(db.Entity):
	cattle_type = Required(str, 8)
	fat_value = Required(float)
	snf_value = Required(float)
	rate = Required(float)

class TS1CollectionRate(db.Entity):
	cattle_type = Required(str, 8)
	fat_value = Required(float)
	snf_value = Required(float)
	fat_rate = Required(float)
	snf_rate = Required(float)

class TS2CollectionRate(db.Entity):
	cattle_type = Required(str, 8)
	min_value = Required(float)
	max_value = Required(float)
	rate = Required(float)
