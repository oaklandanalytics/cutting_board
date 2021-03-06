import os
from multiprocessing import Pool
import sys

args = sys.argv[1:]

def initialize_census_for_region():
    os.system('python scripts/fetch_census_data.py')
    os.system('python scripts/block_to_maz_controls.py')


def initialize_county(county):
    print "Processing data for {}".format(county)
    os.system('python scripts/split_by_city.py "%s"' % county)


def run_jurises(juris):
    print "Processing data for {}".format(juris)
    os.system('python scripts/fetch_buildings.py "%s"' % juris)
    os.system('python scripts/self_intersections.py "%s"' % juris)
    os.system('python scripts/split_parcels.py "%s"' % juris)
    os.system('python scripts/join_buildings_to_parcels.py "%s"' % juris)
    os.system('python scripts/assign_building_attributes.py "%s"' % juris)
    os.system('python scripts/match_unit_controls.py "%s"' % juris)

pool = Pool(4)
counties = ["Solano", "Sonoma", "San Francisco", "San Mateo",
            "Santa Clara", "Napa", "Marin", "Contra Costa",
            "Alameda"]

#initialize_census_for_region()
#pool.map(initialize_county, counties)

jurises = []
for county in counties:
    for juris in open('cache/jurislist.%s.txt' % county).readlines():
        if juris[0] == "#":
            continue  # skip if commented
        jurises.append(juris[:-1])
jurises.sort()

# filter jurises we have already processed
jurises = [
    f for f in jurises if
    not os.path.exists("cache/%s_buildings_match_controls.csv" % f)]

jurises = [f for f in jurises if f != "Unincorporated San Francisco"]

if len(args):
    # pass jurises to run as comman line arguments
    jurises = args

print "Running for: %d jurises" % len(jurises), jurises

pool.map(run_jurises, jurises)
