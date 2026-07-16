import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for better-looking plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("Set2")

# Load the data
df = pd.read_csv('../data/fraud_transactions.csv')

print("=" * 60)
print("FRAUD TRANSACTION ANALYSIS REPORT")
print("=" * 60)

print(f"\n📊 Dataset Overview:")
print(f"   - Total Transactions: {len(df):,}")
print(f"   - Fraud Transactions: {df['is_fraud'].sum():,}")
print(f"   - Fraud Rate: {df['is_fraud'].mean()*100:.2f}%")

# 1. Fraud by transaction type
print("\n🔍 Fraud by Transaction Type:")
fraud_by_type = df.groupby('transaction_type')['is_fraud'].agg(['count', 'mean'])
fraud_by_type['mean'] = fraud_by_type['mean'] * 100
print(fraud_by_type.round(2))

# 2. Create visualizations
print("\n📈 Creating visualizations...")

# Create a figure with multiple subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Financial Fraud Analysis Dashboard', fontsize=16, fontweight='bold')

# Plot 1: Distribution of transaction amounts
ax1 = axes[0, 0]
fraud_amounts = df[df['is_fraud'] == 1]['amount']
legit_amounts = df[df['is_fraud'] == 0]['amount']

ax1.hist(legit_amounts, bins=50, alpha=0.7, label='Legitimate', color='blue')
ax1.hist(fraud_amounts, bins=20, alpha=0.7, label='Fraudulent', color='red')
ax1.set_xlabel('Transaction Amount ($)')
ax1.set_ylabel('Frequency')
ax1.set_title('Transaction Amount Distribution by Status')
ax1.legend()
ax1.set_xlim(0, 10000)

# Plot 2: Fraud rate by transaction type
ax2 = axes[0, 1]
fraud_rate_by_type = df.groupby('transaction_type')['is_fraud'].mean() * 100
bars = ax2.bar(fraud_rate_by_type.index, fraud_rate_by_type.values, color='coral')
ax2.set_xlabel('Transaction Type')
ax2.set_ylabel('Fraud Rate (%)')
ax2.set_title('Fraud Rate by Transaction Type')
for bar, value in zip(bars, fraud_rate_by_type.values):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
             f'{value:.1f}%', ha='center', va='bottom')

# Plot 3: Fraud by hour of day
ax3 = axes[1, 0]
hourly_fraud = df.groupby('hour')['is_fraud'].mean() * 100
hourly_count = df.groupby('hour')['is_fraud'].count()

ax3.plot(hourly_fraud.index, hourly_fraud.values, marker='o', color='purple', linewidth=2)
ax3.set_xlabel('Hour of Day')
ax3.set_ylabel('Fraud Rate (%)')
ax3.set_title('Fraud Rate by Hour of Day')
ax3.set_xticks(range(0, 24, 3))

# Plot 4: Amount by category
ax4 = axes[1, 1]
category_fraud = df.groupby('amount_category')['is_fraud'].mean() * 100
ax4.bar(category_fraud.index, category_fraud.values, color='teal')
ax4.set_xlabel('Amount Category')
ax4.set_ylabel('Fraud Rate (%)')
ax4.set_title('Fraud Rate by Amount Category')

plt.tight_layout()
plt.savefig('../data/fraud_analysis_dashboard.png', dpi=300, bbox_inches='tight')
print("✅ Dashboard saved as 'fraud_analysis_dashboard.png'")

# 3. Key insights
print("\n💡 KEY INSIGHTS:")
print("-" * 40)

# Insight 1: Most common fraud type
top_fraud_type = fraud_rate_by_type.idxmax()
top_fraud_rate = fraud_rate_by_type.max()
print(f"🔹 Highest fraud rate: '{top_fraud_type}' ({top_fraud_rate:.1f}%)")

# Insight 2: Time pattern
peak_fraud_hour = hourly_fraud.idxmax()
print(f"🔹 Peak fraud hour: {peak_fraud_hour}:00 (fraud rate: {hourly_fraud.max():.1f}%)")

# Insight 3: Amount pattern
high_risk_category = category_fraud.idxmax()
print(f"🔹 Riskiest amount category: '{high_risk_category}'")

# Insight 4: Average fraud amount vs legitimate
fraud_avg = df[df['is_fraud'] == 1]['amount'].mean()
legit_avg = df[df['is_fraud'] == 0]['amount'].mean()
print(f"🔹 Average fraud amount: ${fraud_avg:.2f} vs legitimate: ${legit_avg:.2f}")

print("\n" + "=" * 60)
print("✅ Analysis complete!")