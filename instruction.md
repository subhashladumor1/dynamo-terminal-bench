There is an Apache access log at `/app/access.log`. Parse it and write a JSON report to `/app/report.json`.

**Success criteria — your submission passes when ALL of the following are true:**

1. `/app/report.json` exists and contains valid JSON with keys `total_requests`, `unique_ips`, and `top_path`.
2. `total_requests` is an integer equal to the number of non-blank lines in the log.
3. `unique_ips` is an integer equal to the number of distinct client IP addresses in the log.
4. `top_path` is a string equal to the URL path that appears in the most requests.

**Required output format:**

```json
{"total_requests": 6, "unique_ips": 3, "top_path": "/index.html"}
```

Save the result to `/app/report.json`. No other output files are required.
