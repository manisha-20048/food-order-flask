from flask import Flask,request,redirect,url_for,render_template,make_response
from datetime import datetime
app=Flask(__name__)
customers={}
orders={}
prices={'Biryani':100,'meals':150,'chicken':200,'dal':20,'curd_Rice':50}
@app.route('/')
def welcome():
    return render_template('welcome.html')
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=="POST":
        username=request.form['username']
        email=request.form['email']
        phno=request.form['phno']
        password=request.form['password']
        confirm_password=request.form['confirm_password']
        if password==confirm_password:
            if username not in customers:
                customers[username]={'Email':email,'Phno':phno,'Password':password,"Quantity":0,'pirce':0}
                return redirect(url_for('login'))
            else:
                return 'username already exists'
        else:
            return 'Password doesnot match to conform password'    

    return render_template('register.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        login_username=request.form['username']
        login_password=request.form['password']
        if login_username in customers:
            register_password=customers[login_username]['Password']
            if login_password==register_password:
                cookie=make_response (redirect (url_for('dashboard')))
                cookie.set_cookie('username',login_username)
                return cookie
            else:
                return 'password incorrect'
        else:
            return "username not exists"
    return render_template('login.html')
@app.route('/dashboard')
def dashboard():
    if request.cookies.get('username'):
        username=request.cookies.get('username')
        return render_template('dashboard.html',username=username)
@app.route('/food orders',methods=['GET','POST'])    
def food_order():
    if request.method=='POST':
        customer_name=request.form['name']
        phno=request.form['phno']
        Address=request.form['Address']
        item=request.form['item']
        quantity=int(request.form['quantity'])
        if customer_name not in orders:
            date=datetime.now().strftime("%d-%m-%Y")
            time=datetime.now().strftime("%H:%M:%S")
            if item in prices:
                price=int(prices[item])*int(quantity)
                orders[customer_name]={'Phno':phno,'Item':[],'Quantity':quantity,'total_price':price,'date':date,'time':time,'order_status':'','pay information':''}
                orders[customer_name]['Item'].append(item)
            else:
                return 'Order is not available'
        else:
            orders[customer_name]['Item'].append(item)
            orders[customer_name]['total_price']+=int(prices[item])
            return orders
    return render_template('food_order.html')
@app.route('/view_orders')
def view_orders():
        if orders:
            return orders
        return render_template('view_orders.html',orders=orders)
@app.route('/update_order_info',methods=['GET','POST'])
def update_order_info():
    if request.method=='POST':
        if orders:
            customer_name=request.form['customer_name']
            order_status='successfull'
            pay_information='payment succesfull'
            if customer_name in orders:
                orders[customer_name]['order_status']=order_status
                orders[customer_name]['pay information']=pay_information
                return orders[customer_name]
            else:
                return 'customer_name is not valid'
        else:
            return 'you not ordered yet'
    return render_template('update_order_info.html')
@app.route('/delete order',methods=['GET','POST'])
def delete_order():
    if request.method=='POST':
        customer_name=request.form['customer_name']
        if customer_name in orders:
            del orders[customer_name]
            return 'Deleted Succesfully' 
        else:
            return 'Customer is not orderd'
    return render_template('delete_order.html')   
@app.route('/logout',methods=['GET','POST'])
def logout():
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        if username in customers:
            del customers[username]
            return redirect (url_for('login'))
        else:
            return 'user name not exists'
    return render_template('logout.html')
@app.route('/delete Account',methods=['GET','POST'])
def delete_account():
    if request.method=='POST':
            username=request.cookies.get('username')
            if username in customers:
                customers.pop(username)
                resp=make_response(redirect(url_for('welcome')))
                resp.delete_cookie('username')
                return resp
            else:
                return 'please login to delete account'
    return render_template('delete_account.html')    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
