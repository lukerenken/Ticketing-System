import datetime

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('ticket.db')

#User Object
class User(UserMixin, Model):
    first_name = CharField()
    last_name = CharField()
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)
    
    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)

    def get_tickets(self):
        return Ticket.select().where(Ticket.user == self)



    @classmethod
    def create_user(cls, username, email, password, first_name, last_name, admin=False):
        try:
            with DATABASE.transaction():
                cls.create(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                    is_admin=admin)
        except IntegrityError:
            raise ValueError("User already exists")


# Ticket Object
class Ticket(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    ticket_number = IntegerField(unique=True)
    user = ForeignKeyField(
        rel_model=User,
        related_name='tickets'
    )
    equipment_type = CharField()
    equipment_brand = CharField()
    equipment_location = CharField()
    department = CharField()
    description_of_problem = TextField()
    update = TextField(null=True)
    sign_of_damage = BooleanField(default=False)
    is_closed = BooleanField(default=False)
    last_edited_by = CharField()

    class Meta:
        database = DATABASE
        order_by = ('-ticket_number',)

    def create(cls, equipment_type, equipment_brand, equipment_location, timestamp, ticket_number,
                      department, description_of_problem, sign_of_damage, user, last_edited_by):
        try:
            with DATABASE.transaction():
                cls.create(
                    timestamp=datetime.datetime.now(),
                    ticket_number=int(timestamp.strftime('%y%m%d%H%S')),
                    equipment_type=equipment_type,
                    equipment_brand=equipment_brand,
                    equipment_location=equipment_location,
                    department=department,
                    description_of_problem=description_of_problem,
                    sign_of_damage=sign_of_damage,
                    last_edited_by=user
                )
        except IntegrityError:
            raise ValueError("A ticket with that number already exists")



def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Ticket], safe=True)
    DATABASE.close()