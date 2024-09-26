from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from flask_login import *

class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)


class Influencer(db.Model, UserMixin):
    __tablename__ = 'influencer'
    influencer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.Integer(), nullable=False)
    category = db.Column(db.String, nullable=True)
    reach = db.Column(db.String, nullable=True)
    platform = db.Column(db.String, nullable=True)
    website = db.Column(db.String, nullable=True)
    status = db.Column(db.String, nullable=True)
    ratings = db.Column(db.Float, nullable=True)
    ads = db.relationship('Ads', back_populates='influencer',
                          cascade="all, delete-orphan")



class Sponsor(db.Model, UserMixin):
    __tablename__ = 'sponsor'
    sponsor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.Integer(), nullable=False)
    category = db.Column(db.String, nullable=True)
    bname = db.Column(db.String, nullable=False)
    web = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    spending = db.Column(db.Integer, nullable=True)
    ratings = db.Column(db.Float, nullable=True)
    status = db.Column(db.String, nullable=True)
    campaigns = db.relationship(
        'Campaigns', back_populates='sponsor', cascade="all, delete-orphan")
    ads = db.relationship('Ads', back_populates='sponsor',
                          cascade="all, delete-orphan")



class Campaigns(db.Model):
    __tablename__ = 'campaigns'
    campaign_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)
    goals = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    visibility = db.Column(db.String, nullable=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.sponsor_id'))
    sponsor = db.relationship('Sponsor', back_populates='campaigns')
    ads = db.relationship('Ads', back_populates='campaign')


class Ads(db.Model):
    __tablename__ = 'ads'
    ad_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey(
        'campaigns.campaign_id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey(
        'influencer.influencer_id'), nullable=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey(
        'sponsor.sponsor_id'), nullable=False)
    name = db.Column(db.String, nullable=False, unique=True)
    requirements = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    
    payment = db.Column(db.Integer, nullable=False)
    campaign = db.relationship('Campaigns', back_populates='ads')
    influencer = db.relationship('Influencer', back_populates='ads')
    sponsor = db.relationship('Sponsor', back_populates='ads')

