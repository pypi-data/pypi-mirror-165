#------------------------------------------------------------------------------
# Creates database connection
# Defines models for database tables
#------------------------------------------------------------------------------

from peewee import *
from playhouse.mysql_ext import JSONField
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

#------------------------------------------------------------------------------
# Database connection object - initialised later
#------------------------------------------------------------------------------
#db = SqliteDatabase(None)
db = MySQLDatabase(None)

#------------------------------------------------------------------------------
# Base Class
#------------------------------------------------------------------------------
class BaseModel(Model):
    class Meta:
        database = db

#------------------------------------------------------------------------------
# Node Table
#------------------------------------------------------------------------------
class Node(BaseModel):
    name = CharField(unique=True)
    environment = CharField(null=True)
    hostname = CharField(null=True)    
    enabled = BooleanField()

#------------------------------------------------------------------------------
# Group Table
#------------------------------------------------------------------------------
class Group(BaseModel):
    name = CharField(unique=True)
    type = IntegerField(null=True)

#------------------------------------------------------------------------------
# Role Table
#------------------------------------------------------------------------------
class Role(BaseModel):
    name = CharField(unique=True)

#------------------------------------------------------------------------------
# Role Items Table
#------------------------------------------------------------------------------
class RoleItem(BaseModel):
    role_id = IntegerField(null=False)
    item = CharField(null=False)

#------------------------------------------------------------------------------
# Node/Group Membership Table
#------------------------------------------------------------------------------
class GroupNodeMembership(BaseModel):
    group = ForeignKeyField(Group, backref='group_nodes')
    node = ForeignKeyField(Node, backref='node_groups')

#------------------------------------------------------------------------------
# Role/Node Relationship Table
#------------------------------------------------------------------------------
class NodeRoleRelationship(BaseModel):
    node = ForeignKeyField(Node, backref='node_roles')
    role = ForeignKeyField(Role, backref='role_nodes')

#------------------------------------------------------------------------------
# Role/Group Relationship Table
#------------------------------------------------------------------------------
class GroupRoleRelationship(BaseModel):
    group = ForeignKeyField(Group, backref='group_roles')
    role = ForeignKeyField(Role, backref='role_groups')

#------------------------------------------------------------------------------
# Custom Fact Tables
#------------------------------------------------------------------------------
class CustomFact(BaseModel):
    name = CharField(unique=True)
    has_valid_values = BooleanField()

class CustomFactValue(BaseModel):
    fact_id = IntegerField(null=False)
    value = CharField(null=False)

class CustomFactNodeValue(BaseModel):
    node_id = ForeignKeyField(Node, backref='node_facts')
    fact_name = CharField(null=False)
    fact_value = CharField(null=False)
    fact_type = IntegerField(null=False)

#------------------------------------------------------------------------------
# Dynamic Group Tables
#------------------------------------------------------------------------------
class DynamicGroupCriteria(BaseModel):
    group_id = ForeignKeyField(Group, backref='group_dg_criteria')
    fact_name = CharField(null=False)
    fact_values = CharField(null=False)

class DynamicGroupMembership(BaseModel):
    group_id = ForeignKeyField(Group, backref='group_dg_nodes')
    node_id = ForeignKeyField(Node, backref='node_dg_groups')
    
#------------------------------------------------------------------------------
# User Table
#------------------------------------------------------------------------------
class User(BaseModel, UserMixin):
    username = CharField(null=False, unique=True)
    password_hash = CharField(null=False)
    full_name = CharField(null=False)
    user_type = IntegerField(null=False)
    enabled = IntegerField(null=False)
    mfa = IntegerField(null=False)

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

#------------------------------------------------------------------------------
# Config Table
#------------------------------------------------------------------------------
class Config(BaseModel):
    name = CharField(null=False, unique=True)
    kill_switch = BooleanField()
    
#------------------------------------------------------------------------------
# Container Table
#------------------------------------------------------------------------------
class Container(BaseModel):
    name = CharField(null=False, unique=True)
    last_status = BooleanField(null=False)
    last_runtime = DateTimeField(null=False)

#------------------------------------------------------------------------------
# Node Reports Table
#------------------------------------------------------------------------------
class NodeReports(BaseModel):
    node_id = ForeignKeyField(Node, backref='node_reports')
    status = CharField(null=False)
    start_time = DateTimeField(null=False)
    end_time = DateTimeField(null=False)
    puppet_version = CharField(null=False)
    skips = IntegerField(null=False)
    successes = IntegerField(null=False)
    failures = IntegerField(null=False)
    event_data = JSONField()

#------------------------------------------------------------------------------
# Node Puppet Facts Table
#------------------------------------------------------------------------------
class NodePuppetFacts(BaseModel):
    node_id = ForeignKeyField(Node, backref='node_puppet_facts')
    osfamily = CharField(null=False)
    os_name = CharField(null=False)
    release_full = CharField(null=False)
    release_major = CharField(null=False)
    release_minor = CharField(null=False)
    release_description = CharField(null=False)
    kernelrelease = CharField(null=False)
    kernelmajversion = CharField(null=False)

#------------------------------------------------------------------------------
# Node Overrides Table
#------------------------------------------------------------------------------
class NodeOverrides(BaseModel):
    node_id = ForeignKeyField(Node, backref='node_overrides')
    hiera_variable = CharField(null=False)
    hiera_value = CharField(null=False)
