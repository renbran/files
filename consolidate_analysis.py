import csv
import json
from collections import Counter, defaultdict
from datetime import datetime

print("=" * 80)
print("CONSOLIDATED ANALYSIS: Lead Generation vs Sales Performance")
print("=" * 80)

# Read the original lead analysis file (all leads including lost)
print("\n📊 Loading Original Leads Data (faraz analysis.csv)...")
original_data = []
with open('faraz analysis.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        original_data.append(row)

print(f"   ✓ Total Leads (All): {len(original_data):,}")

# Read the new sales pipeline file (active/converted deals)
print("\n📊 Loading Sales Pipeline Data (2024-2025.csv)...")
pipeline_data = []
with open('2024-2025.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pipeline_data.append(row)

print(f"   ✓ Total Pipeline Records: {len(pipeline_data):,}")

print("\n" + "=" * 80)
print("PIPELINE ANALYSIS (2024-2025.csv)")
print("=" * 80)

# Analyze stages in the new file
stages = Counter(row['Stage'] for row in pipeline_data if row.get('Stage'))
print("\n🎯 STAGE Distribution:")
for stage, count in stages.most_common():
    percentage = (count / len(pipeline_data)) * 100
    print(f"   {stage:25s}: {count:6,} ({percentage:5.2f}%)")

# Analyze sources in pipeline
sources_pipeline = Counter(row['Source'] for row in pipeline_data if row.get('Source'))
print("\n📍 SOURCE Distribution in Pipeline:")
for source, count in sources_pipeline.most_common(15):
    percentage = (count / len(pipeline_data)) * 100
    print(f"   {source:25s}: {count:6,} ({percentage:5.2f}%)")

# Analyze responsible agents in pipeline
agents_pipeline = Counter(row['Responsible'] for row in pipeline_data if row.get('Responsible'))
print("\n👤 TOP 15 Agents in Pipeline:")
for agent, count in agents_pipeline.most_common(15):
    percentage = (count / len(pipeline_data)) * 100
    print(f"   {agent:30s}: {count:6,} ({percentage:5.2f}%)")

# Analyze dates
print("\n📅 Date Analysis:")
dates_2024 = sum(1 for row in pipeline_data if '2024' in row.get('Created', ''))
dates_2025 = sum(1 for row in pipeline_data if '2025' in row.get('Created', ''))
print(f"   2024 Leads: {dates_2024:,}")
print(f"   2025 Leads: {dates_2025:,}")

# Stage conversion analysis by source
print("\n" + "=" * 80)
print("CONVERSION FUNNEL BY SOURCE")
print("=" * 80)

source_stages = defaultdict(lambda: defaultdict(int))
for row in pipeline_data:
    source = row.get('Source', 'Unknown')
    stage = row.get('Stage', 'Unknown')
    if source and stage:
        source_stages[source][stage] += 1

# Define successful stages (customize based on your business process)
successful_stages = ['CLOSED', 'WON', 'DEAL WON', 'SUCCESSFUL']
active_stages = ['CONTACTED', 'OPTIONS SENT', 'VIEWING', 'NEGOTIATION', 'PROPOSAL']
early_stages = ['NEW', 'ATTEMPT', 'CONTACTED']

print("\nTop Sources Performance:")
for source, stages_count in sorted(source_stages.items(), key=lambda x: sum(x[1].values()), reverse=True)[:10]:
    total = sum(stages_count.values())
    successful = sum(stages_count.get(stage, 0) for stage in successful_stages)
    active = sum(stages_count.get(stage, 0) for stage in active_stages)

    print(f"\n{source}:")
    print(f"   Total: {total:,}")
    print(f"   Active Pipeline: {active} ({(active/total)*100:.1f}%)")
    if successful > 0:
        print(f"   ✅ Successful: {successful} ({(successful/total)*100:.1f}%)")

# Compare with original data
print("\n" + "=" * 80)
print("COMPARISON: Original Leads vs Current Pipeline")
print("=" * 80)

# Count statuses in original data
original_status = Counter(row.get('STATUS', 'Unknown') for row in original_data)
print("\nOriginal Data Status:")
for status, count in original_status.most_common():
    percentage = (count / len(original_data)) * 100
    print(f"   {status:20s}: {count:6,} ({percentage:5.2f}%)")

print("\n" + "=" * 80)
print("KEY INSIGHTS")
print("=" * 80)

# Calculate key metrics
original_lost_rate = (original_status.get('DEAL LOST', 0) / len(original_data)) * 100
original_closed_rate = (original_status.get('CLOSED', 0) / len(original_data)) * 100

print(f"\n📉 Original Dataset (faraz analysis.csv):")
print(f"   - Total Leads: {len(original_data):,}")
print(f"   - Deal Lost Rate: {original_lost_rate:.2f}%")
print(f"   - Closed Rate: {original_closed_rate:.2f}%")

print(f"\n📈 Current Pipeline (2024-2025.csv):")
print(f"   - Total Records: {len(pipeline_data):,}")
print(f"   - Most Common Stage: {stages.most_common(1)[0][0]} ({stages.most_common(1)[0][1]:,})")

# Identify leads that might be in both datasets
common_sources_orig = set(row.get('Source', '') for row in original_data if row.get('Source'))
common_sources_pipe = set(row.get('Source', '') for row in pipeline_data if row.get('Source'))
overlapping_sources = common_sources_orig & common_sources_pipe

print(f"\n🔄 Data Overlap:")
print(f"   - Common Sources: {len(overlapping_sources)}")
print(f"   - Sources: {', '.join(sorted(overlapping_sources)[:10])}")

# Calculate total unique leads if we can match by ID
original_ids = set(str(row.get('ID', '')) for row in original_data if row.get('ID'))
pipeline_ids = set(str(row.get('ID', '')) for row in pipeline_data if row.get('ID'))
overlapping_ids = original_ids & pipeline_ids

print(f"\n🆔 ID Overlap:")
print(f"   - Leads in both datasets: {len(overlapping_ids):,}")
print(f"   - Unique to original: {len(original_ids - pipeline_ids):,}")
print(f"   - Unique to pipeline: {len(pipeline_ids - original_ids):,}")

# Save consolidated stats
consolidated_stats = {
    'original_data': {
        'total_leads': len(original_data),
        'status_distribution': dict(original_status),
        'deal_lost_rate': original_lost_rate,
        'closed_rate': original_closed_rate
    },
    'pipeline_data': {
        'total_records': len(pipeline_data),
        'stage_distribution': dict(stages),
        'source_distribution': dict(sources_pipeline.most_common(20)),
        'top_agents': dict(agents_pipeline.most_common(15)),
        'year_distribution': {'2024': dates_2024, '2025': dates_2025}
    },
    'comparison': {
        'overlapping_lead_ids': len(overlapping_ids),
        'unique_to_original': len(original_ids - pipeline_ids),
        'unique_to_pipeline': len(pipeline_ids - original_ids),
        'common_sources': list(overlapping_sources)
    }
}

with open('consolidated_analysis_stats.json', 'w') as f:
    json.dump(consolidated_stats, f, indent=2)

print("\n✅ Analysis complete! Stats saved to consolidated_analysis_stats.json")
print("=" * 80)
