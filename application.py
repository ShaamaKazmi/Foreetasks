from flask import Flask,json
from flask import request,jsonify
from functools import wraps
app = Flask(__name__)

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

	return wrapperfunc()
@app.route('/calc',methods=['POST'])
@inverse	
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
	return jsonify(result=res)
	
if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5000)	
