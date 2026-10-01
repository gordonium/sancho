---
name: Home Directions data census, part 2 queries
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: The read-only database queries that finish the census (which fields are filled, by era; duplicate emails; invoice totals and paid flags; compiled reports; relation shapes), written for the Nerd to run on the dev clone only, under the plugin kit's staging rules; not yet requested and not yet run
sources: ["[doc:census-2026-10-01.md]", "[doc:survey-hdonline.md]", "[doc:survey-hdonline-home-directions.md]", "[doc:~/Dev/clc-plugins/CLAUDE.md §10]"]
status: superseded as a plan 2026-10-01 late: Gordon said "Go ahead and census" and the queries were run from this thread, adapted, the same evening (results in census-part2-2026-10-01.md); kept as the record of what was intended, with the review's corrections noted below
---
# Census part 2: the queries

**Run 2026-10-01 late, adapted.** Results: `census-part2-2026-10-01.md`. What changed when they met the real database, and what an independent review found wrong in this draft:
- The clone runs MariaDB 10.3.17, and WP-CLI's database command works there although WordPress itself cannot load (the shell has PHP 7.3).
- The queries ran one statement per call with no trailing semicolon; the kit's guard now refuses `;` in a remote command.
- The clone turned out to hold v2's own `REPORTS` and `CONTACTS` tables, so "which fields are filled, by era" was answered from those, with the era taken from the job date. That also answers the review's point that era by post date is meaningless for contacts (their post date is the 2021 import date).
- Review corrections to the SQL as drafted: `AS groups` and `AS empty` are reserved words on MySQL 8 (use `n_groups`, `empty_rows`); `NOT LIKE 'field\_%'` drops NULL values (use `LEFT(meta_value,6) <> 'field_'` with an `IS NULL` branch); Q2 would have printed raw values of sparsely filled text fields, against this file's own rule (it was run for the paid flag and the inspector only); Q3 counted all contacts, not only clients (run on v2's `CONTACTS` with the client type instead); Q4's fee total would have summed only the base fee and mis-cast values with a currency sign (not run as a total); Q6 omitted `hdo_appt_additional_contacts` (included when run); Q7's `BETWEEN` stopped at midnight on the last day and looked only for dates after 2100 (run with `>=` and `<`).
- Added when run: a check that the post date is the job date (it is, on 10,209 of 10,212 appointments).

**Where:** the dev clone `hdonline-sancho.sitedistrict.com` only. Never live. The kit's live-site guard and staging rules apply. [doc:~/Dev/clc-plugins/CLAUDE.md §10]
**Needs first:** an SSH alias and key for the clone (not set up [doc:current-system.md]); Gordon installs the key. Then check whether `wp db query` works on that host; on some SiteDistrict hosts the shell's PHP is too old for WP-CLI to load WordPress. [doc:~/Dev/clc-plugins/skills/plugin-edit/SKILL.md:60] If it does not, stop and say so; do not read `wp-config.php` for credentials.
**Rules:** `SELECT` only. No `UPDATE`, `DELETE`, `INSERT`, `ALTER`, no temporary tables. Output is counts; never print names, emails, addresses or phone numbers. Replace `wp_` with the site's real table prefix (`wp db prefix`).
**Era** below means the post date: before 1996, 1996 to 2008, 2009 to 2020, 2021 on.

## Q1. Every field, how often it is filled, by era
```sql
SELECT p.post_type,
       pm.meta_key,
       CASE WHEN YEAR(p.post_date) < 1996 THEN 'a_before_1996'
            WHEN YEAR(p.post_date) < 2009 THEN 'b_1996_2008'
            WHEN YEAR(p.post_date) < 2021 THEN 'c_2009_2020'
            ELSE 'd_2021_on' END AS era,
       COUNT(*) AS rows_with_key,
       SUM(pm.meta_value IS NOT NULL AND pm.meta_value <> '' AND pm.meta_value <> 'a:0:{}') AS rows_filled,
       COUNT(DISTINCT pm.meta_value) AS distinct_values
FROM wp_posts p
JOIN wp_postmeta pm ON pm.post_id = p.ID
WHERE p.post_type IN ('hdo_appointments','hdo_contacts','hdo_properties','hdo_invoices','hdo_reports')
  AND p.post_status <> 'trash'
  AND pm.meta_value NOT LIKE 'field\_%'
  AND pm.meta_key NOT IN ('_edit_lock','_edit_last')
GROUP BY p.post_type, pm.meta_key, era
ORDER BY p.post_type, pm.meta_key, era;
```
Answers: which legacy fields are worth a column in v4 (R7.8), and which inspection-era fields are empty (R2.7).

## Q2. Values of the small fields (categories only)
For each key from Q1 where `distinct_values` is 25 or fewer, and the key is not a name, address, phone, email or notes field:
```sql
SELECT pm.meta_value, COUNT(*) AS n
FROM wp_posts p JOIN wp_postmeta pm ON pm.post_id = p.ID
WHERE p.post_type = '<type>' AND pm.meta_key = '<key>' AND p.post_status <> 'trash'
GROUP BY pm.meta_value ORDER BY n DESC;
```
Expected candidates: state, house type, water supply, sewage disposal, the invoice paid flag, the stamp choice, the copy-to flags.

## Q3. Clients sharing an email (the dedup key)
Find the email key name in Q1 first (contact details group), then:
```sql
SELECT COUNT(*) AS clients_with_email,
       COUNT(DISTINCT LOWER(TRIM(pm.meta_value))) AS distinct_emails
FROM wp_posts p JOIN wp_postmeta pm ON pm.post_id = p.ID
WHERE p.post_type = 'hdo_contacts' AND p.post_status <> 'trash'
  AND pm.meta_key = '<email key>' AND pm.meta_value <> '';

SELECT group_size, COUNT(*) AS groups
FROM (SELECT COUNT(*) AS group_size
      FROM wp_posts p JOIN wp_postmeta pm ON pm.post_id = p.ID
      WHERE p.post_type = 'hdo_contacts' AND p.post_status <> 'trash'
        AND pm.meta_key = '<email key>' AND pm.meta_value <> ''
      GROUP BY LOWER(TRIM(pm.meta_value))) g
GROUP BY group_size ORDER BY group_size;
```
Counts only; the emails themselves are not printed.

## Q4. Invoices: money and paid
```sql
SELECT YEAR(p.post_date) AS yr,
       COUNT(*) AS invoices,
       SUM(fee.meta_value <> '') AS with_fee,
       ROUND(SUM(CAST(fee.meta_value AS DECIMAL(10,2))),0) AS fee_total,
       SUM(paid.meta_value IN ('1','Yes','yes','true')) AS marked_paid
FROM wp_posts p
LEFT JOIN wp_postmeta fee  ON fee.post_id  = p.ID AND fee.meta_key  = 'hdo_invoice_fee'
LEFT JOIN wp_postmeta paid ON paid.post_id = p.ID AND paid.meta_key = 'hdo_invoice_paid'
WHERE p.post_type = 'hdo_invoices' AND p.post_status <> 'trash'
GROUP BY yr ORDER BY yr;
```
The paid flag has mixed shapes (form labels and `'1'`/`'0'`) [doc:survey-hdonline-home-directions.md §9 item 5]; Q2 on `hdo_invoice_paid` shows which, then adjust the `IN (...)` list.

## Q5. Reports: compiled versus letters
```sql
SELECT YEAR(p.post_date) AS yr,
       COUNT(*) AS reports,
       SUM(c.meta_value = '1') AS compiled,
       SUM(CHAR_LENGTH(p.post_content) = 0) AS empty_body
FROM wp_posts p
LEFT JOIN wp_postmeta c ON c.post_id = p.ID AND c.meta_key = '_hdo_report_is_compiled'
WHERE p.post_type = 'hdo_reports' AND p.post_status <> 'trash'
GROUP BY yr ORDER BY yr;
```

## Q6. Relations: shape and completeness
```sql
SELECT pm.meta_key,
       SUM(pm.meta_value LIKE 'a:%') AS serialized_array,
       SUM(pm.meta_value REGEXP '^[0-9]+$') AS plain_id,
       SUM(pm.meta_value = '' OR pm.meta_value = 'a:0:{}') AS empty,
       COUNT(*) AS total
FROM wp_posts p JOIN wp_postmeta pm ON pm.post_id = p.ID
WHERE p.post_type = 'hdo_appointments' AND p.post_status <> 'trash'
  AND pm.meta_key IN ('hdo_appt_client','hdo_appt_property','hdo_appt_report','hdo_appt_invoice','hdo_appt_broker','hdo_appt_attorney','hdo_appt_inspector')
GROUP BY pm.meta_key;
```
Answers how the migration must normalise the links. [doc:survey-hdonline.md §9 item 41]

## Q7. The 2008 gap and the 8888 rows
```sql
SELECT DATE_FORMAT(post_date,'%Y-%m') AS ym, post_type, COUNT(*) AS n
FROM wp_posts
WHERE post_type IN ('hdo_appointments','hdo_invoices','hdo_properties')
  AND post_date BETWEEN '2007-06-01' AND '2009-12-31' AND post_status <> 'trash'
GROUP BY ym, post_type ORDER BY ym, post_type;

SELECT post_type, post_status, COUNT(*) FROM wp_posts
WHERE post_date >= '2100-01-01' GROUP BY post_type, post_status;
```
Shows the month the data stops and resumes.

## Q8. Size of the thing
```sql
SELECT COUNT(*) AS postmeta_rows FROM wp_postmeta;
SELECT post_type, COUNT(*) AS n, ROUND(SUM(CHAR_LENGTH(post_content))/1048576,1) AS content_mb
FROM wp_posts GROUP BY post_type ORDER BY n DESC;
SELECT COUNT(*) AS attachments FROM wp_posts WHERE post_type = 'attachment';
```

## Also worth one look, read-only
The source of the active plugin "CLC HDOnline Data Migrator Utility" 0.1 on the clone (`wp-content/plugins/`, folder name unknown): its mapping code says where the 1983 to 2020 rows came from. Read it; do not run it.
