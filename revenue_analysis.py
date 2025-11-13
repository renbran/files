import csv
import json
from collections import Counter, defaultdict

print("=" * 80)
print("REVENUE & CONVERSION ANALYSIS")
print("=" * 80)

# Read pipeline data
pipeline_data = []
with open('2024-2025.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pipeline_data.append(row)

# Define conversion stages
conversion_stages = {
    'CUSTOMER': 'Converted Customer',
    'HOT': 'Hot Lead',
    'OPTIONS SENT': 'Options Sent',
    'CONTACTED': 'Contacted',
    'ATTEMPT': 'Attempted Contact',
    'NEW': 'New Lead',
    'IDLE': 'Idle',
    'UNSUCCESSFUL': 'Unsuccessful',
    'Junk Lead': 'Junk Lead'
}

print("\n📊 CONVERSION FUNNEL ANALYSIS")
print("=" * 80)

# Count by stage
stage_counts = Counter(row['Stage'] for row in pipeline_data if row.get('Stage'))

# Calculate funnel metrics
total_leads = len(pipeline_data)
customers = stage_counts.get('CUSTOMER', 0)
hot_leads = stage_counts.get('HOT', 0)
options_sent = stage_counts.get('OPTIONS SENT', 0)
contacted = stage_counts.get('CONTACTED', 0)
attempts = stage_counts.get('ATTEMPT', 0)
new_leads = stage_counts.get('NEW', 0)
unsuccessful = stage_counts.get('UNSUCCESSFUL', 0)
junk = stage_counts.get('Junk Lead', 0)

print(f"\n🎯 Sales Funnel (Top to Bottom):")
print(f"   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print(f"   📥 Total Leads:           {total_leads:6,} (100.00%)")
print(f"   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print(f"   ├─ 🗑️  Junk Leads:         {junk:6,} ({(junk/total_leads)*100:5.2f}%) [Removed]")
print(f"   │")
print(f"   └─ 📊 Qualified Leads:    {total_leads - junk:6,} ({((total_leads-junk)/total_leads)*100:5.2f}%)")
print(f"      ├─ 🔵 NEW:             {new_leads:6,} ({(new_leads/total_leads)*100:5.2f}%)")
print(f"      ├─ 📞 ATTEMPT:         {attempts:6,} ({(attempts/total_leads)*100:5.2f}%)")
print(f"      ├─ ✅ CONTACTED:       {contacted:6,} ({(contacted/total_leads)*100:5.2f}%)")
print(f"      ├─ 📋 OPTIONS SENT:    {options_sent:6,} ({(options_sent/total_leads)*100:5.2f}%)")
print(f"      ├─ 🔥 HOT:             {hot_leads:6,} ({(hot_leads/total_leads)*100:5.2f}%)")
print(f"      ├─ ✅ CUSTOMER:        {customers:6,} ({(customers/total_leads)*100:5.2f}%) [CONVERTED!]")
print(f"      └─ ❌ UNSUCCESSFUL:    {unsuccessful:6,} ({(unsuccessful/total_leads)*100:5.2f}%)")

# Conversion rates
qualified_leads = total_leads - junk
conversion_rate = (customers / total_leads) * 100 if total_leads > 0 else 0
qualified_conversion_rate = (customers / qualified_leads) * 100 if qualified_leads > 0 else 0

print(f"\n📈 KEY METRICS:")
print(f"   - Overall Conversion Rate:     {conversion_rate:.2f}% (Customers / All Leads)")
print(f"   - Qualified Conversion Rate:   {qualified_conversion_rate:.2f}% (Customers / Non-Junk Leads)")
print(f"   - Active Pipeline:             {contacted + options_sent + hot_leads:,} leads")
print(f"   - Win Rate Potential:          {(customers / (customers + unsuccessful)) * 100 if (customers + unsuccessful) > 0 else 0:.2f}%")

# Analyze conversion by source
print("\n" + "=" * 80)
print("CONVERSION RATE BY SOURCE")
print("=" * 80)

source_conversion = defaultdict(lambda: {'total': 0, 'customers': 0, 'hot': 0, 'options_sent': 0,
                                         'contacted': 0, 'unsuccessful': 0, 'junk': 0})

for row in pipeline_data:
    source = row.get('Source', 'Unknown')
    stage = row.get('Stage', '')

    if source:
        source_conversion[source]['total'] += 1
        if stage == 'CUSTOMER':
            source_conversion[source]['customers'] += 1
        elif stage == 'HOT':
            source_conversion[source]['hot'] += 1
        elif stage == 'OPTIONS SENT':
            source_conversion[source]['options_sent'] += 1
        elif stage == 'CONTACTED':
            source_conversion[source]['contacted'] += 1
        elif stage == 'UNSUCCESSFUL':
            source_conversion[source]['unsuccessful'] += 1
        elif stage == 'Junk Lead':
            source_conversion[source]['junk'] += 1

print("\n🏆 SOURCE PERFORMANCE (sorted by customer conversion):")
print(f"\n{'Source':25s} {'Total':>8s} {'Customers':>10s} {'Conv%':>8s} {'Active':>8s} {'Junk%':>8s}")
print("─" * 85)

sorted_sources = sorted(source_conversion.items(),
                       key=lambda x: x[1]['customers'],
                       reverse=True)

for source, metrics in sorted_sources[:15]:
    total = metrics['total']
    customers = metrics['customers']
    active = metrics['contacted'] + metrics['options_sent'] + metrics['hot']
    junk = metrics['junk']

    conv_rate = (customers / total) * 100 if total > 0 else 0
    junk_rate = (junk / total) * 100 if total > 0 else 0

    print(f"{source:25s} {total:8,} {customers:10,} {conv_rate:7.2f}% {active:8,} {junk_rate:7.2f}%")

# Analyze conversion by agent
print("\n" + "=" * 80)
print("AGENT PERFORMANCE - TOP CONVERTERS")
print("=" * 80)

agent_conversion = defaultdict(lambda: {'total': 0, 'customers': 0, 'hot': 0, 'options_sent': 0,
                                       'contacted': 0, 'unsuccessful': 0})

for row in pipeline_data:
    agent = row.get('Responsible', 'Unknown')
    stage = row.get('Stage', '')

    if agent and agent != 'CRM System':  # Exclude CRM System
        agent_conversion[agent]['total'] += 1
        if stage == 'CUSTOMER':
            agent_conversion[agent]['customers'] += 1
        elif stage == 'HOT':
            agent_conversion[agent]['hot'] += 1
        elif stage == 'OPTIONS SENT':
            agent_conversion[agent]['options_sent'] += 1
        elif stage == 'CONTACTED':
            agent_conversion[agent]['contacted'] += 1
        elif stage == 'UNSUCCESSFUL':
            agent_conversion[agent]['unsuccessful'] += 1

print(f"\n{'Agent':30s} {'Total':>8s} {'Customers':>10s} {'Conv%':>8s} {'Pipeline':>10s}")
print("─" * 85)

sorted_agents = sorted(agent_conversion.items(),
                      key=lambda x: x[1]['customers'],
                      reverse=True)

for agent, metrics in sorted_agents[:20]:
    if metrics['total'] >= 10:  # Only show agents with at least 10 leads
        total = metrics['total']
        customers = metrics['customers']
        pipeline = metrics['contacted'] + metrics['options_sent'] + metrics['hot']

        conv_rate = (customers / total) * 100 if total > 0 else 0

        print(f"{agent:30s} {total:8,} {customers:10,} {conv_rate:7.2f}% {pipeline:10,}")

# Monthly conversion analysis
print("\n" + "=" * 80)
print("MONTHLY PERFORMANCE")
print("=" * 80)

monthly_data = defaultdict(lambda: {'leads': 0, 'customers': 0})

for row in pipeline_data:
    created = row.get('Created', '')
    stage = row.get('Stage', '')

    if created and '/' in created:
        try:
            parts = created.split('/')
            if len(parts) == 3:
                day, month, year = parts
                month_key = f"{year}-{month.zfill(2)}"
                monthly_data[month_key]['leads'] += 1
                if stage == 'CUSTOMER':
                    monthly_data[month_key]['customers'] += 1
        except:
            pass

print(f"\n{'Month':12s} {'Leads':>10s} {'Customers':>12s} {'Conv%':>8s}")
print("─" * 50)

for month in sorted(monthly_data.keys())[-12:]:  # Last 12 months
    metrics = monthly_data[month]
    leads = metrics['leads']
    customers = metrics['customers']
    conv_rate = (customers / leads) * 100 if leads > 0 else 0

    print(f"{month:12s} {leads:10,} {customers:12,} {conv_rate:7.2f}%")

# Calculate projected revenue (assuming average deal value)
print("\n" + "=" * 80)
print("REVENUE PROJECTIONS")
print("=" * 80)

# These are example values - adjust based on your actual average deal values
AVERAGE_DEAL_VALUES = {
    'low_estimate': 50000,    # AED 50,000
    'mid_estimate': 150000,   # AED 150,000
    'high_estimate': 500000   # AED 500,000
}

print(f"\n💰 Revenue Estimates (Total Customers: {customers:,}):")
print(f"   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

for scenario, deal_value in AVERAGE_DEAL_VALUES.items():
    total_revenue = customers * deal_value
    print(f"   {scenario.replace('_', ' ').title():20s}: AED {total_revenue:15,} (@ AED {deal_value:,} per deal)")

print(f"\n💡 NOTE: These are projections based on assumed average deal values.")
print(f"   Update AVERAGE_DEAL_VALUES in the script with actual data for accurate figures.")

# Save detailed conversion analysis
conversion_analysis = {
    'funnel_metrics': {
        'total_leads': total_leads,
        'qualified_leads': qualified_leads,
        'customers': customers,
        'hot_leads': hot_leads,
        'options_sent': options_sent,
        'contacted': contacted,
        'attempts': attempts,
        'new_leads': new_leads,
        'unsuccessful': unsuccessful,
        'junk_leads': junk
    },
    'conversion_rates': {
        'overall_conversion_rate': conversion_rate,
        'qualified_conversion_rate': qualified_conversion_rate
    },
    'source_performance': {
        source: {
            'total': metrics['total'],
            'customers': metrics['customers'],
            'conversion_rate': (metrics['customers'] / metrics['total'] * 100) if metrics['total'] > 0 else 0,
            'active_pipeline': metrics['contacted'] + metrics['options_sent'] + metrics['hot']
        }
        for source, metrics in sorted_sources[:20]
    },
    'top_agents': {
        agent: {
            'total': metrics['total'],
            'customers': metrics['customers'],
            'conversion_rate': (metrics['customers'] / metrics['total'] * 100) if metrics['total'] > 0 else 0
        }
        for agent, metrics in sorted_agents[:20] if metrics['total'] >= 10
    }
}

with open('conversion_analysis_stats.json', 'w') as f:
    json.dump(conversion_analysis, f, indent=2)

print("\n✅ Analysis complete! Stats saved to conversion_analysis_stats.json")
print("=" * 80)
