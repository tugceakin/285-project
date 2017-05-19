import datetime
import json
from sqlalchemy_utils.types import choice

from app import db
from data import scrape_historical_data

def to_json(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    # add your coversions for things like datetime's 
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if isinstance(v, datetime.date):
            d[c.name] = v.strftime('%b %d, %Y')
        elif c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return json.dumps(d)

class Symbol(db.Model):

    __tablename__ = 'symbol'
    TYPES = (
        ('ETF', 'ETF'),
        ('STOCK', 'Stock'),
    )

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String)
    symbol_type = db.Column(choice.ChoiceType(TYPES))

    def get_historical_data(self):
        DAYS = 5
        dates = last_n_dates(DAYS)
        values_in_db = self.values.filter(db.and_(
            SymbolValue.date >= dates[-1],
            SymbolValue.date <= dates[0],
        ))
        if values_in_db.count() != DAYS:
            # Delete first because no upsert
            values_in_db.delete()
            # db.session.commit()
            for data in scrape_historical_data(self.symbol):
                self.values.append(SymbolValue(**data))
            # db.session.commit()
        values_in_db = self.values.filter(db.and_(
            SymbolValue.date >= dates[-1],
            SymbolValue.date <= dates[0],
        ))
        return values_in_db


    def repr(self):
        return '<Symbol {}:{}>'.format(self.id, self.symbol)

    def to_json(self):
        return to_json(self, self.__class__)

    def __unicode__(self):
        return '<Symbol {}:{}>'.format(self.id, self.symbol)


class SymbolValue(db.Model):

    __tablename__ = 'symbol_value'
    __table_args__ = (db.UniqueConstraint('date', 'symbol_id'),)

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    value = db.Column(db.Float)
    open = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    close = db.Column(db.Float)
    adj_close = db.Column(db.Float)
    volume = db.Column(db.String)
    symbol_id = db.Column(db.Integer, db.ForeignKey('symbol.id'))
    symbol = db.relationship('Symbol', backref=db.backref('values', lazy='dynamic'))

    def to_json(self):
        return to_json(self, self.__class__)

def last_n_dates(n):
    base = datetime.datetime.today().date()
    return [base - datetime.timedelta(days=x) for x in range(0, n)]
