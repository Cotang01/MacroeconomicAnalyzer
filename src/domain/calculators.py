
OPERATIONS = {
    "max": lambda x: max(x) if x else 0,
    "min": lambda x: min(x) if x else 0,
    "average": lambda x: sum(x)/len(x) if x else 0.0
    }

AGGREGATABLE_FIELDS = {
    "gdp", "gdp_growth", "inflation", "unemployment", "population"
    }