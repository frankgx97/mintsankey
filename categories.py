categories = {
    'Auto & Transport': [
        'Auto Insurance',
        'Auto Payment',
        'Gas & Fuel',
        'Parking',
        'Public Transportation',
        'Ride Share',
        'Service & Parts'
    ],
    'Bills & Utilities': [
        'Home Phone',
        'Internet',
        'Mobile Phone',
        'Television',
        'Utilities',
    ],
    'Business Services': [
        'Advertising',
        'Legal',
        'Office Supplies',
        'Printing',
        'Shipping',
    ],
    'Education': [
        'Books & Supplies',
        'Student Loan',
        'Tuition',
    ],
    'Entertainment': [
        'Amusement',
        'Arts',
        'Movies & DVDs',
        'Music',
        'Newspapers & Magazines',
    ],
    'Fees & Charges': [
        'ATM Fee',
        'Bank Fee',
        'Finance Charge',
        'Late Fee',
        'Service Fee',
        'Trade Commissions',
    ],
    'Financial': [
        'Financial Advisor',
        'Life Insurance',
    ],
    'Food & Dining': [
        'Alcohol & Bars',
        'Coffee Shops',
        'Fast Food',
        'Food Delivery',
        'Groceries',
        'Restaurants',
    ],
    'Gifts & Donations': [
        'Charity',
        'Gift',
    ],
    'Health & Fitness': [
        'Dentist',
        'Doctor',
        'Eyecare',
        'Gym',
        'Health Insurance',
        'Pharmacy',
        'Sports',
    ],
    'Home': [
        'Furnishings',
        'Home Improvement',
        'Home Insurance',
        'Home Services',
        'Home Supplies',
        'Lawn & Garden',
        'Mortgage & Rent',
    ],
    'Income': [
        'Bonus',
        'Interest Income',
        'Paycheck',
        'Reimbursement',
        'Rental Income',
        'Returned Purchase',
    ],
    'Investments': [
        'Buy',
        'Deposit',
        'Dividend & Cap Gains',
        'Sell',
        'Withdrawal',
    ],
    'Kids': [
        'Allowance',
        'Baby Supplies',
        'Babysitter & Daycare',
        'Child Support',
        'Kids Activities',
        'Toys',
    ],
    'Loans': [
        'Loan Fees and Charges',
        'Loan Insurance',
        'Loan Interest',
        'Loan Payment',
        'Loan Principal',
    ],
    'Misc Expenses': [],
    'Personal Care': [
        'Hair',
        'Laundry',
        'Spa & Massage',
    ],
    'Pets': [
        'Pet Food & Supplies',
        'Pet Grooming',
        'Veterinary',
    ],
    'Shopping': [
        'Books',
        'Clothing',
        'Electronics & Software',
        'Hobbies',
        'Sporting Goods',
    ],
    'Taxes': [
        'Federal Tax',
        'Local Tax',
        'Property Tax',
        'Sales Tax',
        'State Tax',
    ],
    'Transfer': [
        'Credit Card Payment',
        'Transfer for Cash Spending',
    ],
    'Travel': [
        'Air Travel',
        'Hotel',
        'Rental Car & Taxi',
        'Vacation',
    ],
    'Uncategorized': [
        'Cash & ATM',
        'Check',
    ],
}

def category_reverse_lookup(sub_category: str) -> str:
    if sub_category in categories:
        return str
    for k in categories:
        if sub_category in categories[k]:
            return k
    return 'Uncategorized'

def get_categories(input_category: str) -> str:
    if input_category in categories:
        return input_category, None
    else:
        return category_reverse_lookup(input_category), input_category