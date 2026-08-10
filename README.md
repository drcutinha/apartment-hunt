# SF Apartment Hunt

Automated apartment monitoring system for San Francisco. Monitors Craigslist, RentCast, Zillow, Zumper, and Redfin for 4+ bedroom apartments in Mission District and Hayes Valley under $10k/month.

**Live Dashboard**: [senduri919.github.io/apartment-hunt](https://senduri919.github.io/apartment-hunt)

## How it works

A GitHub Actions workflow runs every 12 hours and:
1. Collects listings from 5 data sources
2. Deduplicates across sources (same apartment on Craigslist and Zillow gets merged)
3. Extracts features from descriptions (laundry, parking, pets, building type, transit)
4. Scores each listing 0-100 based on weighted criteria
5. Generates a static dashboard deployed to GitHub Pages
6. Emails roommates when new listings are found

## Scoring

Listings are scored 0-100 with configurable weights:

| Criterion | Weight | Priority |
|-----------|--------|----------|
| Square footage | 20 | High |
| Building type (modern) | 15 | High |
| In-unit laundry | 15 | High |
| Transit proximity | 10 | Medium |
| Parking | 8 | Medium |
| Pet policy | 7 | Medium |
| Outdoor space | 7 | Medium |
| Move-in timing | 8 | Medium |
| Lease flexibility | 5 | Medium |
| Price (lower=better) | 5 | Medium |

Edit `config.yaml` to adjust weights, neighborhoods, price range, and more.

## Setup

### 1. API Keys (optional but recommended)

The system works with zero API keys (Craigslist RSS is free), but adding keys enables more sources:

| Service | Free Tier | Sign Up |
|---------|-----------|---------|
| RentCast | 50 requests/month | [rentcast.io/api](https://rentcast.io/api) |
| RapidAPI (Zillow/Redfin) | Varies by provider | [rapidapi.com](https://rapidapi.com) |
| Apify (Zumper) | 10 actor runs/month | [apify.com](https://apify.com) |
| Resend (email) | 100 emails/day | [resend.com](https://resend.com) |

### 2. Add GitHub Secrets

Go to **Settings > Secrets and variables > Actions** and add:

- `RENTCAST_API_KEY`
- `RAPIDAPI_KEY`
- `APIFY_API_KEY`
- `RESEND_API_KEY`

### 3. Enable GitHub Pages

Go to **Settings > Pages** and set Source to **GitHub Actions**.

### 4. Configure

Edit `config.yaml` to set:
- Roommate email addresses (for notifications)
- Scoring weights
- Enable/disable specific collectors

### 5. Run

The workflow runs automatically every 12 hours. To trigger manually:
- Go to **Actions > Apartment Monitor > Run workflow**

## Local Development

```bash
pip install -r requirements.txt

# Set API keys (optional)
cp .env.example .env
# Edit .env with your keys
source .env

# Run the full pipeline
python main.py run

# Or run individual steps
python main.py collect
python main.py process
python main.py generate
python main.py notify

# View the generated site
open site/index.html
```

## Collaboration

The dashboard supports:
- **Voting**: Thumbs up/down on listings
- **Status tracking**: Mark listings as New, Contacted, Toured, Favorite, or Rejected
- **Notes**: Add notes to listings

Collaboration data is stored in `data/collaboration.json`. Edit it directly on GitHub or through the dashboard interface.

## Project Structure

```
src/
  models.py            - Listing data model
  config.py            - Configuration loader
  feature_extractor.py - Regex-based feature extraction from descriptions
  scorer.py            - Weighted 0-100 scoring algorithm
  processor.py         - Deduplication, merging, orchestration
  notifier.py          - Email notifications via Resend
  site_generator.py    - Static site generation via Jinja2
  collectors/
    craigslist.py      - Craigslist RSS feed
    rentcast.py        - RentCast API
    zillow.py          - Zillow via RapidAPI
    zumper.py          - Zumper via Apify
    redfin.py          - Redfin via RapidAPI
```
