# import the libraries we need
from faker import Faker
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Initialize the Faker generator
fake = Faker()

# Set a seed so results are reproducible (you'll get the same "random" data each time)
Faker.seed(42)
np.random.seed(42)
random.seed(42)

# Number of transactions to generate
NUM_TRANSACTIONS = 10000
# Fraud rate - 5% of transactions will be fraudulent
FRAUD_RATE = 0.05

print(f"Generating {NUM_TRANSACTIONS} transactions with {FRAUD_RATE*100}% fraud rate...")

# Create lists to store our data
transactions = []

# Generate the data
for i in range(NUM_TRANSACTIONS):
    # Basic transaction info using Faker
    transaction_id = f"TXN-{i+1:06d}"
    customer_name = fake.name()
    customer_email = fake.email()
    transaction_date = fake.date_between(start_date='-90d', end_date='today')
    transaction_time = fake.time()
    
    # Generate realistic transaction amounts
    # Most transactions are small, some are large
    amount = round(np.random.lognormal(mean=4.5, sigma=1.0), 2)
    # Cap extremely large values
    amount = min(amount, 50000)
    
    # Transaction types
    transaction_types = ['PURCHASE', 'TRANSFER', 'WITHDRAWAL', 'DEPOSIT', 'PAYMENT']
    transaction_type = random.choice(transaction_types)
    
    # Merchant or recipient
    merchant = fake.company()
    location = fake.city()
    
    # Account balance before transaction (starting balance)
    starting_balance = round(np.random.lognormal(mean=8, sigma=1.5), 2)
    starting_balance = min(starting_balance, 100000)
    
    # Calculate ending balance
    if transaction_type in ['PURCHASE', 'WITHDRAWAL', 'TRANSFER']:
        ending_balance = starting_balance - amount
    else:  # DEPOSIT or PAYMENT
        ending_balance = starting_balance + amount
    
    # Determine if this is fraud (based on rules, not random)
    is_fraud = False
    
    # Rule 1: Transactions where amount > 10,000 and starting_balance < 1000
    if amount > 10000 and starting_balance < 1000:
        is_fraud = True
    
    # Rule 2: Deposits where ending_balance is more than 5x starting_balance
    if transaction_type == 'DEPOSIT' and ending_balance > starting_balance * 5:
        is_fraud = True
    
    # Rule 3: Random fraud allocation to hit our 5% target
    if random.random() < FRAUD_RATE * 0.3:
        is_fraud = True
    
    # Add some weird behavior to fraudulent transactions
    if is_fraud:
        # Fraudulent transactions often happen at unusual times (2-4 AM)
        if random.random() < 0.4:
            transaction_time = f"{random.randint(2, 4):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"
        # Fraud often involves round amounts
        if random.random() < 0.3:
            amount = round(amount / 100) * 100
        # Unusual merchant names
        merchant = "FRAUD_" + fake.company()
    
    # Append all the data for this transaction
    transactions.append({
        'transaction_id': transaction_id,
        'customer_name': customer_name,
        'customer_email': customer_email,
        'transaction_date': transaction_date,
        'transaction_time': transaction_time,
        'amount': amount,
        'transaction_type': transaction_type,
        'merchant': merchant,
        'location': location,
        'starting_balance': starting_balance,
        'ending_balance': ending_balance,
        'is_fraud': int(is_fraud)
    })

# Convert to a pandas DataFrame
df = pd.DataFrame(transactions)

# Add calculated fields that are useful for analysis
df['day_of_week'] = pd.to_datetime(df['transaction_date']).dt.day_name()
df['hour'] = pd.to_datetime(df['transaction_time'], format='%H:%M:%S').dt.hour

# Add a field for amount category
df['amount_category'] = pd.cut(
    df['amount'],
    bins=[0, 50, 200, 1000, 5000, float('inf')],
    labels=['Micro', 'Small', 'Medium', 'Large', 'Very Large']
)

# Save to CSV
df.to_csv('../data/fraud_transactions.csv', index=False)
print(f"✅ Data saved to ../data/fraud_transactions.csv")
print(f"📊 Total transactions: {len(df)}")
print(f"🚨 Fraudulent transactions: {df['is_fraud'].sum()}")

# Display a sample of the data
print("\n📋 Sample of generated data:")
print(df.head(10))

# Summary statistics
print("\n📈 Amount Statistics:")
print(df['amount'].describe())

print("\n💰 Fraud vs Non-Fraud Summary:")
print(df.groupby('is_fraud')['amount'].agg(['count', 'mean', 'sum']))