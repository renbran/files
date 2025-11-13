import csv
import json
from collections import Counter, defaultdict
from datetime import datetime

# Read the CSV file
data = []
with open('faraz analysis.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append(row)

print(f"Total Leads: {len(data)}")

# Analyze STATUS
status_counts = Counter(row['STATUS'] for row in data if row['STATUS'])
print("\n=== STATUS Distribution ===")
for status, count in status_counts.most_common():
    percentage = (count / len(data)) * 100
    print(f"{status}: {count} ({percentage:.2f}%)")

# Analyze SOURCE
source_counts = Counter(row['Source'] for row in data if row['Source'])
print("\n=== SOURCE Distribution ===")
for source, count in source_counts.most_common():
    percentage = (count / len(data)) * 100
    print(f"{source}: {count} ({percentage:.2f}%)")

# Analyze Responsible (Top 15)
responsible_counts = Counter(row['Responsible'] for row in data if row['Responsible'])
print("\n=== TOP 15 Responsible Agents ===")
for agent, count in responsible_counts.most_common(15):
    percentage = (count / len(data)) * 100
    print(f"{agent}: {count} ({percentage:.2f}%)")

# Analyze Internal/External
internal_external = Counter(row['Internal/External'] for row in data if row['Internal/External'])
print("\n=== Internal/External Distribution ===")
for type_, count in internal_external.items():
    percentage = (count / len(data)) * 100
    print(f"{type_}: {count} ({percentage:.2f}%)")

# Analyze dates
dates_by_month = defaultdict(int)
dates_2024 = 0
dates_2025 = 0

for row in data:
    if row['Created']:
        try:
            # Parse date (DD/MM/YYYY format)
            parts = row['Created'].split('/')
            if len(parts) == 3:
                day, month, year = parts
                dates_by_month[f"{year}-{month.zfill(2)}"] += 1
                if year == '2024':
                    dates_2024 += 1
                elif year == '2025':
                    dates_2025 += 1
        except:
            pass

print("\n=== Year Distribution ===")
print(f"2024 Leads: {dates_2024}")
print(f"2025 Leads: {dates_2025}")

print("\n=== Monthly Distribution (Top 10) ===")
for month, count in sorted(dates_by_month.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"{month}: {count}")

# Analyze conversion by source
conversion_by_source = defaultdict(lambda: {'total': 0, 'lost': 0, 'inprocess': 0})
for row in data:
    source = row['Source']
    status = row['STATUS']
    if source and status:
        conversion_by_source[source]['total'] += 1
        if status == 'DEAL LOST':
            conversion_by_source[source]['lost'] += 1
        elif status == 'INPROCESS':
            conversion_by_source[source]['inprocess'] += 1

print("\n=== Conversion Rate by Source ===")
for source, stats in sorted(conversion_by_source.items(), key=lambda x: x[1]['total'], reverse=True):
    if stats['total'] > 100:  # Only show sources with significant data
        lost_rate = (stats['lost'] / stats['total']) * 100
        inprocess_rate = (stats['inprocess'] / stats['total']) * 100
        print(f"{source}: Total={stats['total']}, InProcess={inprocess_rate:.1f}%, Lost={lost_rate:.1f}%")

# Save detailed stats to JSON
stats = {
    'total_leads': len(data),
    'status_distribution': dict(status_counts),
    'source_distribution': dict(source_counts.most_common(20)),
    'top_agents': dict(responsible_counts.most_common(15)),
    'year_distribution': {'2024': dates_2024, '2025': dates_2025},
    'monthly_distribution': dict(sorted(dates_by_month.items())[-12:])
}

with open('lead_analysis_stats.json', 'w') as f:
    json.dump(stats, f, indent=2)

print("\n✓ Analysis complete! Stats saved to lead_analysis_stats.json")
