from flask import render_template,request,jsonify
from . import main
from .. import db
from ..models import Record,VoteLog
import json,time,datetime



@main.route('/record', methods=['GET', 'POST'])
def dataentry():

    if request.form.get('user'):
        Vote = (request.form.get('vote'))
        NewDanmu = Record(users=request.form.get('user'),
                          press=request.form.get('press'),
                          date=datetime.datetime.now(),
                          VoteId=Vote)
        db.session.add(NewDanmu)
        db.session.commit()
    else:
        print("录入失败")
        return "0"

@main.route('/record/<int:id>', methods=['GET', 'POST'])
def recordShow(id):

    if id:
        out = []
        data = Record.query.filter(Record.id > id).all()
        for x in data:
            out.append(x.to_json())
        return jsonify(out)
    else:
        print("查询失败")
        return "0"

@main.route('/vote', methods=['GET', 'POST'])
def voteentry():
    if request.form.get('result'):
        NewVote = VoteLog(result=request.form.get('result'),
                          count=request.form.get('set'),
                          date=datetime.datetime.now())
        db.session.add(NewVote)
        db.session.commit()
        return str(NewVote.id)
    else:
        print("录入失败")
        return "0"

@main.route('/vote/<int:id>', methods=['GET', 'POST'])
def voteShow(id):
    if id:
        out = []
        data = VoteLog.query.filter(VoteLog.id > id).all()
        for x in data:
            out.append(x.to_json())
        return jsonify(out)
    else:
        print("查询失败")
        return "0"

@main.route('/countrecord/')
def data():
    data = Record.query.count()
    return str(data)


