from . import db


class Record(db.Model):
    __tablename__ = 'Record'
    id = db.Column(db.Integer, primary_key=True)
    press = db.Column(db.String(64))
    users = db.Column(db.String(64))
    date = db.Column(db.DATETIME())
    VoteId = db.Column(db.Integer,db.ForeignKey('VoteLog.id'))

    def __repr__(self):
        return '<Record %r>' % self.press

    def to_json(self):
        return {
            'id': self.id,
            'press': self.press,
            'users': self.users,
        }



class VoteLog(db.Model):
    __tablename__ = 'VoteLog'
    id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.String(64))
    date = db.Column(db.DATETIME())
    count = db.Column(db.String(1024),nullable=True)

    def __repr__(self):
        return '<VoteLog %r>' % self.result

    def to_json(self):
        return {
            'id': self.id,
            'result': self.result,
            'count': self.count,
        }