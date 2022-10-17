# Copyright 2015 Google Inc.
from datetime import datetime
#from typing_extensions import NotRequired
#from enum import unique
from flask import Flask
from sqlalchemy.sql.elements import between
from flask_sqlalchemy import SQLAlchemy
#from config import SECRET_KEY
from sqlalchemy import desc

builtin_list = list

from intWeb import db
#db = SQLAlchemy()

def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)

def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data


class Acc(db.Model):
    __tablename__ = 'Acc'
    id= db.Column(db.Integer,primary_key=True)
    acno = db.Column(db.BigInteger,unique=True,nullable=False)
    acc= db.Column(db.String(160))
    orderNo= db.Column(db.String(80))
    regSDate= db.Column(db.DateTime, nullable=False,default=datetime.utcnow) 
    regEdate= db.Column(db.DateTime) 
    voucherNo= db.Column(db.String(80))
    vendor= db.Column(db.String(80))
    total=db.Column(db.Integer)
    describ=db.Column(db.Text)
    readonly=db.Column(db.Integer,default=0)
    createdById = db.Column(db.String(255))    
    Path=db.Column(db.String(80))
    imageUrl = db.Column(db.String(255))    
    ctime = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)  #创建时间
    utime = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)  #更新时间
    
    def __init__(self, acno=None, acc=None, orderNo=None, regSDate=None,voucherNo=None,vendor=None,total=None,describ=None,createdById=None,imageUrl=None,Path=None):
        self.acno=acno
        self.acc=acc
        self.orderNo=orderNo
        self.regSDate=regSDate
        self.voucherNo=voucherNo
        self.vendor=vendor
        self.createdById=createdById
        self.imageUrl=imageUrl
        self.total=total
        self.describ=describ
        self.Path=Path
    def __repr__(self):
        return "<acc(accno='%s', acc=%s)" % (self.accno, self.acc)    

##############################################
def list(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Acc.query
             #.filter_by(Open=1)
             .order_by(Acc.id)
             .limit(limit)
             .offset(cursor))
    lessons = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(lessons) == limit else None
    return (lessons, next_page)

def list_desc(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Acc.query
             #.filter_by(Open=1)
             .order_by(desc(Acc.id))
             .limit(limit)
             .offset(cursor))
    lessons = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(lessons) == limit else None
    return (lessons, next_page)


# [START list_by_user]
def list_by_user(user_id, limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Acc.query
             .filter_by(createdById=user_id)
             .order_by(Acc.id)
             .limit(limit)
             .offset(cursor))
    lessons = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(lessons) == limit else None
    return (lessons, next_page)
# [END list_by_user]


def read(id):
    result = Acc.query.get(id)
    if not result:
        return None
    return from_sql(result)

def create(data):
    acc = Acc(**data)
    db.session.add(acc)
    db.session.commit()
    return from_sql(acc)

def update(data, id):
    acc = Acc.query.get(id)
    for k, v in data.items():
        setattr(acc, k, v)
    db.session.commit()
    return from_sql(acc)

def delete(id):
    Acc.query.filter_by(id=id).delete()
    db.session.commit()

class Item(db.Model):
    __tablename__ = 'Item'    
    id = db.Column(db.Integer,primary_key=True)
    itemno=db.Column(db.BigInteger,unique=True,nullable=True) # 物品編號
    name = db.Column(db.String(80))  # 產品
    model= db.Column(db.String(80))  # 型號
    sn = db.Column(db.String(80))    # SN/PN
    quantity= db.Column(db.Integer)  # 數量
    price = db.Column(db.Integer)    # 單價
    adjust= db.Column(db.Integer)    # 攤折
    amount= db.Column(db.Integer)    # 淨值
    depr_ed= db.Column(db.Integer)    # 淨攤
                                     # 資助金額
                                     # 資助單位/個人
    insure =db.Column(db.String(80))   # 保險 X

    keeper=db.Column(db.String(80))  # 移動 history
    note1=db.Column(db.Text)  # 地方

    note2=db.Column(db.Text)  # 資助
    
    # status
    lebalmark= db.Column(db.String(80))   # 標籤
    inventory= db.Column(db.String(80))   # 清查
    # ICT
    hostname= db.Column(db.String(80)) 	
    wifi_mac= db.Column(db.String(80)) 	
    lan_mac	= db.Column(db.String(80)) 
    wifi_mac_style2	= db.Column(db.String(80)) 
    lan_mac_sytle_2	= db.Column(db.String(80)) 
    cpu 	= db.Column(db.String(80)) 
    ram	= db.Column(db.String(80)) 
    disk= db.Column(db.String(80)) 
    accyear	= db.Column(db.String(80)) 
    # ItemType
    itemTypeId = db.Column(db.Integer)
    # Acc
    # acno
    regSDate= db.Column(db.DateTime, nullable=False,default=datetime.utcnow) 
    acc_acno = db.Column(db.BigInteger, db.ForeignKey('Acc.acno'), nullable=False)
    acc = db.relationship('Acc',  backref=db.backref('Item', lazy=True))
    createdById = db.Column(db.String(255))    
    Path=db.Column(db.String(80))
    imageUrl = db.Column(db.String(255))    
    ctime = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)  #创建时间
    utime = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)  #更新时间
    describ = db.Column(db.Text)

    def __init__(self, 
                 itemno=None,
                 name=None,
                 model=None,
                 sn=None,
                 quantity=None,
                 price=None,
                 adjust=None,
                 amount=None,
                 depr_ed=None,
                 insure=None,
                 keeper=None,
                 note1=None,
                 note2=None,
                 acc_acno=None,
                 regSDate=None,
                 lebalmark=None,
                 inventory=None,
                 Path=None,
                 imageUrl=None,
                 createdById=None,
                 itemTypeId=None,
                 hostname= None,
                 wifi_mac= None,
                 lan_mac	=None,
                 wifi_mac_style2	=None,
                 lan_mac_sytle_2	=None,
                 cpu 	=None,
                 ram	=None,
                 disk=None,
                 accyear	=None,
                describ=None
                 ):
        self.itemno =itemno
        self.name =name
        self.model =model
        self.sn =sn
        self.quantity =quantity
        self.price =price
        self.adjust = adjust
        self.amount = amount
        self.adjust = adjust
        self.depr_ed = depr_ed
        self.insure=insure
        self.keeper=keeper
        self.note1=note1
        self.note2=note2
        self.acc_acno=acc_acno
        self.regSDate=regSDate
        self.lebalmark=lebalmark
        self.inventory=inventory        
        self.Path=Path
        self.imageUrl=imageUrl
        self.createdById=createdById
        self.itemTypeId=itemTypeId
        self.hostname= hostname
        self.wifi_mac= wifi_mac
        self.lan_mac	=lan_mac	
        self.wifi_mac_style2	=wifi_mac_style2	
        self.lan_mac_sytle_2	=lan_mac_sytle_2	
        self.cpu 	=cpu 	
        self.ram	=ram	
        self.disk=disk
        self.accyear=accyear	
        self.describ=describ

    def __repr__(self):
        return "<item(name='%s')" % (self.name)    


##############################################
def locationitemlist_desc(roomid,buwei=1000000, limit=500,cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Item.query
             .filter(Item.note1.like(f"%{roomid}%"))
             .order_by(desc(Item.itemno))
             #.limit(limit)
             #.offset(cursor)
             )
    lessons = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(lessons) == limit else None
    return (lessons, next_page)

def snitemlist_desc(sn,buwei=1000000, limit=10,cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Item.query
             .filter(Item.sn.like(f"%{sn}%"))
             .order_by(desc(Item.itemno))
             .limit(limit)
             .offset(cursor))
    lessons = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(lessons) == limit else None
    return (lessons, next_page)

def modelitemlist_desc(model,buwei=1000000, limit=10,cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Item.query
             .filter(Item.model.like(f"%{model}%"))
             .order_by(desc(Item.itemno))
             .limit(limit)
             .offset(cursor))
    lessons = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(lessons) == limit else None
    return (lessons, next_page)



def categoryitemlist_desc(cateid,buwei=1000000, limit=10,cursor=None):
    cursor = int(cursor) if cursor else 0
    sint=int(cateid)*buwei
    print(sint)
    query = (Item.query
             .filter(Item.itemno.between(sint,sint+buwei-1))
             .order_by(desc(Item.itemno))
             .limit(limit)
             .offset(cursor))
    lessons = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(lessons) == limit else None
    return (lessons, next_page)



def Itemlist_by_acno(acc_acno):
    query = (Item.query
             .filter_by(acc_acno=acc_acno)
             .order_by(Item.id))
    lessons = builtin_list(map(from_sql, query.all()))
    return (lessons)

def Itemlist(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Item.query
             #.filter_by(Open=1)
             .order_by(Item.id)
             .limit(limit)
             .offset(cursor))
    lessons = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(lessons) == limit else None
    return (lessons, next_page)

def Itemlist_desc(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Item.query
             #.filter_by(Open=1)
             .order_by(desc(Item.id))
             .limit(limit)
             .offset(cursor))
    lessons = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(lessons) == limit else None
    return (lessons, next_page)


# [START list_by_user]
def Itemlist_by_user(user_id, limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Item.query
             .filter_by(createdById=user_id)
             .order_by(Item.id)
             .limit(limit)
             .offset(cursor))
    lessons = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(lessons) == limit else None
    return (lessons, next_page)
# [END list_by_user]



def readItem(id):
    result = Item.query.get(id)
    if not result:
        return None
    return from_sql(result)

def createItem(data):
    acc = Item(**data)
    db.session.add(acc)
    db.session.commit()
    return from_sql(acc)

def updateItem(data, id):
    acc = Item.query.get(id)
    for k, v in data.items():
        setattr(acc, k, v)
    db.session.commit()
    return from_sql(acc)

def deleteItem(id):
    Item.query.filter_by(id=id).delete()
    db.session.commit()

def readAllFromTable(tablename):
    if tablename=="acc":
        query = (Acc.query
                 .order_by(Acc.id))
        lessons = builtin_list(map(from_sql, query.all()))
        return (lessons)

    elif  tablename=="item":
        query = (Item.query
                 .order_by(Item.id))
        lessons = builtin_list(map(from_sql, query.all()))
        return (lessons)
    return None
##############################################
#class ItemType(db.Model):
#    __tablename__ = 'ItemType'    
#    """    所有资产的共有数据表    """
#    itemTypeId = db.Column(db.Integer,primary_key=True)
#    itemTypeName = db.Column(db.String(80),unique=True,nullable=False)
#    pk=db.Column(db.Integer)
#    sk=db.Column(db.Integer)
#    leaf=db.Column(db.Integer)
#    describ=db.Column(db.Text)
#    def __init__(self, itemTypeName=None, pk=None, sk=None, leaf=None, nodescribte=None):
#        self.itemType=itemTypeName
#        self.pk=pk
#        self.sk=sk
#        self.leaf=leaf
#        self.describ=nodescribte
#    def __repr__(self):
#        return "<itemType(itemType='%s')" % (self.itemType)    
#
#class Area(db.Model):
#    __tablename__ = 'Area'
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String(80),unique=True,nullable=False) #"区域"
#    subnet = db.Column(db.String(80))                          # ip subent 
#    describ = db.Column(db.Text)
#    def __init__(self, name=None):
#        self.name=name
#    def __repr__(self):
#        return "<Area(name)='%s')" % (self.name)    
#
#class Manufacturer(db.Model):
#    __tablename__ = 'Manufacturer'
#    id = db.Column(db.Integer, primary_key=True)
#    name =db.Column(db.String(80),unique=True,nullable=False)
#    contact = db.Column(db.String(80),unique=True,nullable=False)
#    phone =db.Column(db.String(80),unique=True,nullable=False)
#    describ = db.Column(db.Text)
#    def __init__(self, name=None):
#        self.name=name
#    def __str__(self):
#        return self.name
#
#class Belong(db.Model):
#    __tablename__ = 'Belong'    
#    id = db.Column(db.Integer, primary_key=True)
#    name =db.Column(db.String(80),unique=True,nullable=False)
#    describ = db.Column(db.Text)
#    def __init__(self, name=None):
#        self.name=name
#    def __str__(self):
#        return self.name

def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('../../config.py')
    init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
        """
        admin = User("admin","123","admin","1")
        studa = User("stu","123","stu","8","SC1A","01")
        studb = User("sta","123","stu","8","SC2A","01")
        db.session.add(admin)
        db.session.add(studa)
        db.session.add(studb)
        """
        db.session.commit()
    print("All tables created")

if __name__ == '__main__':
    _create_database()

