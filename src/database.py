from flask import Flask, jsonify, redirect, url_for, request, render_template
from flask_mysqldb import MySQL
from flask_cors import CORS
from datetime import datetime 
import logging
import mysql.connector


app = Flask(__name__)
CORS(app)

# Configuration for MySQL
app.config['MYSQL_HOST'] = 'localhost'  # Hostname
app.config['MYSQL_USER'] = 'root'  # Username
app.config['MYSQL_PASSWORD'] = 'aishhil2125'  # Password
app.config['MYSQL_DB'] = 'oasis'  # Database name

mysql = MySQL(app)

@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name

@app.route('/')
def index():
    return render_template('index.html')

# ================
# Register Farmer
# ================

@app.route('/regfar', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        mobno = request.form['MobileNumber']
        accno = request.form['Accno']
        ifsc = request.form['IFSC']
        branch = request.form['branch']
        cur = mysql.connection.cursor()
        
        query = "INSERT INTO register_farmer (name, mobno, accno, ifsc, branch) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(query, (name, mobno, accno, ifsc, branch))
        mysql.connection.commit()
        
        # Get the last inserted token_id
        token_id = cur.lastrowid
        
        create_table_query = f"""
        CREATE TABLE token_{token_id} (
          date DATE NULL,
          amount_per_ltr DECIMAL(10, 2) NULL,
          quantity DECIMAL(10, 2) NULL,
          total_amount DECIMAL(10, 2) NULL
        );
        """
        cur.execute(create_table_query)
        mysql.connection.commit()
        cur.close()
        
        return f"""
        <script type="text/javascript"> 
        alert("Your Registration has been successful. TOKEN: '{token_id}'");
        </script>
        """
    else:
        name = request.args.get('name')
        return "success get " + name


# ==========
# Buy Milk
# =========

@app.route('/submitbuymilk', methods=['POST', 'GET'])
def submitbuymilk():
    if request.method == 'POST':
        token = request.form['FID']
        quantity = request.form['Quantity']
        amt = request.form['Amount']
        cur = mysql.connection.cursor()
        expense = int(quantity) * float(amt)
        
        try:
            query = f"INSERT INTO `oasis`.`token_{token}` (date, amount_per_ltr, quantity, total_amount) VALUES (CURDATE(), %s, %s, %s);"
            cur.execute(query, (amt, quantity, expense))
            mysql.connection.commit()
            
            update_expense_query = "UPDATE oasis.token_%s SET expense = expense + %s WHERE date = CURDATE()"
            cur.execute(update_expense_query, (token, expense))
            mysql.connection.commit()
        except Exception as e:
            print(f"ERROR: {e}")
  
        cur.close()
        return """
        <script type="text/javascript"> 
        alert("Successfully recorded");
        </script>
        """
    else:
        name = request.args.get('name')
        return "success get " + name


# =============
#farmertokenid
#amount
#pay_farmer
# =============
# Pay Farmer
@app.route('/submitpayfarmer', methods=['POST', 'GET'])
def submitpayfarmer():
    if request.method == 'POST':
        token_id = int(request.form['farmertokenid'])
        amount_paid = int(request.form['amount'])
        cur = mysql.connection.cursor()
        
        try:
            # Check if the token exists
            query = "SELECT COUNT(*) FROM register_farmer WHERE token_id = %s"
            cur.execute(query, (token_id,))
            result = cur.fetchone()
            if result[0] == 0:
                cur.close()
                return """
                    <script type="text/javascript"> 
                        alert("Error: The token ID does not exist.");
                        window.location.href = "/";
                    </script>
                """
            
            # Fetch the total amount and amount paid
            cur.execute(f"SELECT SUM(quantity * amount_per_ltr) FROM token_{token_id}")
            total_amount_result = cur.fetchone()
            total_amount = total_amount_result[0] if total_amount_result[0] else 0

            cur.execute("SELECT SUM(amount_paid) FROM pay_farmer WHERE token_id = %s", (token_id,))
            amount_paid_result = cur.fetchone()
            amount_paid_so_far = amount_paid_result[0] if amount_paid_result[0] else 0
            
            # Calculate the net amount
            net_amount = total_amount - amount_paid_so_far
            
            # If the payment exceeds the net amount, limit it and show a message
            if amount_paid > net_amount:
                amount_paid = net_amount
                message = "Payment exceeds the net amount owed. Paying only the remaining amount."
            else:
                message = "Successfully Paid."

            # Insert the payment record
            query = "INSERT INTO pay_farmer (token_id, amount_paid) VALUES (%s, %s)"
            cur.execute(query, (token_id, amount_paid))
            mysql.connection.commit()
            cur.close()
            return f"""
            <script type="text/javascript"> 
            alert("{message} Amount paid: {amount_paid}");
            </script>
            """
        except Exception as e:
            print(f"ERROR: {e}")
            return """
            <script type="text/javascript"> 
            alert("An error occurred.");
            </script>
            """
    else:
        name = request.args.get('name')
        return "success get " + name
    

# ================
# Milk Bifurcation
# ================

@app.route('/milkbifurcation', methods=['POST', 'GET'])
def milkbifurcation():
    if request.method == 'POST':
        loose_milk = request.form['Loose Milk']
        milk_for_product = request.form['Milk for Product']
        
        cur = mysql.connection.cursor()
        
        query = f"INSERT INTO milk_bifurcation(date, loose_milk, milk_for_product) VALUES (CURDATE(),{loose_milk},{milk_for_product});"
        cur.execute(query)
        mysql.connection.commit()
        
        # Get the last inserted token_id
        
        cur.close()
        
        return f"""
        <script type="text/javascript"> 
        alert("Recorded successfully.");
        </script>
        """
    else:
        name = request.args.get('name')
        return "success get " + name


# =============
# Show Farmers
# =============

@app.route('/api/data', methods=['GET'])
def get_farmer_data():
    cur = mysql.connection.cursor()
    cur.execute("SELECT token_id, name, mobno, accno, ifsc, branch FROM register_farmer")
    rows = cur.fetchall()
    
    data = []
    for row in rows:
        token_id = row[0]
        name = row[1]
        mobno = row[2]
        accno = row[3]
        ifsc = row[4]
        branch = row[5]

        # Fetch sum of quantity * amount_per_ltr from the token table
        try:
            cur.execute(f"SELECT SUM(quantity * amount_per_ltr) FROM token_{token_id}")
            total_amount_result = cur.fetchone()
            total_amount = total_amount_result[0] if total_amount_result[0] else 0
        except Exception as e:
            print(f"ERROR fetching from token_{token_id}: {e}")
            total_amount = 0

        # Fetch total amount paid to the farmer
        cur.execute("SELECT SUM(amount_paid) FROM pay_farmer WHERE token_id = %s", (token_id,))
        amount_paid_result = cur.fetchone()
        amount_paid = amount_paid_result[0] if amount_paid_result[0] else 0
        
        # Calculate the net amount
        net_amount = total_amount - amount_paid
        if net_amount < 0:
            net_amount = 0
        
        data.append({
            'token_id': token_id,
            'name': name,
            'mobno': mobno,
            'accno': accno,
            'ifsc': ifsc,
            'branch': branch,
            'net_amount': net_amount
        })
    
    cur.close()
    return jsonify(data)

# =============
# Show Overhead
# =============

@app.route('/showoverhead', methods=['GET'])
def get_overhead_data():
    cur = mysql.connection.cursor()

    cur.execute("SELECT date, expense_name, expense_amt, status FROM overhead")
    rows = cur.fetchall()
    
    data = []
    for row in rows:
        date = row[0]
        expense_name = row[1]
        expense_amt = row[2]
        status=row[3]
        
        data.append({
            'date': date,
            'expense_name': expense_name,
            'expense_amt': expense_amt,
            'status': status
        })
    
    cur.close()
    return jsonify(data)

# =============
# Show Logistics
# =============

@app.route('/showlogistics', methods=['GET'])
def get_logistics_data():
    cur = mysql.connection.cursor()

    cur.execute("SELECT date, expense_name, expense_amt, status FROM logistics")
    rows = cur.fetchall()
    
    data = []
    for row in rows:
        date = row[0]
        expense_name = row[1]
        expense_amt = row[2]
        status=row[3]
        
        data.append({
            'date': date,
            'expense_name': expense_name,
            'expense_amt': expense_amt,
            'status': status
        })
    
    cur.close()
    return jsonify(data)

# =========================
# Register vendor route...
# =========================
@app.route('/regven', methods=['POST'])
def regven():
    if request.method == 'POST':
        name = request.form['vendorName']
        enterprise = request.form['enterprise']
        gstno = request.form['GST']
        address = request.form['address']
        mobno = request.form['MobleNumber']
        cur = mysql.connection.cursor()
        query = "INSERT INTO `oasis`.`vendor` (`name`, `enterprise`, `gstno`, `address`, `mobno`,`amount`) VALUES ('%s',' %s', '%s', '%s', '%s',0.0); "% (name, enterprise, gstno, address, mobno)
        abc= cur.execute(query)
        mysql.connection.commit()

        x = cur.lastrowid
        print(x)
        query = """CREATE TABLE oasis.%s (
                date DATE NULL,
                MilkCM500Quan INT NULL,
                MilkCM200Quan INT NULL,
                MilkTM500Quan INT NULL,
                MilkTM200Quan INT NULL,
                Lassi200Quan INT NULL,
                LassiCUP200Quan INT NULL,
                LassiMANGOCUP200Quan INT NULL,
                Dahi200Quan INT NULL,
                Dahi500Quan INT NULL,
                Dahi2LTQuan INT NULL,
                Dahi5LTQuan INT NULL,
                Dahi10LTQuan INT NULL,
                Dahi2LTQuan15 INT NULL,
                Dahi5LTQuan15 INT NULL,
                Dahi10LTQuan15 INT NULL,
                ButtermilkQuan INT NULL,
                Khova500Quan INT NULL,
                Khoya1000Quan INT NULL,
                Shrikhand100Quan INT NULL,
                Shrikhand250Quan INT NULL,
                Ghee200Quan INT NULL,
                Ghee500Quan INT NULL,
                Ghee15LTQuan INT NULL,
                PaneerlooseQuan INT NULL,
                khovalooseQuan INT NULL);""" %x

        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return f"""<script type="text/javascript"> 
        alert("Your Registration has been successful. TOKEN : '{x}");
        </script>"""
    else:
        name = request.args.get('name')
        return "success get " + name

# Product prices route...
@app.route('/productprices', methods=['POST'])
def productprices():
    if request.method == 'POST':
        vendorId = request.form['vendorId']
        MilkCM500Price = request.form['MilkCM500Price']
        MilkCM200Price = request.form['MilkCM200Price']
        MilkTM500Price = request.form['MilkTM500Price']
        MilkTM200Price = request.form['MilkTM200Price']
        Lassi200Price = request.form['Lassi200Price']
        LassiCUP200Price = request.form['LassiCUP200Price']
        LassiMANGOCUP200Price = request.form['LassiMANGOCUP200Price']
        Dahi200Price = request.form['Dahi200Price']
        Dahi500Price = request.form['Dahi500Price']
        Dahi2LTPrice = request.form['Dahi2LTPrice']
        Dahi5LTPrice = request.form['Dahi5LTPrice']
        Dahi10LTPrice = request.form['Dahi10LTPrice']
        Dahi2LTPrice15 = request.form['Dahi2LTPrice15']
        Dahi5LTPrice15 = request.form['Dahi5LTPrice15']
        Dahi10LTPrice15 = request.form['Dahi10LTPrice15']
        ButtermilkPrice = request.form['ButtermilkPrice']
        Khova500Price = request.form['Khova500Price']
        Khoya1000Price = request.form['Khoya1000Price']
        Shrikhand100Price = request.form['Shrikhand100Price']
        Shrikhand250Price = request.form['Shrikhand250Price']
        Ghee200Price = request.form['Ghee200Price']
        Ghee500Price = request.form['Ghee500Price']
        Ghee15LTPrice = request.form['Ghee15LTPrice']
        PaneerloosePrice = request.form['PaneerloosePrice']
        khovaloosePrice = request.form['khovaloosePrice']

        cur = mysql.connection.cursor()
        query = """
        INSERT INTO oasis.product_prices (
            vendorId, MilkCM500Price, MilkCM200Price, MilkTM500Price, MilkTM200Price, 
            Lassi200Price, LassiCUP200Price, LassiMANGOCUP200Price, 
            Dahi200Price, Dahi500Price, Dahi2LTPrice, Dahi5LTPrice, Dahi10LTPrice, 
            Dahi2LTPrice15, Dahi5LTPrice15, Dahi10LTPrice15, 
            ButtermilkPrice, Khova500Price, Khoya1000Price, 
            Shrikhand100Price, Shrikhand250Price, 
            Ghee200Price, Ghee500Price, Ghee15LTPrice, 
            PaneerloosePrice, khovaloosePrice
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(query, (
            vendorId, MilkCM500Price, MilkCM200Price, MilkTM500Price, MilkTM200Price, 
            Lassi200Price, LassiCUP200Price, LassiMANGOCUP200Price, 
            Dahi200Price, Dahi500Price, Dahi2LTPrice, Dahi5LTPrice, Dahi10LTPrice, 
            Dahi2LTPrice15, Dahi5LTPrice15, Dahi10LTPrice15, 
            ButtermilkPrice, Khova500Price, Khoya1000Price, 
            Shrikhand100Price, Shrikhand250Price, 
            Ghee200Price, Ghee500Price, Ghee15LTPrice, 
            PaneerloosePrice, khovaloosePrice
        ))
        mysql.connection.commit()
        cur.close()
        return f"""<script type="text/javascript"> 
        alert("Product prices have been successfully recorded.");
        </script>"""
    else:
        name = request.args.get('name')
        return "success get " + name


# New route to fetch data
@app.route('/showven', methods=['GET'])
def get_data():
    cur = mysql.connection.cursor()
    cur.execute("SELECT token, name, enterprise, gstno, address, mobno, amount FROM vendor")
    rows = cur.fetchall()
    cur.close()
    print(rows)
    
    # Convert to JSON-compatible format
    data = []
    for row in rows:
        data.append({
            'token': row[0],
            'name': row[1],
            'enterprise': row[2],
            'gstno': row[3],
            'address': row[4],
            'mobno': row[5],
            'amount': row[6],
        })
    
    return jsonify(data)

@app.route('/VendorStatus', methods=['GET'])
def get_product_prices():
    cur = mysql.connection.cursor()
    query = """
        SELECT 
            v.name,
            p.vendorId,
            p.MilkCM500Price,
            p.MilkCM200Price,
            p.MilkTM500Price,
            p.MilkTM200Price,
            p.Lassi200Price,
            p.LassiCUP200Price,
            p.LassiMANGOCUP200Price,
            p.Dahi200Price,
            p.Dahi500Price,
            p.Dahi2LTPrice,
            p.Dahi5LTPrice,
            p.Dahi10LTPrice,
            p.Dahi2LTPrice15,
            p.Dahi5LTPrice15,
            p.Dahi10LTPrice15,
            p.ButtermilkPrice,
            p.Khova500Price,
            p.Khoya1000Price,
            p.Shrikhand100Price,
            p.Shrikhand250Price,
            p.Ghee200Price,
            p.Ghee500Price,
            p.Ghee15LTPrice,
            p.PaneerloosePrice,
            p.khovaloosePrice
        FROM 
            vendor v
        JOIN 
            product_prices p ON v.token = p.vendorId;
    """
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    
    # Convert to JSON-compatible format
    data = []
    for row in rows:
        data.append({
            'name': row[0],
            'vendorId': row[1],
            'MilkCM500Price': row[2],
            'MilkCM200Price': row[3],
            'MilkTM500Price': row[4],
            'MilkTM200Price': row[5],
            'Lassi200Price': row[6],
            'LassiCUP200Price': row[7],
            'LassiMANGOCUP200Price': row[8],
            'Dahi200Price': row[9],
            'Dahi500Price': row[10],
            'Dahi2LTPrice': row[11],
            'Dahi5LTPrice': row[12],
            'Dahi10LTPrice': row[13],
            'Dahi2LTPrice15': row[14],
            'Dahi5LTPrice15': row[15],
            'Dahi10LTPrice15': row[16],
            'ButtermilkPrice': row[17],
            'Khova500Price': row[18],
            'Khoya1000Price': row[19],
            'Shrikhand100Price': row[20],
            'Shrikhand250Price': row[21],
            'Ghee200Price': row[22],
            'Ghee500Price': row[23],
            'Ghee15LTPrice': row[24],
            'PaneerloosePrice': row[25],
            'khovaloosePrice': row[26]
        })
    
    return jsonify(data)

# ===================
# Sell products and calculate total
# ===================
@app.route('/sellproducts', methods=['POST'])
def sellproducts():
    if request.method == 'POST':
        try:
            vendorId = request.form['vendorId']
            MilkCM500Quan = int(request.form['MilkCM500Quan'])
            MilkCM200Quan = int(request.form['MilkCM200Quan'])
            MilkTM500Quan = int(request.form['MilkTM500Quan'])
            MilkTM200Quan = int(request.form['MilkTM200Quan'])
            Lassi200Quan = int(request.form['Lassi200Quan'])
            LassiCUP200Quan = int(request.form['LassiCUP200Quan'])
            LassiMANGOCUP200Quan = int(request.form['LassiMANGOCUP200Quan'])
            Dahi200Quan = int(request.form['Dahi200Quan'])
            Dahi500Quan = int(request.form['Dahi500Quan'])
            Dahi2LTQuan = int(request.form['Dahi2LTQuan'])
            Dahi5LTQuan = int(request.form['Dahi5LTQuan'])
            Dahi10LTQuan = int(request.form['Dahi10LTQuan'])
            Dahi2LTQuan15 = int(request.form['Dahi2LTQuan15'])
            Dahi5LTQuan15 = int(request.form['Dahi5LTQuan15'])
            Dahi10LTQuan15 = int(request.form['Dahi10LTQuan15'])
            ButtermilkQuan = int(request.form['ButtermilkQuan'])
            Khova500Quan = int(request.form['Khova500Quan'])
            Khoya1000Quan = int(request.form['Khoya1000Quan'])
            Shrikhand100Quan = int(request.form['Shrikhand100Quan'])
            Shrikhand250Quan = int(request.form['Shrikhand250Quan'])
            Ghee200Quan = int(request.form['Ghee200Quan'])
            Ghee500Quan = int(request.form['Ghee500Quan'])
            Ghee15LTQuan = int(request.form['Ghee15LTQuan'])
            PaneerlooseQuan = int(request.form['PaneerlooseQuan'])
            khovalooseQuan = int(request.form['khovalooseQuan'])

            cur = mysql.connection.cursor()

            # Fetch product prices for the vendor
            query_prices = "SELECT * FROM oasis.product_prices WHERE vendorId = %s"
            cur.execute(query_prices, (vendorId,))
            prices = cur.fetchone()

            if not prices:
                return f"""<script type="text/javascript"> 
                alert("No product prices found for vendor ID '{vendorId}'");
                </script>"""

            _, MilkCM500Price, MilkCM200Price, MilkTM500Price, MilkTM200Price, Lassi200Price, LassiCUP200Price, LassiMANGOCUP200Price, \
            Dahi200Price, Dahi500Price, Dahi2LTPrice, Dahi5LTPrice, Dahi10LTPrice, Dahi2LTPrice15, Dahi5LTPrice15, Dahi10LTPrice15, \
            ButtermilkPrice, Khova500Price, Khoya1000Price, Shrikhand100Price, Shrikhand250Price, Ghee200Price, Ghee500Price, Ghee15LTPrice, \
            PaneerloosePrice, khovaloosePrice = prices

            # Calculate total amount
            total_amount = (
                MilkCM500Quan * MilkCM500Price +    MilkCM200Quan * MilkCM200Price + MilkTM500Quan * MilkTM500Price + 
                MilkTM200Quan * MilkTM200Price + Lassi200Quan * Lassi200Price + LassiCUP200Quan * LassiCUP200Price + 
                LassiMANGOCUP200Quan * LassiMANGOCUP200Price + Dahi200Quan * Dahi200Price + Dahi500Quan * Dahi500Price + 
                Dahi2LTQuan * Dahi2LTPrice + Dahi5LTQuan * Dahi5LTPrice + Dahi10LTQuan * Dahi10LTPrice + 
                Dahi2LTQuan15 * Dahi2LTPrice15 + Dahi5LTQuan15 * Dahi5LTPrice15 + Dahi10LTQuan15 * Dahi10LTPrice15 + 
                ButtermilkQuan * ButtermilkPrice + Khova500Quan * Khova500Price + Khoya1000Quan * Khoya1000Price + 
                Shrikhand100Quan * Shrikhand100Price + Shrikhand250Quan * Shrikhand250Price + Ghee200Quan * Ghee200Price + 
                Ghee500Quan * Ghee500Price + Ghee15LTQuan * Ghee15LTPrice + PaneerlooseQuan * PaneerloosePrice + 
                khovalooseQuan * khovaloosePrice
            )

            # Insert product quantities into vendor-specific table
            query = f"""
            INSERT INTO oasis.{vendorId} (
                date, MilkCM500Quan, MilkCM200Quan, MilkTM500Quan, MilkTM200Quan,
                Lassi200Quan, LassiCUP200Quan, LassiMANGOCUP200Quan, Dahi200Quan, 
                Dahi500Quan, Dahi2LTQuan, Dahi5LTQuan, Dahi10LTQuan, Dahi2LTQuan15, 
                Dahi5LTQuan15, Dahi10LTQuan15, ButtermilkQuan, Khova500Quan, Khoya1000Quan, 
                Shrikhand100Quan, Shrikhand250Quan, Ghee200Quan, Ghee500Quan, Ghee15LTQuan, 
                PaneerlooseQuan, khovalooseQuan
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(query, (
                datetime.now(), MilkCM500Quan, MilkCM200Quan, MilkTM500Quan, MilkTM200Quan, Lassi200Quan, LassiCUP200Quan, 
                LassiMANGOCUP200Quan, Dahi200Quan, Dahi500Quan, Dahi2LTQuan, Dahi5LTQuan, Dahi10LTQuan, Dahi2LTQuan15, 
                Dahi5LTQuan15, Dahi10LTQuan15, ButtermilkQuan, Khova500Quan, Khoya1000Quan, Shrikhand100Quan, Shrikhand250Quan, 
                Ghee200Quan, Ghee500Quan, Ghee15LTQuan, PaneerlooseQuan, khovalooseQuan
            ))

            # Update the vendor's amount in the vendor table
            update_query = "UPDATE oasis.vendor SET amount = amount + %s WHERE token = %s"
            cur.execute(update_query, (total_amount, vendorId))

            mysql.connection.commit()
            cur.close()

            return f"""<script type="text/javascript"> 
            alert("Products sold successfully and amount updated for vendor ID '{vendorId}', Total amount is:'{total_amount}");
            </script>"""

        except Exception as e:
            logging.error(f"Error occurred: {e}")
            return f"""<script type="text/javascript"> 
            alert("An error occurred: {e}");
            </script>"""
    else:
        name = request.args.get('name')
        return "success get " + name

# ========================
# Vendor payments section
# ========================

@app.route('/get_vendor', methods=['POST'])
def get_vendor():
    data = request.get_json()
    vendor_id = data.get('vendorId')
    print('Received vendor ID:', vendor_id)
    
    cur = mysql.connection.cursor()
    query = "SELECT amount FROM vendor WHERE token = %s"
    cur.execute(query, (vendor_id,))
    result = cur.fetchone()
    cur.close()
    
    if result:
        print('Vendor found, amount:', result[0])
        return jsonify({'amount': result[0]})
    else:
        print('Vendor not found')
        return jsonify({'error': 'Vendor not found'}), 404
    

@app.route('/update_vendor', methods=['POST'])
def update_vendor():
    data = request.json
    vendor_id = data.get('vendorId')
    paid_amount = data.get('paidAmount')
    
    cur = mysql.connection.cursor()
    query = "SELECT amount FROM vendor WHERE token = %s"
    cur.execute(query, (vendor_id,))
    result = cur.fetchone()
    
    if result:
        new_amount = result[0] - paid_amount
        update_query = "UPDATE vendor SET amount = %s WHERE token = %s"
        cur.execute(update_query, (new_amount, vendor_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({'new_amount': new_amount})
    else:
        cur.close()
        return jsonify({'error': 'Vendor not found'}), 404



# ===================
# Vendor Transaction
# ===================

@app.route('/VendorTransaction', methods=['POST', 'GET'])
def get_vendor_data():
    try:
        data = request.json
        vendor_id = data.get('vendor_id')
        
        if not vendor_id:
            return jsonify({"error": "Vendor ID is required"}), 400

        cur = mysql.connection.cursor()
        query = f"SELECT date, MilkCM500Quan, MilkCM200Quan, MilkTM500Quan, MilkTM200Quan, Lassi200Quan, LassiCUP200Quan, LassiMANGOCUP200Quan, Dahi200Quan, Dahi500Quan, Dahi2LTQuan, Dahi5LTQuan, Dahi10LTQuan, Dahi2LTQuan15, Dahi5LTQuan15, Dahi10LTQuan15, ButtermilkQuan, Khova500Quan, Khoya1000Quan, Shrikhand100Quan, Shrikhand250Quan, Ghee200Quan, Ghee500Quan, Ghee15LTQuan, PaneerlooseQuan, khovalooseQuan FROM `{vendor_id}`"
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()

        if not rows:
            return jsonify({"error": "No data found for the given vendor ID"}), 404

        print(f"Data fetched: {rows}")
        
        # Convert to JSON-compatible format
        data = []
        for row in rows:
            data.append({
                'date': row[0],
                'MilkCM500Quan': row[1],
                'MilkCM200Quan': row[2],
                'MilkTM500Quan': row[3],
                'MilkTM200Quan': row[4],
                'Lassi200Quan': row[5],
                'LassiCUP200Quan': row[6],
                'LassiMANGOCUP200Quan': row[7],
                'Dahi200Quan': row[8],
                'Dahi500Quan': row[9],
                'Dahi2LTQuan': row[10],
                'Dahi5LTQuan': row[11],
                'Dahi10LTQuan': row[12],
                'Dahi2LTQuan15': row[13],
                'Dahi5LTQuan15': row[14],
                'Dahi10LTQuan15': row[15],
                'ButtermilkQuan': row[16],
                'Khova500Quan': row[17],
                'Khoya1000Quan': row[18],
                'Shrikhand100Quan': row[19],
                'Shrikhand250Quan': row[20],
                'Ghee200Quan': row[21],
                'Ghee500Quan': row[22],
                'Ghee15LTQuan': row[23],
                'PaneerlooseQuan': row[24],
                'khovalooseQuan': row[25]
            })

        return jsonify(data)
    # except Exception as e:
    #     print(f"Database error: {e}")
    #     return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/submitlogistics',methods=['POST','GET'])
def submitlogistics():
    if request.method=='POST':
        title=request.form['title']
        amt=int(request.form['expense'])
        status=request.form['status']
        cur=mysql.connection.cursor()

        query="INSERT INTO `oasis`.`logistics` (`date`, `expense_name`,`status`, `expense_amt`) VALUES (curdate(), '%s', '%s', %d);"%(title,status,amt)
        x=cur.execute(query)
        mysql.connection.commit()
        print(x)
        """
        try:
            query="INSERT INTO `oasis`.`perday` (`date`, `income`, `expense`) VALUES (curdate(), 0, 0);"
            x=cur.execute(query)
            print(x)
            mysql.connection.commit()
        except:
            print("ERROR")
        query="update `oasis`.`perday` set expense=expense+%d where date=curdate();"%(amt)
        x=cur.execute(query)
        print(x)
        mysql.connection.commit()
        cur.execute("SELECT LAST_INSERT_ID() from oasis.vendor;")
        """
        
        cur.close()
        return f"""<script type="text/javascript"> 
        alert("Successfully recorded");
        </script>"""
    else:
        name = request.args.get('name')
        return "success get "+name

@app.route('/submitoverhead',methods=['POST','GET'])
def submitoverhead():
    if request.method=='POST':
        title=request.form['title']
        amt=int(request.form['expense'])
        status=request.form['status']
        cur=mysql.connection.cursor()

        query="INSERT INTO `oasis`.`overhead` (`date`, `expense_name`,`status`, `expense_amt`) VALUES (curdate(), '%s', '%s', %d);"%(title,status,amt)
        x=cur.execute(query)
        mysql.connection.commit()
        print(x)
        """
        try:
            query="INSERT INTO `oasis`.`perday` (`date`, `income`, `expense`) VALUES (curdate(), 0, 0);"
            x=cur.execute(query)
            print(x)
            mysql.connection.commit()
        except:
            print("ERROR")
        query="update `oasis`.`perday` set expense=expense+%d where date=curdate();"%(amt)
        x=cur.execute(query)
        print(x)
        mysql.connection.commit()
        cur.execute("SELECT LAST_INSERT_ID() from oasis.vendor;")
        cur.close()
        """
        
        return f"""<script type="text/javascript"> 
        alert("Successfully recorded");
        </script>"""
    else:
        name = request.args.get('name')
        return "success get "+name

# Add raw materials
@app.route('/submitrawmaterial', methods=['POST'])
def submitrawmaterial():
    if request.method == 'POST':
        # Initialize an empty dictionary to store form data
        data = {}
        print(request.form.get('MilkCM500RolePrice'))
        # List of input fields to process
        input_fields = [
            'MilkCM500RolePrice', 'MilkCM500RoleQuantity',
            'MilkCM200RolePrice', 'MilkCM200RoleQuantity',
            'MilkTM500RolePrice', 'MilkTM500RoleQuantity',
            'MilkTM200RolePrice', 'MilkTM200RoleQuantity',
            'Lassi200RolePrice', 'Lassi200RoleQuantity',
            'LassiCUP200cupPrice', 'LassiCUP200cupQuantity',
            'LassiMANGOCUP200cupPrice', 'LassiMANGOCUP200cupQuantity',
            'Dahi200MLRolePrice', 'Dahi200MLRoleQuantity',
            'Dahi500MLRolePrice', 'Dahi500MLRoleQuantity',
            'Dahi2LTBucketPrice', 'Dahi2LTBucketQuantity',
            'Dahi5LTBucketPrice', 'Dahi5LTBucketQuantity',
            'Dahi10LTBucketPrice', 'Dahi10LTBucketQuantity',
            'Dahi2LT1.5BucketPrice', 'Dahi2LT1.5BucketQuantity',
            'Dahi5LT1.5BucketPrice', 'Dahi5LT1.5BucketQuantity',
            'Dahi10LT1.5BucketPrice', 'Dahi10LT1.5BucketQuantity',
            'ButtermilkRolePrice', 'ButtermilkRoleQuantity',
            'Khova500TinPrice', 'Khova500TinQuantity',
            'Khoya1000TinPrice', 'Khoya1000TinQuantity',
            'Shrikhand100TinPrice', 'Shrikhand100TinQuantity',
            'Shrikhand250TinPrice', 'Shrikhand250TinQuantity',
            'Ghee200TinPrice', 'Ghee200TinQuantity',
            'Ghee500TinPrice', 'Ghee500TinQuantity',
            'Ghee15LTTinPrice', 'Ghee15LTTinQuantity',
            'PaneerloosePrice', 'PaneerlooseQuantity',
            'khovaloosePrice', 'khovalooseQuantity',
            'LASSI_CUP_FOILPrice', 'LASSI_CUP_FOILQuantity',
            'IFF_FLAVER_MANGOPrice', 'IFF_FLAVER_MANGOQuantity',
            'IFF_FLAVER_VANILLAPrice', 'IFF_FLAVER_VANILLAQuantity',
            'CULTURE_AMAZIKAPrice', 'CULTURE_AMAZIKAQuantity',
            'CULTURE_DANISKOPrice', 'CULTURE_DANISKOQuantity',
            'CULTURE_HRPrice', 'CULTURE_HRQuantity',
            'LIQUID_SOAPPrice', 'LIQUID_SOAPQuantity',
            'COS_SODAPrice', 'COS_SODAQuantity',
            'KAOH_Price', 'KAOH_Quantity'
        ]
        fieldc=0
        
        # Iterate over each input field and retrieve its value
        for field in input_fields:
            value = request.form.get(field, '0')
            print('here',value)
            #print(value,field,fieldc)
            
            try:
                data[field] = int(value)
                #print(data[field])
                fieldc+=1
                
            except ValueError:
                data[field] = 0
                #print(data[field])
                fieldc+=1
        print(fieldc)
        # Insert into MySQL
        cur = mysql.connection.cursor()
        try:
            x=['MilkCM500RoleQuan', 'MilkCM500RolePrice', 'MilkCM200RoleQuan', 'MilkCM200RolePrice',
        'MilkTM500RoleQuan', 'MilkTM500RolePrice', 'MilkTM200RoleQuan', 'MilkTM200RolePrice',
        'Lassi200RoleQuan', 'Lassi200RolePrice', 'LassiCUP200cupQuan', 'LassiCUP200cupPrice',
        'LassiMANGOCUP200cupQuan', 'LassiMANGOCUP200cupPrice', 'Dahi200MLRoleQuan', 'Dahi200MLRolePrice',
        'Dahi500MLRoleQuan', 'Dahi500MLRolePrice', 'Dahi2LTBucketQuan', 'Dahi2LTBucketPrice',
        'Dahi5LTBucketQuan', 'Dahi5LTBucketPrice', 'Dahi10LTBucketQuan', 'Dahi10LTBucketPrice',
        'Dahi2LT1_5BucketQuan', 'Dahi2LT1_5BucketPrice', 'Dahi5LT1_5BucketQuan', 'Dahi5LT1_5BucketPrice',
        'Dahi10LT1_5BucketQuan', 'Dahi10LT1_5BucketPrice', 'ButtermilkRoleQuan', 'ButtermilkRolePrice',
        'Khova500TinQuan', 'Khova500TinPrice', 'Khoya1000TinQuan', 'Khoya1000TinPrice',
        'Shrikhand100TinQuan', 'Shrikhand100TinPrice', 'Shrikhand250TinQuan', 'Shrikhand250TinPrice',
        'Ghee200TinQuan', 'Ghee200TinPrice', 'Ghee500TinQuan', 'Ghee500TinPrice',
        'Ghee15LTTinQuan', 'Ghee15LTTinPrice', 'PaneerlooseQuan', 'PaneerloosePrice',
        'khovalooseQuan', 'khovaloosePrice', 'LASSICUPFOILQuan', 'LASSICUPFOILPrice',
        'IFFFLAVERMANGOQuan', 'IFFFLAVERMANGOPrice', 'IFFFLAVERVANILLAQuan', 'IFFFLAVERVANILLAPrice',
        'CULTUREAMAZIKAQuan', 'CULTUREAMAZIKAPrice', 'CULTUREDANISKOQuan', 'CULTUREDANISKOPrice',
        'CULTUREHRQuan', 'CULTUREHRPrice', 'LIQUIDSOAPQuan', 'LIQUIDSOAPPrice',
        'COSSODAQuan', 'COSSODAPrice', 'KAOHQuan', 'KAOHPrice']
            #print("here",len(x))
            query = """
    INSERT INTO raw_materials (buydate,
        MilkCM500RoleQuan, MilkCM500RolePrice, MilkCM200RoleQuan, MilkCM200RolePrice,
        MilkTM500RoleQuan, MilkTM500RolePrice, MilkTM200RoleQuan, MilkTM200RolePrice,
        Lassi200RoleQuan, Lassi200RolePrice, LassiCUP200cupQuan, LassiCUP200cupPrice,
        LassiMANGOCUP200cupQuan, LassiMANGOCUP200cupPrice, Dahi200MLRoleQuan, Dahi200MLRolePrice,
        Dahi500MLRoleQuan, Dahi500MLRolePrice, Dahi2LTBucketQuan, Dahi2LTBucketPrice,
        Dahi5LTBucketQuan, Dahi5LTBucketPrice, Dahi10LTBucketQuan, Dahi10LTBucketPrice,
        Dahi2LT1_5BucketQuan, Dahi2LT1_5BucketPrice, Dahi5LT1_5BucketQuan, Dahi5LT1_5BucketPrice,
        Dahi10LT1_5BucketQuan, Dahi10LT1_5BucketPrice, ButtermilkRoleQuan, ButtermilkRolePrice,
        Khova500TinQuan, Khova500TinPrice, Khoya1000TinQuan, Khoya1000TinPrice,
        Shrikhand100TinQuan, Shrikhand100TinPrice, Shrikhand250TinQuan, Shrikhand250TinPrice,
        Ghee200TinQuan, Ghee200TinPrice, Ghee500TinQuan, Ghee500TinPrice,
        Ghee15LTTinQuan, Ghee15LTTinPrice, PaneerlooseQuan, PaneerloosePrice,
        khovalooseQuan, khovaloosePrice, LASSICUPFOILQuan, LASSICUPFOILPrice,
        IFFFLAVERMANGOQuan, IFFFLAVERMANGOPrice, IFFFLAVERVANILLAQuan, IFFFLAVERVANILLAPrice,
        CULTUREAMAZIKAQuan, CULTUREAMAZIKAPrice, CULTUREDANISKOQuan, CULTUREDANISKOPrice,
        CULTUREHRQuan, CULTUREHRPrice, LIQUIDSOAPQuan, LIQUIDSOAPPrice,
        COSSODAQuan, COSSODAPrice, KAOHQuan, KAOHPrice
    ) VALUES (
        curdate(),%d, %d, %d, %d, %d, %d, %d, %d, %d, %d,
        %d, %d, %d, %d, %d, %d, %d, %d, %d, %d,
        %d, %d, %d, %d, %d, %d, %d, %d, %d, %d,
        %d, %d, %d, %d, %d, %d, %d, %d, %d, %d,
        %d, %d, %d, %d, %d, %d, %d, %d, %d, %d,
        %d, %d, %d, %d, %d, %d, %d, %d, %d, %d,
        %d, %d, %d, %d, %d, %d, %d, %d
        )
"""

            print(tuple(data.values()))
            cur.execute(query%(tuple(data.values())))
            mysql.connection.commit()
            cur.close()
            return """
            <script type="text/javascript"> 
            alert("Successfully submitted raw materials");
            </script>
            """
        except Exception as e:
            print(f"Error inserting into database: {e}")
            return """
            <script type="text/javascript"> 
            alert("An error occurred while submitting raw materials");
            </script>
            """
    else:
        return "Method not allowed"
    
@app.route('/show_raw_materials', methods=['GET'])
def get_datasr():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT buydate,
    MilkCM500RoleQuan, MilkCM500RolePrice, MilkCM200RoleQuan, MilkCM200RolePrice,
    MilkTM500RoleQuan, MilkTM500RolePrice, MilkTM200RoleQuan, MilkTM200RolePrice,
    Lassi200RoleQuan, Lassi200RolePrice, LassiCUP200cupQuan, LassiCUP200cupPrice,
    LassiMANGOCUP200cupQuan, LassiMANGOCUP200cupPrice, Dahi200MLRoleQuan, Dahi200MLRolePrice,
    Dahi500MLRoleQuan, Dahi500MLRolePrice, Dahi2LTBucketQuan, Dahi2LTBucketPrice,
    Dahi5LTBucketQuan, Dahi5LTBucketPrice, Dahi10LTBucketQuan, Dahi10LTBucketPrice,
    Dahi2LT1_5BucketQuan, Dahi2LT1_5BucketPrice, Dahi5LT1_5BucketQuan, Dahi5LT1_5BucketPrice,
    Dahi10LT1_5BucketQuan, Dahi10LT1_5BucketPrice, ButtermilkRoleQuan, ButtermilkRolePrice,
    Khova500TinQuan, Khova500TinPrice, Khoya1000TinQuan, Khoya1000TinPrice,
    Shrikhand100TinQuan, Shrikhand100TinPrice, Shrikhand250TinQuan, Shrikhand250TinPrice,
    Ghee200TinQuan, Ghee200TinPrice, Ghee500TinQuan, Ghee500TinPrice,
    Ghee15LTTinQuan, Ghee15LTTinPrice, PaneerlooseQuan, PaneerloosePrice,
    khovalooseQuan, khovaloosePrice, LASSICUPFOILQuan, LASSICUPFOILPrice,
    IFFFLAVERMANGOQuan, IFFFLAVERMANGOPrice, IFFFLAVERVANILLAQuan, IFFFLAVERVANILLAPrice,
    CULTUREAMAZIKAQuan, CULTUREAMAZIKAPrice, CULTUREDANISKOQuan, CULTUREDANISKOPrice,
    CULTUREHRQuan, CULTUREHRPrice, LIQUIDSOAPQuan, LIQUIDSOAPPrice,
    COSSODAQuan, COSSODAPrice, KAOHQuan, KAOHPrice FROM raw_materials""")
    rows = cur.fetchall()
    cur.close()
    #print(rows)

    # Convert to JSON-compatible format
    data = []
    for row in rows:
        data.append({
            'buydate':row[0],'MilkCM500RoleQuan': row[1], 'MilkCM500RolePrice': row[2],
    'MilkCM200RoleQuan': row[3], 'MilkCM200RolePrice': row[4],
    'MilkTM500RoleQuan': row[5], 'MilkTM500RolePrice': row[6],
    'MilkTM200RoleQuan': row[7], 'MilkTM200RolePrice': row[8],
    'Lassi200RoleQuan': row[9], 'Lassi200RolePrice': row[10],
    'LassiCUP200cupQuan': row[11], 'LassiCUP200cupPrice': row[12],
    'LassiMANGOCUP200cupQuan': row[13], 'LassiMANGOCUP200cupPrice': row[14],
    'Dahi200MLRoleQuan': row[15], 'Dahi200MLRolePrice': row[16],
    'Dahi500MLRoleQuan': row[17], 'Dahi500MLRolePrice': row[18],
    'Dahi2LTBucketQuan': row[19], 'Dahi2LTBucketPrice': row[20],
    'Dahi5LTBucketQuan': row[21], 'Dahi5LTBucketPrice': row[22],
    'Dahi10LTBucketQuan': row[23], 'Dahi10LTBucketPrice': row[24],
    'Dahi2LT1_5BucketQuan': row[25], 'Dahi2LT1_5BucketPrice': row[26],
    'Dahi5LT1_5BucketQuan': row[27], 'Dahi5LT1_5BucketPrice': row[28],
    'Dahi10LT1_5BucketQuan': row[29], 'Dahi10LT1_5BucketPrice': row[30],
    'ButtermilkRoleQuan': row[31], 'ButtermilkRolePrice': row[32],
    'Khova500TinQuan': row[33], 'Khova500TinPrice': row[34],
    'Khoya1000TinQuan': row[35], 'Khoya1000TinPrice': row[36],
    'Shrikhand100TinQuan': row[37], 'Shrikhand100TinPrice': row[38],
    'Shrikhand250TinQuan': row[39], 'Shrikhand250TinPrice': row[40],
    'Ghee200TinQuan': row[41], 'Ghee200TinPrice': row[42],
    'Ghee500TinQuan': row[43], 'Ghee500TinPrice': row[44],
    'Ghee15LTTinQuan': row[45], 'Ghee15LTTinPrice': row[46],
    'PaneerlooseQuan': row[47], 'PaneerloosePrice': row[48],
    'khovalooseQuan': row[49], 'khovaloosePrice': row[50],
    'LASSICUPFOILQuan': row[51], 'LASSICUPFOILPrice': row[52],
    'IFFFLAVERMANGOQuan': row[53], 'IFFFLAVERMANGOPrice': row[54],
    'IFFFLAVERVANILLAQuan': row[55], 'IFFFLAVERVANILLAPrice': row[56],
    'CULTUREAMAZIKAQuan': row[57], 'CULTUREAMAZIKAPrice': row[58],
    'CULTUREDANISKOQuan': row[59], 'CULTUREDANISKOPrice': row[60],
    'CULTUREHRQuan': row[61], 'CULTUREHRPrice': row[62],
    'LIQUIDSOAPQuan': row[63], 'LIQUIDSOAPPrice': row[64],
    'COSSODAQuan': row[65], 'COSSODAPrice': row[66],
    'KAOHQuan': row[67], 'KAOHPrice': row[68]
        })

    return jsonify(data)

# Add raw materials
@app.route('/userawmaterial', methods=['POST'])
def userawmaterial():
    if request.method == 'POST':
        quantities = [
            "MilkCM500RoleQuantity",
            "MilkCM200RoleQuantity",
            "MilkTM500RoleQuantity",
            "MilkTM200RoleQuantity",
            "Lassi200RoleQuantity",
            "LassiCUP200cupQuantity",
            "LassiMANGOCUP200cupQuantity",
            "Dahi200MLRoleQuantity",
            "Dahi500MLRoleQuantity",
            "Dahi2LTBucketQuantity",
            "Dahi5LTBucketQuantity",
            "Dahi10LTBucketQuantity",
            "Dahi2LT1.5BucketQuantity",
            "Dahi5LT1.5BucketQuantity",
            "Dahi10LT1.5BucketQuantity",
            "ButtermilkRoleQuantity",
            "Khova500TinQuantity",
            "Khoya1000TinQuantity",
            "Shrikhand100TinQuantity",
            "Shrikhand250TinQuantity", 
            "Ghee200TinQuantity",
            "Ghee500TinQuantity",
            "Ghee15LTTinQuantity",
            "PaneerlooseQuantity",
            "khovalooseQuantity",
            "LASSI CUP FOIL Quantity",
            "IFF FLAVER MANGO Quantity",
            "IFF FLAVER VANILLA Quantity",
            "CULTURE AMAZIKA Quantity",
            "CULTURE DANISKO Quantity",
            "CULTURE HR Quantity",
            "LIQUID SOAP Quantity",
            "COS SODA Quantity",
            "KAOHQuantity"
        ]
        fieldc=0
        datar={}
        #print(quantities,len(quantities))

        for field in quantities:
                value = request.form.get(field, '0')
                
                try:
                    datar[field] = int(value)
                    fieldc+=1
                    
                except ValueError:
                    datar[field] = 0
                    fieldc+=1
        
        cur = mysql.connection.cursor()
        try:
            query="""
                SELECT 
                SUM(MilkCM500RoleQuan),
                SUM(MilkCM200RoleQuan),
                SUM(MilkTM500RoleQuan),
                SUM(MilkTM200RoleQuan),
                SUM(Lassi200RoleQuan),
                SUM(LassiCUP200cupQuan),
                SUM(LassiMANGOCUP200cupQuan),
                SUM(Dahi200MLRoleQuan),
                SUM(Dahi500MLRoleQuan),
                SUM(Dahi2LTBucketQuan),
                SUM(Dahi5LTBucketQuan),
                SUM(Dahi10LTBucketQuan),
                SUM(Dahi2LT1_5BucketQuan),
                SUM(Dahi5LT1_5BucketQuan),
                SUM(Dahi10LT1_5BucketQuan),
                SUM(ButtermilkRoleQuan),
                SUM(Khova500TinQuan),
                SUM(Khoya1000TinQuan),
                SUM(Shrikhand100TinQuan),
                SUM(Shrikhand250TinQuan),
                SUM(Ghee200TinQuan),
                SUM(Ghee500TinQuan),
                SUM(Ghee15LTTinQuan),
                SUM(PaneerlooseQuan),
                SUM(khovalooseQuan),
                SUM(LASSICUPFOILQuan),
                SUM(IFFFLAVERMANGOQuan),
                SUM(IFFFLAVERVANILLAQuan),
                SUM(CULTUREAMAZIKAQuan),
                SUM(CULTUREDANISKOQuan),
                SUM(CULTUREHRQuan),
                SUM(LIQUIDSOAPQuan),
                SUM(COSSODAQuan),
                SUM(KAOHQuan)
                FROM raw_materials;

                """
            cur.execute(query)
            rows = cur.fetchall()
            #print(rows)
            data=[]
            for row in rows:
                data.append({
                    'MilkCM500RoleQuan': row[0],
                    'MilkCM200RoleQuan': row[1],
                    'MilkTM500RoleQuan': row[2],
                    'MilkTM200RoleQuan': row[3],
                    'Lassi200RoleQuan': row[4],
                    'LassiCUP200cupQuan': row[5],
                    'LassiMANGOCUP200cupQuan': row[6],
                    'Dahi200MLRoleQuan': row[7],
                    'Dahi500MLRoleQuan': row[8],
                    'Dahi2LTBucketQuan': row[9],
                    'Dahi5LTBucketQuan': row[10],
                    'Dahi10LTBucketQuan': row[11],
                    'Dahi2LT1_5BucketQuan': row[12],
                    'Dahi5LT1_5BucketQuan': row[13],
                    'Dahi10LT1_5BucketQuan': row[14],
                    'ButtermilkRoleQuan': row[15],
                    'Khova500TinQuan': row[16],
                    'Khoya1000TinQuan': row[17],
                    'Shrikhand100TinQuan': row[18],
                    'Shrikhand250TinQuan': row[19],
                    'Ghee200TinQuan': row[20],
                    'Ghee500TinQuan': row[21],
                    'Ghee15LTTinQuan': row[22],
                    'PaneerlooseQuan': row[23],
                    'khovalooseQuan': row[24],
                    'LASSICUPFOILQuan': row[25],
                    'IFFFLAVERMANGOQuan': row[26],
                    'IFFFLAVERVANILLAQuan': row[27],
                    'CULTUREAMAZIKAQuan': row[28],
                    'CULTUREDANISKOQuan': row[29],
                    'CULTUREHRQuan': row[30],
                    'LIQUIDSOAPQuan': row[31],
                    'COSSODAQuan': row[32],
                    'KAOHQuan': row[33]
                }
                )
            data=data[0].values()
            
            datar=[float(value) for value in datar.values()]
            data=[float(value) for value in data]
            print(datar,type(datar))
            print(data,type(data))
            result=[x - y for x, y in zip(data, datar)]
            print(tuple(result))
            query="""
                INSERT INTO use_raw_materials (
                    usedate,
                    MilkCM500RoleQuan, MilkCM200RoleQuan, MilkTM500RoleQuan, MilkTM200RoleQuan,
                    Lassi200RoleQuan, LassiCUP200cupQuan, LassiMANGOCUP200cupQuan,
                    Dahi200MLRoleQuan, Dahi500MLRoleQuan, Dahi2LTBucketQuan,
                    Dahi5LTBucketQuan, Dahi10LTBucketQuan, Dahi2LT1_5BucketQuan,
                    Dahi5LT1_5BucketQuan, Dahi10LT1_5BucketQuan, ButtermilkRoleQuan,
                    Khova500TinQuan, Khoya1000TinQuan, Shrikhand100TinQuan,
                    Shrikhand250TinQuan, Ghee200TinQuan, Ghee500TinQuan,
                    Ghee15LTTinQuan, PaneerlooseQuan, khovalooseQuan,
                    LASSICUPFOILQuan, IFFFLAVERMANGOQuan, IFFFLAVERVANILLAQuan,
                    CULTUREAMAZIKAQuan, CULTUREDANISKOQuan, CULTUREHRQuan,
                    LIQUIDSOAPQuan, COSSODAQuan, KAOHQuan
                ) VALUES (
                    curdate(), %d, %d, %d, %d, %d, %d, %d, %d, %d, %d,
                    %d, %d, %d, %d, %d, %d, %d, %d, %d, %d,
                    %d, %d, %d, %d, %d, %d, %d, %d, %d, %d,
                    %d, %d, %d, %d
                )                 
                """
            cur.execute(query%tuple(result))
            mysql.connection.commit()
            cur.close()
            return """
            <script type="text/javascript"> 
            alert("Successfully submitted raw materials");
            </script>
            """
        except Exception as e:
            print(f"Error inserting into database: {e}")
            return """
            <script type="text/javascript"> 
            alert("An error occurred while submitting raw materials");
            </script>
            """
    else:
        return "Method not allowed"


if __name__ == '__main__':
    app.run(debug=True)
