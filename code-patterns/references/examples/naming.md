# Naming Examples

Source base: `book1:chapter-7-simplicity`.

## Dense Local Calculation

Before shape:

```text
q = s(j, f, m)
p(q)
```

After shape:

```text
quarterly_total = sum_months(january, february, march)
print(quarterly_total)
```

Decision reason: the original names force the reader to infer meaning from implementation or external context. The replacement names are long enough to communicate the role, but still short enough to keep the lines readable.

Avoid condition: do not rename public symbols this way until consumers and compatibility are inspected.

## Overlong Name

Before shape:

```text
annual_revenue_for_company_in_fiscal_year_2026_as_of_current_report_date
```

After shape:

```text
reported_annual_revenue
```

Decision reason: overlong names can make expressions harder to scan. Keep the important distinction in the name and move extra detail to surrounding structure, type, or documentation when needed.

Avoid condition: do not shorten names so far that the symbol loses domain meaning.
