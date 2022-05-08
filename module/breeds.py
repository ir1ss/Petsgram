# breeds表模型
from sqlalchemy import Table
from common.database import dbconnect
from module.users import Users

# 把common/database.py中定义的数据库连接实例导入
dbsession, md, DBase = dbconnect()

class Breeds(DBase):
    __table__ = Table('breeds', md, autoload=True)

    def find_all_breed(self):
        result = dbsession.query(Breeds.breedId, Breeds).all()
        return result

    def find_by_name(self, breedName):
        row = dbsession.query(Breeds).filter(Breeds.breedName==breedName).first()
        return row

    def find_by_id(self, id):
        row = dbsession.query(Breeds).filter(Breeds.breedId==id).first()
        return row

    def my_generator(self):
        for i in range(120):
            row = dbsession.query(Breeds).filter(Breeds.breedId == i).first()
            row.cover = str(i) + '.jpg'
            print(row)
            dbsession.commit()

if __name__ == '__main__':
    # breeds = Breeds()
    # result = breeds.find_all_breed()
    # print(result)
    # Breeds().my_generator()
    pass
