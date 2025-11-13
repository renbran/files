import csv
import json
from collections import Counter, defaultdict
from datetime import datetime

print("=" * 80)
print("REALISTIC ANALYSIS: Post-June 2025 + 522 Actual Deals")
print("=" * 80)

# Read pipeline data
pipeline_data = []
with open('2024-2025.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pipeline_data.append(row)

print(f"\n📊 Total Records in Pipeline: {len(pipeline_data):,}")

# Filter for post-June 2025 data (July 2025 onwards)
post_june_data = []
for row in pipeline_data:
    created = row.get('Created', '')
    if created and '/' in created:
        try:
            parts = created.split('/')
            if len(parts) == 3:
                day, month, year = parts
                # Check if 2025 and month >= 07
                if year == '2025' and int(month) >= 7:
                    post_june_data.append(row)
        except:
            pass

print(f"📅 Post-June 2025 Records: {len(post_june_data):,}")
print(f"   (July 2025 onwards - when Bitrix tracking started)")

# Analyze the full dataset to understand stages
print("\n" + "=" * 80)
print("UNDERSTANDING THE DATA")
print("=" * 80)

all_stages = Counter(row['Stage'] for row in pipeline_data if row.get('Stage'))
print("\n📊 All Stages in Dataset:")
for stage, count in all_stages.most_common():
    percentage = (count / len(pipeline_data)) * 100
    print(f"   {stage:25s}: {count:6,} ({percentage:5.2f}%)")

# Analyze post-June stages
post_june_stages = Counter(row['Stage'] for row in post_june_data if row.get('Stage'))
print("\n📊 Post-June 2025 Stages:")
for stage, count in post_june_stages.most_common():
    percentage = (count / len(post_june_data)) * 100 if post_june_data else 0
    print(f"   {stage:25s}: {count:6,} ({percentage:5.2f}%)")

# CRITICAL: We have 522 ACTUAL deals
ACTUAL_DEALS = 522

print("\n" + "=" * 80)
print("REALISTIC CONVERSION ANALYSIS")
print("=" * 80)

print(f"\n💰 ACTUAL DEALS: {ACTUAL_DEALS}")
print(f"📊 Total Leads in System: {len(pipeline_data):,}")
print(f"📅 Post-June Leads (Tracked Period): {len(post_june_data):,}")

# Calculate realistic conversion rate
# If we have 522 deals and 29,768 leads, but only post-June is tracked properly
realistic_conversion = (ACTUAL_DEALS / len(pipeline_data)) * 100
post_june_conversion = (ACTUAL_DEALS / len(post_june_data)) * 100 if post_june_data else 0

print(f"\n📈 Conversion Rates:")
print(f"   Overall (522 deals / {len(pipeline_data):,} leads): {realistic_conversion:.2f}%")
print(f"   Post-June Rate (if all 522 came from post-June): {post_june_conversion:.2f}%")

# Analyze by source for post-June data
print("\n" + "=" * 80)
print("POST-JUNE 2025 SOURCE ANALYSIS")
print("=" * 80)

source_counts_post_june = Counter(row['Source'] for row in post_june_data if row.get('Source'))
print(f"\n📍 Source Distribution (Post-June {len(post_june_data):,} leads):")
for source, count in source_counts_post_june.most_common(15):
    percentage = (count / len(post_june_data)) * 100 if post_june_data else 0
    print(f"   {source:25s}: {count:6,} ({percentage:5.2f}%)")

# Calculate expected deals by source proportion
print(f"\n💰 ESTIMATED DEAL DISTRIBUTION (Based on {ACTUAL_DEALS} actual deals):")
print(f"\nAssuming deals distributed proportionally to lead volume:")
print(f"\n{'Source':25s} {'Leads':>8s} {'Lead%':>8s} {'Est. Deals':>12s} {'Conv%':>8s}")
print("─" * 85)

for source, count in source_counts_post_june.most_common(15):
    lead_percentage = (count / len(post_june_data)) * 100 if post_june_data else 0
    estimated_deals = int((count / len(post_june_data)) * ACTUAL_DEALS) if post_june_data else 0
    source_conversion = (estimated_deals / count * 100) if count > 0 else 0

    print(f"{source:25s} {count:8,} {lead_percentage:7.2f}% {estimated_deals:12,} {source_conversion:7.2f}%")

# Analyze by month for post-June
print("\n" + "=" * 80)
print("MONTHLY BREAKDOWN (Post-June 2025)")
print("=" * 80)

monthly_post_june = defaultdict(int)
for row in post_june_data:
    created = row.get('Created', '')
    if created and '/' in created:
        try:
            parts = created.split('/')
            if len(parts) == 3:
                day, month, year = parts
                month_key = f"{year}-{month.zfill(2)}"
                monthly_post_june[month_key] += 1
        except:
            pass

print(f"\n{'Month':12s} {'Leads':>10s} {'% of Post-June':>15s}")
print("─" * 45)
for month in sorted(monthly_post_june.keys()):
    leads = monthly_post_june[month]
    percentage = (leads / len(post_june_data)) * 100 if post_june_data else 0
    print(f"{month:12s} {leads:10,} {percentage:14.2f}%")

# Calculate realistic conversion if we assume different scenarios
print("\n" + "=" * 80)
print("SCENARIO ANALYSIS")
print("=" * 80)

print(f"\n📊 Scenario 1: All 522 deals from entire dataset ({len(pipeline_data):,} leads)")
print(f"   Conversion Rate: {(ACTUAL_DEALS / len(pipeline_data)) * 100:.2f}%")

print(f"\n📊 Scenario 2: 522 deals but only post-June leads matter ({len(post_june_data):,} leads)")
print(f"   Conversion Rate: {(ACTUAL_DEALS / len(post_june_data)) * 100 if post_june_data else 0:.2f}%")

# Let's calculate how many deals might have come from pre-June vs post-June
# If tracking started in June, let's estimate the split
pre_june_count = len(pipeline_data) - len(post_june_data)
print(f"\n📊 Scenario 3: Deals split by period")
print(f"   Pre-June period: {pre_june_count:,} leads")
print(f"   Post-June period: {len(post_june_data):,} leads")

# If we assume pre-June had low tracking, maybe only 20% of deals came from there
pre_june_deals_estimate = int(ACTUAL_DEALS * 0.2)
post_june_deals_estimate = int(ACTUAL_DEALS * 0.8)

print(f"\n   Conservative estimate:")
print(f"   - Pre-June deals (20%): ~{pre_june_deals_estimate} deals from {pre_june_count:,} leads = {(pre_june_deals_estimate/pre_june_count)*100 if pre_june_count > 0 else 0:.2f}%")
print(f"   - Post-June deals (80%): ~{post_june_deals_estimate} deals from {len(post_june_data):,} leads = {(post_june_deals_estimate/len(post_june_data))*100 if post_june_data else 0:.2f}%")

# Most realistic: Let's assume deals came proportionally but with better tracking post-June
# Calculate monthly average
months_total = len(set(monthly_post_june.keys()))
months_with_data = 12  # Roughly Oct 2024 - Nov 2025

post_june_months = len(set(monthly_post_june.keys()))
pre_june_months = months_with_data - post_june_months

deals_per_month = ACTUAL_DEALS / months_with_data
pre_june_deals = int(deals_per_month * pre_june_months)
post_june_deals = int(deals_per_month * post_june_months)

print(f"\n📊 Scenario 4: Equal monthly deal rate across {months_with_data} months")
print(f"   Deals per month: ~{deals_per_month:.1f}")
print(f"   Pre-June deals ({pre_june_months} months): ~{pre_june_deals} deals")
print(f"   Post-June deals ({post_june_months} months): ~{post_june_deals} deals")
print(f"   Post-June conversion: {(post_june_deals / len(post_june_data)) * 100 if post_june_data else 0:.2f}%")

# Save realistic analysis
realistic_stats = {
    'actual_deals': ACTUAL_DEALS,
    'total_leads': len(pipeline_data),
    'post_june_leads': len(post_june_data),
    'pre_june_leads': pre_june_count,
    'scenarios': {
        'scenario_1_all_leads': {
            'leads': len(pipeline_data),
            'deals': ACTUAL_DEALS,
            'conversion_rate': (ACTUAL_DEALS / len(pipeline_data)) * 100
        },
        'scenario_2_post_june_only': {
            'leads': len(post_june_data),
            'deals': ACTUAL_DEALS,
            'conversion_rate': (ACTUAL_DEALS / len(post_june_data)) * 100 if post_june_data else 0
        },
        'scenario_3_conservative_split': {
            'pre_june_deals': pre_june_deals_estimate,
            'post_june_deals': post_june_deals_estimate,
            'post_june_conversion': (post_june_deals_estimate / len(post_june_data)) * 100 if post_june_data else 0
        },
        'scenario_4_equal_monthly': {
            'pre_june_deals': pre_june_deals,
            'post_june_deals': post_june_deals,
            'post_june_conversion': (post_june_deals / len(post_june_data)) * 100 if post_june_data else 0,
            'deals_per_month': deals_per_month
        }
    },
    'post_june_source_distribution': dict(source_counts_post_june.most_common(20)),
    'monthly_breakdown': dict(monthly_post_june)
}

with open('realistic_analysis_stats.json', 'w') as f:
    json.dump(realistic_stats, f, indent=2)

print("\n" + "=" * 80)
print("MOST REALISTIC ESTIMATE")
print("=" * 80)

print(f"\n✅ RECOMMENDED INTERPRETATION:")
print(f"   Total Deals: {ACTUAL_DEALS}")
print(f"   Post-June Leads: {len(post_june_data):,}")
print(f"   Post-June Deals (assuming equal monthly rate): ~{post_june_deals}")
print(f"   Realistic Conversion Rate: {(post_june_deals / len(post_june_data)) * 100 if post_june_data else 0:.2f}%")
print(f"\n   This suggests: {(post_june_deals / len(post_june_data)) * 100 if post_june_data else 0:.1f}% conversion for tracked period")
print(f"   Much more realistic than the 0.74% calculated earlier!")

print("\n✅ Analysis complete! Stats saved to realistic_analysis_stats.json")
print("=" * 80)
