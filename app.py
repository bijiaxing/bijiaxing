from datetime import datetime
import os,time,json
from flask import Flask, request,jsonify
from flask import render_template
from flask_cors import CORS
import readvec 
from qsresouce import *
import pickle
import tulingbot

Ecommerce_queList=[]
Ecommerce_ansList=[]
Logistics_queList=[]
Logistics_ansList=[]
Hotel_queList=[]
Hotel_ansList=[]
#语料列表声明

readQSresouce('corpus/ecommerce.txt',Ecommerce_queList,Ecommerce_ansList)#读取电商沙盘语料库
readQSresouce('corpus/logistics.txt',Logistics_queList,Logistics_ansList)#读取物流沙盘语料库
readQSresouce('corpus/hotel.txt',Hotel_queList,Hotel_ansList)#读取物流沙盘语料库
#语料读取

StopWord_list=[]
readQSresouce('corpus/stopword.txt',StopWord_list,StopWord_list)
Temp_list=["告诉" , "请问" , "我" , "什么" , "是" ," " ,"呀", "到底","，","？","?",".","。", "可不可以","的","该","如何","进行","吗","说","讲" ,"么" ,"谈" ,"干什么", "是否", "请", "会","怎么办","到底","应该","怎么样", "怎么","做","应该","这",
  "才能","达到","呢", "用来","可以","干","啥"]
StopWord_list.extend(Temp_list)
#停用词读取

with open('embedding.pickle', 'rb') as handle:
    vectors = pickle.load(handle)
# 用vectors从embedding.pickle中读取全部词向量

app = Flask(__name__)
CORS(app)

@app.route("/",methods=['GET'])
def login():
    return render_template("login.html")

@app.route("/check",methods=['post'])
def check():
    username = request.form['username']
    password = request.form['password']
    if username=='admin' and password=='password':
        return render_template('qsSystem.html')
    return render_template("login.html",answer="wrong")

@app.route("/question",methods=['post'])
def add():
    ques=request.form['question'].replace('\n','')#去除回车
    ans=request.form['answer'].replace('\n','')
    Ecommerce_queList.append(ques)
    Ecommerce_ansList.append(ans)
    file1=open("ecommerce.txt","a")
    file1.write('\n')
    file1.write(ques)
    file1.write('\n')
    file1.write(ans)
    file1.close()
    return render_template('qsSystem.html',answer="success")


#电商沙盘机器人接口
@app.route("/chatbot")
def chat():
    tmpcontent = request.args.get('content')
    content=tmpcontent.replace('\n','')
    answer=readvec.similarityCheck(content,vectors,Ecommerce_queList,Ecommerce_ansList)
    if answer==None:
        answer=tulingbot.get_answer(content)
    file1=open("Log/HistoryEcommerce.txt","a")
    file1.write(content)
    file1.write('\n')
    file1.write(answer)
    file1.close()
    print(content)
    print(answer)
    return  json.dumps({'as':answer}) 
#酒店沙盘机器人接口
@app.route("/hotel")
def hotel():
    tmpcontent = request.args.get('content')
    content=tmpcontent.replace('\n','')
    answer=readvec.similarityCheck(content,vectors,Hotel_queList,Hotel_ansList)
    if answer==None:
        answer=tulingbot.get_answer(content)
    file2=open("Log/HistoryHotel.txt","a")
    file2.write(content)
    file2.write('\n')
    file2.write(answer)
    file2.close()
    print(content)
    print(answer)
    return  json.dumps({'as':answer}) 

#物流沙盘机器人接入口
@app.route("/logistics")
def logistics():
    tmpcontent = request.args.get('content')
    content=tmpcontent.replace('\n','')
    answer=readvec.similarityCheck(content,vectors,Logistics_queList,Logistics_ansList)
    if answer==None:
        answer=tulingbot.get_answer(content)
    file3=open("Log/HistoryLogistics.txt","a")
    file3.write(content)
    file3.write('\n')
    file3.write(answer)
    file3.close()
    print(content)
    print(answer)
    return  json.dumps({'as':answer}) 



if __name__ == '__main__':
    #app.run()
    app.run(debug=True)
    #debug=True,debug模式会产生双倍的内存消耗



# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 80))
#     app.run(host='0.0.0.0', port=port, debug=True)#coding:utf8

