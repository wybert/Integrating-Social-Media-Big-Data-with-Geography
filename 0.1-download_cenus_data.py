import os

state_list = {"01":"ALABAMA",
"02":"ALASKA",
"04":"ARIZONA",
"05":"ARKANSAS",
"06":"CALIFORNIA",
"08":"COLORADO",
"09":"CONNECTICUT",
"10":"DELAWARE",
"11":"DISTRICT OF COLUMBIA",
"12":"FLORIDA",
"13":"GEORGIA",
"15":"HAWAII",
"16":"IDAHO",
"17":"ILLINOIS",
"18":"INDIANA",
"19":"IOWA",
"20":"KANSAS",
"21":"KENTUCKY",
"22":"LOUISIANA",
"23":"MAINE",
"24":"MARYLAND",
"25":"MASSACHUSETTS",
"26":"MICHIGAN",
"27":"MINNESOTA",
"28":"MISSISSIPPI",
"29":"MISSOURI",
"30":"MONTANA",
"31":"NEBRASKA",
"32":"NEVADA",
"33":"NEW HAMPSHIRE",
"34":"NEW JERSEY",
"35":"NEW MEXICO",
"36":"NEW YORK",
"37":"NORTH CAROLINA",
"38":"NORTH DAKOTA",
"39":"OHIO",
"40":"OKLAHOMA",
"41":"OREGON",
"42":"PENNSYLVANIA",
"44":"RHODE ISLAND",
"45":"SOUTH CAROLINA",
"46":"SOUTH DAKOTA",
"47":"TENNESSEE",
"48":"TEXAS",
"49":"UTAH",
"50":"VERMONT",
"51":"VIRGINIA",
"53":"WASHINGTON",
"54":"WEST VIRGINIA",
"55":"WISCONSIN",
"56":"WYOMING"}

base_url = "https://www2.census.gov/geo/tiger/TIGER2021/TABBLOCK20/tl_2021_%s_tabblock20.zip"
outpath = "data/census_data/"
os.makedirs(outpath, exist_ok=True)
from tqdm import tqdm
for state in tqdm(state_list,total=len(state_list)):
    url = base_url % state
    os.system("wget %s -P %s" % (url, outpath))



