import pandas as pd
import json
from flask import Flask, render_template, request
app = Flask(__name__)
df = pd.read_csv('data.csv')

@app.route('/data/counties')
def getCounties():
    counties = {
        'counties': []
    }
    count_buff = {
        'counties': []
    }
    reg_name = df['reg_name'].to_numpy()
    reg_id = df['reg_id'].to_numpy()
    for name, regid in zip(reg_name, reg_id):
        count_buff['counties'].append({'name': name, 'id': int(regid)})
    for value in count_buff['counties']:
        if value not in counties['counties']:
            counties['counties'].append(value)
    json_counties = json.dumps(counties)
    return json_counties

@app.route('/data/taxes')
def getTaxes():
    taxes = {
        'taxes': []
    }
    tax_buff = {
        'taxes': []
    }
    tax_id = []
    tax_name = df['tax_name'].to_numpy()
    tax_id = df['tax_id'].to_numpy()
    for name, taxid in zip(tax_name, tax_id):
        tax_buff['taxes'].append({'name': name, 'id': int(taxid)})
    for value in tax_buff['taxes']:
        if value not in taxes['taxes']:
            taxes['taxes'].append(value)        
    json_taxes = json.dumps(taxes)
    return json_taxes

@app.route('/data/<int:countyId>/taxes')
def getCountyTaxesFrom(countyId):
    countyTaxesFrom = {
        'taxes': {}
    }
    yearFrom = request.args.get('from', default = 2012, type = int)
    yearTo = request.args.get('to', default = 2020, type = int)
    tax_df = df.loc[df['reg_id'] == countyId]
    final_df = tax_df.loc[tax_df['year'].between(yearFrom, yearTo)]
    tax_id = final_df['tax_id'].to_numpy()
    years = final_df['year'].to_numpy()
    amounts = final_df['amount'].to_numpy()
    taxes = []
    for taxid, year, amount in zip(tax_id, years, amounts):
        taxes.append({int(taxid): [{int(year): float(amount)}]})
    merged_taxes = {}
    for obj in taxes:
        for list in obj:
            if list in merged_taxes:
                merged_taxes[list] += (obj[list])
            else:
                merged_taxes[list] = obj[list]
    countyTaxesFrom['taxes'] = merged_taxes
    json_countyTaxesFrom = json.dumps(countyTaxesFrom)
    return json_countyTaxesFrom

@app.route('/data/<int:countyId>/taxes/<int:taxId>')
def getCountyTaxFrom(countyId, taxId):
    countyTaxFrom = {
        'tax': {}
    }
    yearFrom = request.args.get('from', default = 2012, type = int)
    yearTo = request.args.get('to', default = 2020, type = int)
    taxes_df = df.loc[df['reg_id'] == countyId]
    tax_df = taxes_df.loc[df['tax_id'] == taxId]
    final_df = tax_df.loc[tax_df['year'].between(yearFrom, yearTo)]
    years = final_df['year'].to_numpy()
    amounts = final_df['amount'].to_numpy()
    tax = []
    for year, amount in zip(years, amounts):
        tax.append({int(taxId): [{int(year): float(amount)}]})
    merged_tax = {}
    for obj in tax:
        for list in obj:
            if list in merged_tax:
                merged_tax[list] += (obj[list])
            else:
                merged_tax[list] = obj[list]
    countyTaxFrom['tax'] = merged_tax
    json_countyTaxFrom = json.dumps(countyTaxFrom)
    return json_countyTaxFrom

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html'), 404

@app.errorhandler(401)
def notAuth(error):
    return render_template('401.html'), 401

@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403

@app.errorhandler(500)
def serverError(error):
    return render_template('500.html'), 500

# print(getCounties())
# print(getTaxes())
# print(getCountyTaxesFrom(13))
# print(getCountyTaxFrom(12, 14))