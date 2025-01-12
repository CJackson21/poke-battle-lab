"""
As the filename suggests, this is meant to populate
the Pokemon database. Which is on a 24 hour scheduler 
to rerun, in case any chnages are made to the api. Will
probably end up making this a weekly or bi-weekly check.
"""
from utils.fetch_pokemon import fetch_pokemon

def main():
    fetch_pokemon()

if __name__ == "__main__":
    main()
