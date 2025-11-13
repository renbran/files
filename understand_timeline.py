import csv
from collections import defaultdict
from datetime import datetime

print("=" * 80)
print("UNDERSTANDING YOUR DATA TIMELINE")
print("=" * 80)

# Read pipeline data
pipeline_data = []
with open('2024-2025.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pipeline_data.append(row)

print(f"\n📊 Total Records: {len(pipeline_data):,}")

# Parse all dates and organize by month
monthly_breakdown = defaultdict(lambda: {'total': 0, 'by_stage': defaultdict(int), 'by_source': defaultdict(int)})

for row in pipeline_data:
    created = row.get('Created', '')
    stage = row.get('Stage', 'Unknown')
    source = row.get('Source', 'Unknown')

    if created and '/' in created:
        try:
            parts = created.split('/')
            if len(parts) == 3:
                day, month, year = parts
                month_key = f"{year}-{month.zfill(2)}"

                monthly_breakdown[month_key]['total'] += 1
                monthly_breakdown[month_key]['by_stage'][stage] += 1
                monthly_breakdown[month_key]['by_source'][source] += 1
        except:
            pass

print("\n" + "=" * 80)
print("MONTHLY BREAKDOWN OF ALL LEADS")
print("=" * 80)

print(f"\n{'Month':12s} {'Total Leads':>12s} {'% of Total':>12s}")
print("─" * 40)

total_leads = len(pipeline_data)
for month in sorted(monthly_breakdown.keys()):
    leads = monthly_breakdown[month]['total']
    percentage = (leads / total_leads) * 100
    print(f"{month:12s} {leads:12,} {percentage:11.2f}%")

# Show cumulative by period
print("\n" + "=" * 80)
print("CUMULATIVE BY PERIOD")
print("=" * 80)

# 2024
leads_2024 = sum(monthly_breakdown[m]['total'] for m in monthly_breakdown if m.startswith('2024'))
print(f"\n📅 2024 Total: {leads_2024:,} leads")

# 2025 by quarter
q1_2025 = sum(monthly_breakdown[m]['total'] for m in monthly_breakdown if m.startswith('2025') and m.split('-')[1] in ['01', '02', '03'])
q2_2025 = sum(monthly_breakdown[m]['total'] for m in monthly_breakdown if m.startswith('2025') and m.split('-')[1] in ['04', '05', '06'])
q3_2025 = sum(monthly_breakdown[m]['total'] for m in monthly_breakdown if m.startswith('2025') and m.split('-')[1] in ['07', '08', '09'])
q4_2025 = sum(monthly_breakdown[m]['total'] for m in monthly_breakdown if m.startswith('2025') and m.split('-')[1] in ['10', '11', '12'])

print(f"\n📅 2025 Q1 (Jan-Mar): {q1_2025:,} leads")
print(f"📅 2025 Q2 (Apr-Jun): {q2_2025:,} leads")
print(f"📅 2025 Q3 (Jul-Sep): {q3_2025:,} leads")
print(f"📅 2025 Q4 (Oct-Nov): {q4_2025:,} leads")

# Post-June 2025 (July onwards)
post_june_2025 = sum(monthly_breakdown[m]['total'] for m in monthly_breakdown
                     if m.startswith('2025') and int(m.split('-')[1]) >= 7)

print(f"\n📅 Post-June 2025 (Jul-Nov): {post_june_2025:,} leads")
print(f"   That's {(post_june_2025/total_leads)*100:.1f}% of all leads")

# Calculate realistic conversion with 522 deals
ACTUAL_DEALS = 522

print("\n" + "=" * 80)
print("CONVERSION SCENARIOS WITH 522 ACTUAL DEALS")
print("=" * 80)

print(f"\n💰 You have: {ACTUAL_DEALS} actual closed deals")
print(f"📊 You have: {total_leads:,} total leads in system")

# Scenario 1: All deals from all leads
conv_all = (ACTUAL_DEALS / total_leads) * 100
print(f"\n📊 Scenario 1: All 522 deals from all {total_leads:,} leads")
print(f"   Conversion Rate: {conv_all:.2f}%")

# Scenario 2: Deals proportional to post-June
if post_june_2025 > 0:
    # If we assume deals came proportionally
    estimated_post_june_deals = int((post_june_2025 / total_leads) * ACTUAL_DEALS)
    conv_post_june_prop = (estimated_post_june_deals / post_june_2025) * 100

    print(f"\n📊 Scenario 2: Deals proportional to lead volume")
    print(f"   Post-June leads: {post_june_2025:,} ({(post_june_2025/total_leads)*100:.1f}% of total)")
    print(f"   Expected post-June deals: ~{estimated_post_june_deals} ({(estimated_post_june_deals/ACTUAL_DEALS)*100:.1f}% of {ACTUAL_DEALS})")
    print(f"   Conversion Rate: {conv_post_june_prop:.2f}%")

# Scenario 3: Most deals are from post-June (since that's when tracking improved)
if post_june_2025 > 0:
    # Assume 70% of deals are from post-June period
    post_june_deals_70pct = int(ACTUAL_DEALS * 0.7)
    conv_70pct = (post_june_deals_70pct / post_june_2025) * 100

    print(f"\n📊 Scenario 3: 70% of deals from post-June period")
    print(f"   Post-June deals: ~{post_june_deals_70pct} (70% of {ACTUAL_DEALS})")
    print(f"   Post-June leads: {post_june_2025:,}")
    print(f"   Conversion Rate: {conv_70pct:.2f}%")

# Scenario 4: Equal deals per month
months_with_data = len([m for m in monthly_breakdown if monthly_breakdown[m]['total'] > 0])
deals_per_month = ACTUAL_DEALS / months_with_data
post_june_months = len([m for m in monthly_breakdown if m.startswith('2025') and int(m.split('-')[1]) >= 7])
estimated_post_june_deals_equal = int(deals_per_month * post_june_months)

if post_june_2025 > 0:
    conv_equal_monthly = (estimated_post_june_deals_equal / post_june_2025) * 100

    print(f"\n📊 Scenario 4: Equal deals per month ({deals_per_month:.1f} deals/month)")
    print(f"   Post-June months: {post_june_months}")
    print(f"   Post-June deals: ~{estimated_post_june_deals_equal}")
    print(f"   Post-June leads: {post_june_2025:,}")
    print(f"   Conversion Rate: {conv_equal_monthly:.2f}%")

print("\n" + "=" * 80)
print("BY SOURCE ANALYSIS (Post-June 2025)")
print("=" * 80)

# Aggregate post-June sources
post_june_sources = defaultdict(int)
for month in monthly_breakdown:
    if month.startswith('2025') and int(month.split('-')[1]) >= 7:
        for source, count in monthly_breakdown[month]['by_source'].items():
            post_june_sources[source] += count

print(f"\n📍 Post-June Lead Sources ({post_june_2025:,} total leads):")
print(f"\n{'Source':25s} {'Leads':>10s} {'% of Leads':>12s} {'Est. Deals*':>12s}")
print("─" * 65)

# Sort by volume
sorted_sources = sorted(post_june_sources.items(), key=lambda x: x[1], reverse=True)
for source, count in sorted_sources[:15]:
    lead_pct = (count / post_june_2025) * 100 if post_june_2025 > 0 else 0
    # Estimate deals proportionally (using 70% scenario)
    est_deals = int((count / post_june_2025) * post_june_deals_70pct) if post_june_2025 > 0 else 0

    print(f"{source:25s} {count:10,} {lead_pct:11.2f}% {est_deals:12,}")

print(f"\n* Estimated assuming 70% of {ACTUAL_DEALS} deals ({post_june_deals_70pct}) from post-June")

print("\n" + "=" * 80)
print("RECOMMENDATION")
print("=" * 80)

print(f"\n✅ MOST REALISTIC INTERPRETATION:")
print(f"\n   If you started proper Bitrix tracking after June 2025:")
print(f"   - Post-June leads: {post_june_2025:,}")
print(f"   - Realistic conversion estimate: {conv_70pct:.2f}% (assuming 70% of deals from this period)")
print(f"   - This means ~{post_june_deals_70pct} of your {ACTUAL_DEALS} deals came from {post_june_2025:,} tracked leads")
print(f"\n   This is MUCH more realistic than 0.74%!")
print(f"   It suggests your actual conversion rate is closer to {conv_70pct:.1f}%")

print("\n" + "=" * 80)
