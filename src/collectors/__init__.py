from src.collectors.craigslist import CraigslistCollector
from src.collectors.rentcast import RentCastCollector
from src.collectors.zillow import ZillowCollector
from src.collectors.zumper import ZumperCollector
from src.collectors.redfin import RedfinCollector

COLLECTORS = {
    "craigslist": CraigslistCollector,
    "rentcast": RentCastCollector,
    "zillow": ZillowCollector,
    "zumper": ZumperCollector,
    "redfin": RedfinCollector,
}
