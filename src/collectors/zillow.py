from __future__ import annotations

import logging

import requests

from src.collectors.base import BaseCollector
from src.models import Listing, generate_listing_id

logger = logging.getLogger(__name__)


class ZillowCollector(BaseCollector):

    @property
    def name(self) -> str:
        return "zillow"

    def collect(self) -> list[Listing]:
        if not self.config.rapidapi_key:
            logger.warning("Zillow: no RapidAPI key configured, skipping")
            return []

        if not self.check_budget():
            return []

        search = self.config.search
        url = "https://real-estate-zillow-com.p.rapidapi.com/v1/search/rent"
        params = {
            "location": f"{search.city}, {search.state}",
            "property_types": "apartment",
            "min_price": 1000,
            "max_price": search.max_price,
            "min_beds": search.min_bedrooms,
            "min_baths": search.min_bathrooms,
            "sort": "relevant",
            "page": 1,
        }
        headers = {
            "x-rapidapi-key": self.config.rapidapi_key,
            "x-rapidapi-host": "real-estate-zillow-com.p.rapidapi.com",
            "Content-Type": "application/json",
        }

        try:
            logger.info("Fetching Zillow listings via RapidAPI")
            resp = requests.get(url, params=params, headers=headers, timeout=30)
            self.record_api_call()

            if resp.status_code == 429:
                logger.warning("Zillow: rate limited")
                return []

            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            logger.error(f"Zillow API error: {e}")
            return []

        props = data.get("props", [])
        if not props and isinstance(data, list):
            props = data

        listings = []
        for item in props:
            listing = self._parse_listing(item)
            if listing and self._matches_filters(listing):
                listings.append(listing)

        logger.info(f"Zillow: found {len(listings)} matching listings")
        return listings

    def _parse_listing(self, item: dict) -> Listing | None:
        address = item.get("address", "") or item.get("streetAddress", "")
        price = item.get("price") or item.get("rentZestimate")
        if not price:
            price_str = str(item.get("price", "0"))
            price_str = price_str.replace("$", "").replace(",", "").replace("+", "").split("/")[0]
            try:
                price = int(float(price_str))
            except (ValueError, TypeError):
                return None

        if isinstance(price, str):
            try:
                price = int(float(price.replace("$", "").replace(",", "").split("/")[0]))
            except (ValueError, TypeError):
                return None

        listing = Listing(
            source="zillow",
            source_id=str(item.get("zpid", "")),
            source_url=item.get("detailUrl", "") or f"https://www.zillow.com/homedetails/{item.get('zpid', '')}_zpid/",
            address=address,
            city=item.get("city", "San Francisco"),
            state=item.get("state", "CA"),
            zip_code=str(item.get("zipcode", "")),
            latitude=item.get("latitude"),
            longitude=item.get("longitude"),
            price=int(price),
            bedrooms=int(item.get("bedrooms", 0) or 0),
            bathrooms=float(item.get("bathrooms", 0) or 0),
            sqft=item.get("livingArea") or item.get("area"),
            property_type=item.get("homeType"),
        )

        if item.get("imgSrc"):
            listing.images = [item["imgSrc"]]

        listing.id = generate_listing_id(listing.address or str(listing.source_id), listing.price, listing.bedrooms)
        self._detect_neighborhood(listing)
        return listing

    def _detect_neighborhood(self, listing: Listing):
        addr_lower = listing.address.lower()
        zip_code = listing.zip_code
        if zip_code in {"94110", "94114"} or "mission" in addr_lower:
            listing.neighborhood = "Mission District"
        elif zip_code in {"94102", "94103"} or "hayes" in addr_lower:
            listing.neighborhood = "Hayes Valley"

    def _matches_filters(self, listing: Listing) -> bool:
        search = self.config.search
        if listing.price > search.max_price:
            return False
        if listing.bedrooms < search.min_bedrooms:
            return False
        if listing.bathrooms < search.min_bathrooms:
            return False
        valid_zips = set(search.zip_codes)
        if listing.zip_code and listing.zip_code not in valid_zips and not listing.neighborhood:
            return False
        return True
