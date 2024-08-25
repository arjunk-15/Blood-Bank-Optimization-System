from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

inventory = {
    'A+': {'quantity': 50, 'expiration_date': '2024-08-20'},
    'O-': {'quantity': 30, 'expiration_date': '2024-08-15'},
    'B+': {'quantity': 20, 'expiration_date': '2024-08-18'},
}

def estimate_demand(hospital):
    return {
        'A+': 10,
        'O-': 10,
        'B+': 10,
    }

def distribute_blood(inventory, hospitals):
    distribution_results = []
    for hospital in hospitals:
        demand = estimate_demand(hospital)
        distribution = {}
        for blood_type, required_units in demand.items():
            if inventory[blood_type]['quantity'] >= required_units:
                inventory[blood_type]['quantity'] -= required_units
                distribution[blood_type] = required_units
            else:
                distribution[blood_type] = 'Insufficient stock'
        distribution_results.append({'hospital': hospital, 'distribution': distribution})
    return distribution_results

@app.route('/')
def home():
    hospitals = ['Hospital A', 'Hospital B']
    distribution_results = distribute_blood(inventory, hospitals)
    return render_template('index.html', inventory=inventory, distribution_results=distribution_results)

@app.route('/update_inventory', methods=['POST'])
def update_inventory():
    blood_type = request.form['blood_type']
    new_quantity = int(request.form['quantity'])
    inventory[blood_type]['quantity'] = new_quantity
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
