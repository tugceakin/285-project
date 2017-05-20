from db import db, Symbol, SymbolValue
from datetime import date

print 'dropping tables'
db.drop_all()

print 'creating db'
db.create_all()

print 'creating symbols'
with open('stocks.txt', 'r') as f:
    for line in f:
        db.session.add(Symbol(symbol=line.strip(), symbol_type='STOCK'))

with open('etfs.txt', 'r') as f:
    for line in f:
        db.session.add(Symbol(symbol=line.strip(), symbol_type='ETF'))

with open('index.txt', 'r') as f:
    for line in f:
        db.session.add(Symbol(symbol=line.strip(), symbol_type='ETF', index=True))

with open('quality.txt', 'r') as f:
    for line in f:
        db.session.add(Symbol(symbol=line.strip(), symbol_type='STOCK', quality=True))

with open('ethical.txt', 'r') as f:
    for line in f:
        db.session.add(Symbol(symbol=line.strip(), symbol_type='STOCK', ethical=True))

for a in Symbol.query.all():
    print a.id, a.symbol, a.symbol_type, a.index
