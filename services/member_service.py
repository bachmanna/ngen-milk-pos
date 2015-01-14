from models.member import Member
from models.cattle_type import CattleType
from pony.orm import commit, select

class MemberService:
	def __init__(self):
		pass

	def add(self, name, cattle_type, mobile):
		member = Member(name=name, cattle_type=cattle_type, mobile=mobile, status=True)
		commit()
		return member.id

	def get(self, _id):
		member = Member[_id]
		return member

	def search(self, name=None, mobile=None, cattle_type=None):
		lst = select(p for p in Member if p.mobile == mobile)[:]
		return lst

	def delete(self, _id):
		pass

	def import_data(self, csv_data):
		pass

	def export_data(self):
		return None
