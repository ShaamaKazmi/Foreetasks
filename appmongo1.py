from flask import Flask,json
from flask import request,jsonify
import pymongo
from functools import wraps
app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
calculations = mydb["calculations"]
last_op = mydb["last_operations"]
def inverse(f):
	@wraps(f)
	def wrapperfunc(*args,**kwargs):
		req_data=request.get_json()
		op=req_data["op"]
		if op=='+':
    			request.json["op"]="-"
		elif op=='-':
			request.json["op"]="+"
		elif op=='*':
			request.json["op"]="/"
		elif op=='/':
			request.json["op"]=="*"
		return f(*args,**kwargs)

	return wrapperfunc
@app.route('/view')
def view_db():
	collist = mydb.list_collection_names()
	if "calculations" in collist:
		return "found"
	else:
		return "not found"
@app.route('/calc',methods=['POST'])
	
def calculator():
	req_data=request.json
	op1=req_data["op1"]
	op2=req_data["op2"]
	op=req_data["op"]
	if op=='+':
		res=op1+op2
	elif op=='-':
		res=op1-op2
	elif op=='*':
		res=op1*op2
	elif op=='/':
		if op2==0:
			error='undefined'
			return jsonify(error)
		else:
			res=op1/op2
	mydict={"op1":op1, "op2":op2, "op":op, "result":res}
	calculations.insert_one(mydict)
	last_op.delete_many({})
#	rec="Last OP table:<br>"
	for record in calculations.find({"op":"+"}).sort([("_id",-1)]).limit(4):
		last_op.insert_one(record)	
	for record in calculations.find({"op":"-"}).sort([("_id",-1)]).limit(4):
		last_op.insert_one(record)	
	for record in calculations.find({"op":"*"}).sort([("_id",-1)]).limit(4):
		last_op.insert_one(record)	
	for record in calculations.find({"op":"/"}).sort([("_id",-1)]).limit(4):
		last_op.insert_one(record)	
#	for record in last_op.find():
#		rec=rec+str(record)+"<br>"	

	return jsonify(result=res)

@app.route('/calculations',methods=['GET'])
def total_calc():
	output="Output:<br>"
	for x in calculations.find():
		output=output+str(x)+"<br>"
	y=calculations.find().count()
	output=output+"<br>Total_count:"+str(y)
	return output
	
if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5000)	
