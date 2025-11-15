#===================================================
# 📦 PROJECT METADATA
#---------------------------------------------------
# Clay-style CRM seed generator
# Generates:
#   - crm/people.csv
#   - crm/companies.csv
#   - crm/sectors.csv
#   - crm/people_work_history.csv
#   - crm/relationships.csv
#===================================================

import csv
import os
import uuid
import random 

# load config
N_SECTORS = 10
N_COMPANIES = 25
N_PEOPLE = 200

BASE_YEAR_MIN = 2010
BASE_YEAR_MAX = 2025

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRM_DIR = os.path.join(ROOT_DIR,"crm") 

os.makedirs(CRM_DIR, exist_ok=True) 

# Helper Functions

def uid(prefix: str) -> str:
    #generate a long-ish uid with a prefix.
    return f"{prefix}_{uuid.uuid4().hex[:12]}"

def random_name():
    first_names = [
        "Sarah", "Dylan", "Keiko", "Miguel", "Jasper", "Amara", "Liam",
        "Kiana", "Noah", "Leah", "Victor", "Aya", "Ethan", "Bianca",
        "Lucas", "Mara", "Jonas", "Yuri", "Nina", "Caleb"
    ]
    last_names = [
        "Chen", "Reyes", "Tanaka", "Garcia", "Park", "Malik",
        "Santos", "Nguyen", "Patel", "Kwon", "Lopez", "Khan",
        "Ishikawa", "Rivera", "Bautista", "Morales", "Hernandez"
    ]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def random_company_name():
    prefixes = [
        "Northbeam", "Warp", "Citrus", "Signal", "Atlas", "Nova",
        "Harbor", "Summit", "Orbit", "Beacon", "Copper", "Velox"
    ]
    suffixes = ["Capital", "Ventures", "Labs", "Analytics", "Partners", "Systems", "Studios"]
    return f"{random.choice(prefixes)} {random.choice(suffixes)}"

def random_location():
    cities = [
        "Austin, TX", "New York, NY", "San Francisco, CA", "Seattle, WA",
        "Boston, MA", "London, UK", "Berlin, DE", "Singapore", "Sydney, AU",
        "Toronto, CA"
    ]
    return random.choice(cities)

def random_sector_names():
    base = [
        "FinTech", "AI & ML", "HealthTech", "SaaS B2B",
        "Climate & Energy", "E-commerce", "Developer Tools",
        "Cybersecurity", "Data Infrastructure", "Consumer Apps"
    ]
    return base[:N_SECTORS]

def random_title(level: str) -> str:
    mapping = {
        "junior": ["Analyst", "Associate", "Research Analyst"],
        "mid": ["Manager", "Senior Associate", "Product Manager"],
        "senior": ["Director", "Principal", "Lead Engineer"],
        "exec": ["Partner", "VP", "Co-Founder", "Founder", "CTO", "CEO"]       
    }
    return random.choice(mapping[level])

def random_size_bucket():
    return random.choice(["1–10", "11–50", "51–200", "201–500"])

def random_year_span(n_roles: int):
    #generate approximate years for a sequence of roles.
    start_year = random.randint(BASE_YEAR_MIN, BASE_YEAR_MAX - (n_roles *2))
    years = []
    current = start_year
    for i in range(n_roles):
        end = current + random.randint(1,3)
        years.append((current,end))
        current = end
    return years


def write_csv(path, fieldnames, rows):
    with open(path,"w",newline="",encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def run_generate_crm_csvs():
    #generate sectors
    sectors = []
    for name in random_sector_names():
        sectors.append({
            "sector_uid": uid("s"),
            "name": name
        })

    #generate companies
    companies = []
    for i in range(N_COMPANIES):
        sector = random.choice(sectors)
        company_uid = uid("c")
        name = random_company_name()
        domain = name.lower().replace(" ", "") + ".com" 
        companies.append({
            "company_uid": company_uid,
            "name": name,
            "website": f"https://{domain}",
            "sector_uid": sector["sector_uid"],
            "hq_location": random_location(),
            "size_bucket": random_size_bucket(),
            "tags": "vc" if "Capital" in name or "Ventures" in name or "Partners" in name else "startup"
        })   

    # generate people and work history

    people = []
    work_history = []

    for _ in range(N_PEOPLE):
        person_uid = uid("p")
        name = random_name()
        primary_sector = random.choice(sectors)
        n_roles = random.randint(2,4)
        role_spans = random_year_span(n_roles)

        #choose caree trajectory
        levels_seq_options = [
        ["junior", "mid"],
        ["junior", "mid", "senior"],
        ["junior", "mid", "senior", "exec"],
        ["mid", "senior"],
        ["mid", "senior", "exec"]
        ]
        levels_seq = random.choice(levels_seq_options)
        while len(levels_seq) < n_roles:
            levels_seq.append(levels_seq[-1])
        levels_seq = levels_seq[:n_roles]

        chosen_companies = random.sample(companies, k=min(n_roles, len(companies)))

        current_company_uid = chosen_companies[-1]["company_uid"]
        current_title = random_title(levels_seq[-1])

        people.append({
            "person_uid": person_uid,
            "name": name,
            "current_company_uid": current_company_uid,
            "current_title": current_title,
            "primary_sector_uid": primary_sector['sector_uid'],
            "linkedin_url": "",
            "email": "",
            "tags": "investor" if "Partner" in current_title or "Capital" in chosen_companies[-1]["name"] else ""
        })

        for idx, (years, company, level) in enumerate(zip(role_spans, chosen_companies, levels_seq)):
            start_year, end_year = years
            is_last = idx == n_roles - 1
            work_uid = uid("w")
            title = random_title(level)
            if is_last:
                end_date = ""
                is_current = "TRUE"
            else:
                end_date = f"{end_year}-12-31"
                is_current = "FALSE"

            work_history.append({
                "work_uid": work_uid,
                "person_uid": person_uid,
                "company_uid": company["company_uid"],
                "title": title,
                "start_date": f"{start_year}-01-01",
                "end_date": end_date,
                "is_current": is_current
            })

    #special relationships

    relationships = []
    
    #co-founder style links: randomly pick some companies and mark 2-3 current people as cofounders
    for company in random.sample(companies, k=min(8, len(companies))):
        #pick some people who worked there at some point
        people_at_company = [
            wh['person_uid']
            for wh in work_history
            if wh['company_uid'] == company['company_uid']
        ]
        people_at_company = list(set(people_at_company))
        if len(people_at_company) <2:
            continue
        cofounder_group = random.sample(people_at_company, k=min(3, len(people_at_company)))
        #fully connect them
        for i in range(len(cofounder_group)):
            for j in range(i +1, len(cofounder_group)):
                relationships.append({
                    "relationship_uid": uid("r"),
                    "source_uid": cofounder_group[i],
                    "target_uid": cofounder_group[j],
                    "relationship_type": "cofounder_with",
                    "details": company['name']
                })
    
    #advisor / invested_in: treat "Capital/Ventures/Partners" companies as investors
    investor_companies = [c for c in companies if any(x in c['name'] for x in ["Capital", "Ventures", "Partners"])]
    portfolio_companies = [c for c in companies if c not in investor_companies]

    for inv in investor_companies:
        for port in random.sample(portfolio_companies, k=min(3, len(portfolio_companies))):
            relationships.append({
                "relationship_uid": uid("r"),
                "source_uid": inv['company_uid'],
                "target_uid": port['company_uid'],
                "relationship_type": "invested_in",
                "details": random.choice(["Seed","Series A", "Pre-Seed"])
            })

    #write csvs
    write_csv(
    os.path.join(CRM_DIR, "sectors.csv"), ["sector_uid", "name"], sectors
    )
    
    write_csv(
    os.path.join(CRM_DIR, "companies.csv"),
    ["company_uid", "name", "website", "sector_uid", "hq_location", "size_bucket", "tags"],
    companies
    )

    write_csv(
        os.path.join(CRM_DIR, "people.csv"),
        ["person_uid", "name", "current_company_uid", "current_title", "primary_sector_uid", "linkedin_url", "email", "tags"],
        people
    )

    write_csv(
        os.path.join(CRM_DIR, "people_work_history.csv"),
        ["work_uid", "person_uid", "company_uid", "title", "start_date", "end_date", "is_current"],
        work_history
    )

    write_csv(
        os.path.join(CRM_DIR, "relationships.csv"),
        ["relationship_uid", "source_uid", "target_uid", "relationship_type", "details"],
        relationships
    )

if __name__ == '__main__':
    run_generate_crm_csvs()