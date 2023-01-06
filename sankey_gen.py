#!/usr/bin/env python3.6
"""Sakey diagram generator for budgeting 'fun'

See the README for more info.
"""
import csv
from datetime import datetime
import typing
from typing import Dict, List
import plotly.graph_objects as plt
from plotly.offline import plot
import plotly
import toml
import os

from transaction import Transaction



def parse_csv(fname: str) -> List[Transaction]:
    """Parse a CSV file into a list of transactions

    Args:
        fname: filename
        use_labels: if a label is not None, use that as the category instead

    Returns:
        Each row as a Transaction stored in a list
    """
    transactions = []

    with open(fname, 'r', encoding='ISO-8859-1') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # skip header row

        for row in csv_reader:
            t = Transaction()
            t.load_from_csv(row)
            transactions.append(t)

    return transactions

def filter_transactions(
    transactions: List[Transaction], 
    start_date: datetime,
    end_date: datetime, 
    ignore_vendors: List[str],
    ignore_categories: List[str], 
    ignore_accounts: List[str],
    ignore: bool,
    use_labels: bool
    ) -> List[Transaction]:
    """Filter transactions based on date, vendor, and type

    Args:
        transactions: list of all transactions
        start_date: ignore all transactions before this date
        end_date: ignore all transactions after this date
        vendors: filter transactions from these vendors
        categories: filter transactions within these categories
        ignore: if True, ignore transactions from above filters
            else, only return transactions from above filters
        use_labels: check labels in addition to categories

    Returns:
        Filtered list of transactions
    """

    filt_trans = []
    for t in transactions:
        #if t.date <= start_date or t.date >= end_date:
        #    continue

        if ignore:
            if t.vendor in ignore_vendors:
                continue

            if use_labels and t.label in ignore_categories:
                continue

            if t.category in ignore_categories:
                continue

            if t.account in ignore_accounts:
                continue
        else:
            if ignore_vendors and t.vendor not in ignore_vendors:
                continue

            if use_labels and t.label not in ignore_categories:
                continue

            if not use_labels and t.category not in ignore_categories:
                continue
            
            if ignore_accounts and t.account not in ignore_accounts:
                continue

        #if not t.debit:
        #    continue

        filt_trans.append(t)
    return filt_trans

def add_transactions(transactions: List[Transaction], config: Dict):
    """Generate SankeyMatic strings from filtered transactions

    Args:
        f: output file
        transactions: list of all transactions
        take_home: total take home pay for the period
        config: config file
    """

    # These two are placeholders, they won't be used to filter transactions
    start_date = datetime.now()
    end_date = datetime.now()

    filt_trans = filter_transactions(
        transactions=transactions,
        start_date=start_date,
        end_date=end_date,
        ignore_vendors=config['transactions']['ignore_vendors'],
        ignore_categories=config['transactions']['ignore_categories'],
        ignore_accounts=config['transactions']['ignore_accounts'],
        ignore=True,
        use_labels=config['transactions']['prefer_labels'])

    income = {}
    expense = {}
    for tx in filt_trans:
        if tx.debit:
            # expense
            if tx.category not in expense:
                expense[tx.category] = {
                    'amount': tx.amount,
                    'subcategories': {tx.sub_category: tx.amount} if tx.sub_category != None else {}
                    }
            else:
                expense[tx.category]['amount'] += tx.amount
                if tx.sub_category == None:
                    continue
                if tx.sub_category not in expense[tx.category]['subcategories']:
                    expense[tx.category]['subcategories'][tx.sub_category] = tx.amount
                else:
                    expense[tx.category]['subcategories'][tx.sub_category] += tx.amount
        else:
            # income
            if tx.category != 'Income':
                continue
            if tx.category not in income:
                income[tx.category] = {
                    'amount': tx.amount,
                    'subcategories': {tx.sub_category: tx.amount} if tx.sub_category != None else {}
                    }
            else:
                income[tx.category]['amount'] += tx.amount
                if tx.sub_category == None:
                    continue
                if tx.sub_category not in income[tx.category]['subcategories']:
                    income[tx.category]['subcategories'][tx.sub_category] = tx.amount
                else:
                    income[tx.category]['subcategories'][tx.sub_category] += tx.amount

    saving = income['Income']['amount'] - sum([expense[x]['amount'] for x in expense])
    expense['Saving'] = {'amount': saving, 'subcategories': {}}
    plot_data = {
        'source': [],
        'target': [],
        'value': [],
        'labels': [],
    }
    output = ''
    sorted_keys = [x[0] for x in sorted(income.items(), key=lambda x:x[1]['amount'], reverse=True)]
    for k in sorted_keys:
        output += '{} [{}] Net Income\n'.format(k, income[k]['amount'])
        plot_data['source'].append(k)
        plot_data['target'].append('Net Income')
        plot_data['value'].append(income[k]['amount'])
        plot_data['labels'].append(k)
        plot_data['labels'].append('Net Income')
        for sk in income[k]['subcategories']:
            output += '{} [{}] {}\n'.format(sk, income[k]['subcategories'][sk], k)
            plot_data['source'].append(sk)
            plot_data['target'].append(k)
            plot_data['value'].append(income[k]['subcategories'][sk])
            plot_data['labels'].append(k)
            plot_data['labels'].append(sk)
    
    sorted_keys = [x[0] for x in sorted(expense.items(), key=lambda x:x[1]['amount'], reverse=True)]
    for k in sorted_keys:
        output += 'Net Income [{}] {}\n'.format(expense[k]['amount'], k)
        plot_data['source'].append('Net Income')
        plot_data['target'].append(k)
        plot_data['value'].append(expense[k]['amount'])
        plot_data['labels'].append(k)
        plot_data['labels'].append('Net Income')
        
        for sk in expense[k]['subcategories']:
            output += '{} [{}] {}\n'.format(k, expense[k]['subcategories'][sk], sk)
            plot_data['source'].append(k)
            plot_data['target'].append(sk)
            plot_data['value'].append(expense[k]['subcategories'][sk])
            plot_data['labels'].append(k)
            plot_data['labels'].append(sk)

    return plot_data, output

def plot_sankey(data):
    data['labels'] = list(set(data['labels']))
    node_dict = {y:x for x, y in enumerate(data['labels'])}
    source_node = [node_dict[x] for x in data['source']]
    target_node = [node_dict[x] for x in data['target']]

    fig = plt.Figure( 
        data=[plt.Sankey(
            arrangement = "snap",
            node = dict( 
                label = data['labels']
            ),
            link = dict(
                source = source_node,
                target = target_node,
                value = data['value']
            ))])

    img = plotly.io.to_image(
        fig=fig,
        format='png',
        width=1500,
        height=1200,
        )
    html = plotly.io.to_html(
        fig=fig
    )
    return img, html


def main(*, config_file: str = None, session_id: str = None):
    """Generate the SankeyMatic-formatted data"""
    if config_file:
        config_file = open(config_file, 'r')
    else:
        try:
            config_file = open('config.toml', 'r')
        except IOError:
            config_file = open('config-sample.toml', 'r')

    config = toml.load(config_file)
    config_file.close()

    transactions = parse_csv(os.path.join('/tmp', session_id, "input.csv"))

    plot_data, sankeymatic = add_transactions(transactions, config)
    img, html = plot_sankey(plot_data)
    return img, html, sankeymatic

if __name__ == "__main__":
    main()
