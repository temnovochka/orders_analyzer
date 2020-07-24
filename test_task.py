import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='Analyze orders.')
parser.add_argument('file_name', type=str,
                    help='csv-file name with orders')

args = parser.parse_args()

orders = pd.read_csv(args.file_name, delimiter=";", converters={
    'Profit': lambda x: float(x.replace(',', '.')),
    'Sales': lambda x: float(x.replace(',', '.')),
    'Quantity': lambda x: int(x),
    'Order Date': lambda x: pd.to_datetime(x),
    'Ship Date': lambda x: pd.to_datetime(x)
})

print('1. Summary profit = {:.2f}\n'.format(orders['Profit'].sum()))

orders_grouped_by_product = orders.groupby('Product ID').agg({
    'Sales': 'sum',
    'Quantity': 'sum',
    'Profit': 'sum',
    'Product Name': 'first'
})


def _aggregate_by_field(field, fun):
    product = orders_grouped_by_product.loc[fun(orders_grouped_by_product[field])]
    return product.name, product['Product Name']


best_product_sales = _aggregate_by_field('Sales', lambda x: x.idxmax())
best_product_quantity = _aggregate_by_field('Quantity', lambda x: x.idxmax())
best_product_profit = _aggregate_by_field('Profit', lambda x: x.idxmax())

print('2. Best products:\nby sales: {}, {}\nby quantity: {}, {}\nby profit: {}, {}\n'.format(*best_product_sales,
                                                                                             *best_product_quantity,
                                                                                             *best_product_profit))

worst_product_sales = _aggregate_by_field('Sales', lambda x: x.idxmin())
worst_product_quantity = _aggregate_by_field('Quantity', lambda x: x.idxmin())
worst_product_profit = _aggregate_by_field('Profit', lambda x: x.idxmin())

print('3. Worst products:\nby sales: {}, {}\nby quantity: {}, {}\nby profit: {}, {}\n'.format(*worst_product_sales,
                                                                                              *worst_product_quantity,
                                                                                              *worst_product_profit))

unique_orders = orders.groupby('Order ID').first()
unique_orders['Delivery Time'] = unique_orders['Ship Date'] - unique_orders['Order Date']
print('4. Average delivery time = {}'.format(unique_orders['Delivery Time'].mean()))
print('5. Standard deviation of delivery time = {}'.format(unique_orders['Delivery Time'].std()))

orders_grouped_by_product.to_csv('products_info.csv', sep=';')
