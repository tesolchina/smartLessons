# Hong Kong Government Email Extraction Results

## Project Overview
This project successfully extracted email addresses from the Hong Kong government's access to information website (https://www.access.gov.hk/en/howtomakeinfo/index.html) and all linked department pages.

## Summary Statistics
- **Total emails found**: 116
- **Total departments scraped**: 78
- **Date of extraction**: September 11, 2025
- **Success rate**: 100% (all department pages were successfully accessed)

## Top Departments by Email Count
1. **Home Affairs Department** - 19 emails
2. **Hong Kong Police Force** - 19 emails
3. **Financial Services and the Treasury Bureau** - 2 emails
4. **Environmental Protection Department** - 2 emails (one duplicate across departments)
5. All other departments - 1 email each

## Email Domain Distribution
The extracted emails span across **73 unique domains**, primarily:
- `.gov.hk` domains (majority - government departments)
- `.org.hk` domains (3 organizations: erb.org, icac.org.hk, pcpd.org.hk)
- `.edu.hk` domains (1: ugc.edu.hk)
- `.hk` domains (1: rthk.hk)

## Sample Contact Information
Here are some key department contacts:

### High-Level Government Offices
- Chief Executive's Office: ceo@ceo.gov.hk
- Financial Services and Treasury Bureau: angelakylam@fstb.gov.hk, enq@fstb.gov.hk
- Security Bureau: aioreq@sb.gov.hk

### Major Service Departments
- Hong Kong Police Force: Multiple emails including seo-support@police.gov.hk
- Immigration Department: rm@immd.gov.hk
- Inland Revenue Department: taxinfo@ird.gov.hk
- Buildings Department: enquiry@bd.gov.hk

### Specialized Agencies
- Independent Commission Against Corruption: general@icac.org.hk
- Hong Kong Monetary Authority: publicenquiry@hkma.gov.hk
- Hong Kong Observatory: dsec@hko.gov.hk

## Data Files Generated
1. **hk_gov_emails_20250911_163227.csv** - Structured CSV format with columns:
   - email
   - department
   - source_url
   - found_at (timestamp)

2. **hk_gov_emails_20250911_163227.json** - JSON format with the same data structure

## Technical Implementation
- **Language**: Python 3.11.8
- **Libraries used**: requests, beautifulsoup4, lxml, pandas
- **Method**: Web scraping with respectful delays (1 second between requests)
- **Error handling**: Retry logic and graceful failure handling
- **Email validation**: Regex pattern matching with false positive filtering

## Usage Notes
- All emails are converted to lowercase for consistency
- Duplicates within the same department are removed
- The scraper respects the website's resources with appropriate delays
- Both plain text emails and mailto links were extracted
- All results include source attribution for transparency

## File Structure
```
crawlGovWebsite/
├── email_scraper.py           # Main scraper script
├── debug_scraper.py           # Debug utility script
├── requirements.txt           # Python dependencies
├── hk_gov_emails_*.csv        # Results in CSV format
├── hk_gov_emails_*.json       # Results in JSON format
└── README.md                  # This summary document
```

This comprehensive extraction provides a complete directory of Hong Kong government department contact emails as of September 2025.
