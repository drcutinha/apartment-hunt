from __future__ import annotations

import re

from src.models import Listing

LAUNDRY_IN_UNIT = [
    re.compile(r'\bin[\s-]?unit\s+(washer|laundry|w/d|w&d)', re.I),
    re.compile(r'\bwasher\s*(?:/|and|&)\s*dryer\s+in[\s-]?unit', re.I),
    re.compile(r'\bprivate\s+laundry', re.I),
    re.compile(r'\bw/d\s+in[\s-]?unit', re.I),
    re.compile(r'\bin[\s-]?unit\s+w/d', re.I),
    re.compile(r'\bwasher\s*(?:/|and|&)\s*dryer\s+(?:included|inside)', re.I),
    re.compile(r'\bin-unit\s+washer', re.I),
]

LAUNDRY_SHARED = [
    re.compile(r'\bshared\s+laundry', re.I),
    re.compile(r'\blaundry\s+(?:room|facility|on[\s-]?site|in\s+(?:building|basement|garage))', re.I),
    re.compile(r'\bcoin[\s-]?op\s+laundry', re.I),
]

MODERN_PATTERNS = [
    re.compile(r'\b(?:new(?:ly)?\s+(?:built|construction|renovated|remodel(?:ed)?))', re.I),
    re.compile(r'\bmodern\b', re.I),
    re.compile(r'\bcontemporary\b', re.I),
    re.compile(r'\bgut[\s-]?renovat', re.I),
    re.compile(r'\b(?:updated|upgraded)\s+(?:kitchen|bath|appliance)', re.I),
    re.compile(r'\bstainless\s+steel\s+appliance', re.I),
    re.compile(r'\bquartz\s+counter', re.I),
    re.compile(r'\bhardwood\s+floors?\b.*\b(?:modern|new)', re.I),
    re.compile(r'\bnew\s+(?:kitchen|bathroom|appliance)', re.I),
]

VICTORIAN_PATTERNS = [
    re.compile(r'\bvictorian\b', re.I),
    re.compile(r'\bedwardian\b', re.I),
    re.compile(r'\bpre[\s-]?war\b', re.I),
    re.compile(r'\bhistoric\b', re.I),
    re.compile(r'\bclassic\s+(?:sf|san\s+francisco)\b', re.I),
]

RENOVATED_PATTERNS = [
    re.compile(r'\brenovated\b', re.I),
    re.compile(r'\bremodel(?:ed)?\b', re.I),
    re.compile(r'\brefurbished\b', re.I),
    re.compile(r'\bupdated\b', re.I),
    re.compile(r'\brestored\b', re.I),
]

PARKING_GARAGE = [
    re.compile(r'\bgarage\s*parking', re.I),
    re.compile(r'\bparking\s*garage', re.I),
    re.compile(r'\b(?:1|2|one|two)\s*(?:car\s+)?garage', re.I),
    re.compile(r'\bindoor\s+parking', re.I),
    re.compile(r'\bdeeded\s+parking', re.I),
]

PARKING_LOT = [
    re.compile(r'\bparking\s+(?:lot|spot|space|included)', re.I),
    re.compile(r'\b(?:1|2|one|two)\s+parking\s+(?:spot|space)', re.I),
    re.compile(r'\boff[\s-]?street\s+parking', re.I),
    re.compile(r'\bdriveway', re.I),
]

PARKING_STREET = [
    re.compile(r'\bstreet\s+parking', re.I),
    re.compile(r'\bpermit\s+parking', re.I),
]

NO_PARKING = [
    re.compile(r'\bno\s+parking', re.I),
]

PET_FRIENDLY = [
    re.compile(r'\bpets?\s+(?:ok|okay|welcome|allowed|friendly)', re.I),
    re.compile(r'\bdog(?:s)?\s+(?:ok|okay|welcome|allowed)', re.I),
    re.compile(r'\bcat(?:s)?\s+(?:ok|okay|welcome|allowed)', re.I),
    re.compile(r'\bpet[\s-]?friendly', re.I),
]

PET_CATS_ONLY = [
    re.compile(r'\bcats?\s+only', re.I),
    re.compile(r'\bno\s+dogs?\b.*\bcats?\s+(?:ok|allowed)', re.I),
    re.compile(r'\bsmall\s+pets?\s+(?:ok|only)', re.I),
]

NO_PETS = [
    re.compile(r'\bno\s+pets?\b', re.I),
    re.compile(r'\bpets?\s+not\s+allowed', re.I),
]

OUTDOOR_PATTERNS = [
    re.compile(r'\b(?:private\s+)?(?:back)?yard\b', re.I),
    re.compile(r'\bpatio\b', re.I),
    re.compile(r'\bbalcony\b', re.I),
    re.compile(r'\bdeck\b', re.I),
    re.compile(r'\broof(?:top)?\s*(?:deck|terrace|access|patio)', re.I),
    re.compile(r'\bgarden\b', re.I),
    re.compile(r'\boutdoor\s+space', re.I),
]

TRANSIT_PATTERNS = [
    re.compile(r'(\d+(?:\.\d+)?)\s*(?:mi(?:le)?s?|blocks?)\s*(?:to|from)\s*(bart|muni|caltrain|16th\s*(?:st)?(?:\s*mission)?|24th\s*(?:st)?(?:\s*mission)?|civic\s*center|powell|montgomery)', re.I),
    re.compile(r'(?:near|close\s+to|steps?\s+(?:to|from)|walk\s+to)\s*(bart|muni|caltrain|16th\s*(?:st)?|24th\s*(?:st)?)', re.I),
    re.compile(r'\b(bart|muni)\s+(?:station|stop|line)\s*(?:nearby|close)', re.I),
]

LEASE_MTM = [
    re.compile(r'\bmonth[\s-]?to[\s-]?month\b', re.I),
    re.compile(r'\bflexible\s+lease\b', re.I),
    re.compile(r'\bno\s+(?:long[\s-]?term\s+)?lease\s+required\b', re.I),
    re.compile(r'\bshort[\s-]?term\b', re.I),
]

LEASE_12MO = [
    re.compile(r'\b(?:1|one)\s*(?:[-]?\s*year|yr)\s+lease\b', re.I),
    re.compile(r'\b12\s*(?:[-]?\s*month|mo)\s+lease\b', re.I),
]

LEASE_24MO = [
    re.compile(r'\b(?:2|two)\s*(?:[-]?\s*year|yr)\s+lease\b', re.I),
    re.compile(r'\b24\s*(?:[-]?\s*month|mo)\s+lease\b', re.I),
]


def _match_any(text: str, patterns: list[re.Pattern]) -> bool:
    return any(p.search(text) for p in patterns)


def extract_features(listing: Listing):
    text = f"{listing.description} {listing.address}"

    if listing.has_in_unit_laundry is None:
        if _match_any(text, LAUNDRY_IN_UNIT):
            listing.has_in_unit_laundry = True
        elif _match_any(text, LAUNDRY_SHARED):
            listing.has_in_unit_laundry = False

    if listing.building_type is None:
        if _match_any(text, MODERN_PATTERNS):
            listing.building_type = "modern"
        elif _match_any(text, RENOVATED_PATTERNS):
            listing.building_type = "renovated"
        elif _match_any(text, VICTORIAN_PATTERNS):
            listing.building_type = "victorian"

    if listing.has_parking is None:
        if _match_any(text, NO_PARKING):
            listing.has_parking = False
            listing.parking_type = "none"
        elif _match_any(text, PARKING_GARAGE):
            listing.has_parking = True
            listing.parking_type = "garage"
        elif _match_any(text, PARKING_LOT):
            listing.has_parking = True
            listing.parking_type = "lot"
        elif _match_any(text, PARKING_STREET):
            listing.has_parking = True
            listing.parking_type = "street"

    if listing.is_pet_friendly is None:
        if _match_any(text, NO_PETS):
            listing.is_pet_friendly = False
        elif _match_any(text, PET_CATS_ONLY):
            listing.is_pet_friendly = True
            listing.pet_details = "cats only"
        elif _match_any(text, PET_FRIENDLY):
            listing.is_pet_friendly = True

    if listing.has_outdoor_space is None:
        if _match_any(text, OUTDOOR_PATTERNS):
            listing.has_outdoor_space = True
            for p in OUTDOOR_PATTERNS:
                m = p.search(text)
                if m:
                    listing.outdoor_details = m.group(0).strip()
                    break

    if listing.nearest_transit is None:
        for p in TRANSIT_PATTERNS:
            m = p.search(text)
            if m:
                listing.nearest_transit = m.group(0).strip()
                break

    if listing.lease_term is None:
        if _match_any(text, LEASE_MTM):
            listing.lease_term = "month-to-month"
        elif _match_any(text, LEASE_24MO):
            listing.lease_term = "24 months"
        elif _match_any(text, LEASE_12MO):
            listing.lease_term = "12 months"
