total_jobs = 0
selected_jobs = 0

if total_jobs > 0:
    success_rate = (selected_jobs / total_jobs) * 100
else:
    success_rate = 0

print("Success Rate:", success_rate, "%")