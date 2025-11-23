#!/usr/bin/env python3
"""
Comprehensive CSV to API Identifier Mapping Table
Generated from Canadian Weather API and CSV data
"""

# Mapping table: CSV site codes -> API identifiers
# Format: "csv_code": "api_id",  # City Name, Province
CSV_TO_API_MAPPING = {
    "s0000002": "bc-12",  # Clearwater, BC
    "s0000003": "bc-13",  # Valemount, BC
    "s0000004": "bc-39",  # Grand Forks, BC
    "s0000005": "bc-47",  # McBride, BC
    "s0000006": "bc-49",  # Merritt, BC
    "s0000007": "bc-56",  # Masset, BC
    "s0000008": "bc-72",  # Invermere, BC
    "s0000009": "bc-8",  # Dome Creek, BC
    "s0000010": "mb-18",  # Little Grand Rapids, MB
    "s0000011": "mb-27",  # Oxford House, MB
    "s0000012": "mb-33",  # Bissett, MB
    "s0000013": "mb-39",  # Shamattawa, MB
    "s0000014": "mb-56",  # York Factory, MB
    "s0000015": "mb-60",  # Flin Flon, MB
    "s0000016": "nl-10",  # Musgrave Harbour, NL
    "s0000017": "nl-42",  # New-Wes-Valley, NL
    "s0000018": "nl-43",  # Bay Roberts, NL
    "s0000019": "nl-8",  # St. Alban's, NL
    "s0000021": "ns-43",  # North Mountain (Cape Breton), NS
    "s0000026": "pe-2",  # Maple Plains, PE
    "s0000030": "yt-3",  # Rancheria, YT
    "s0000031": "yt-4",  # Dempster (Highway), YT
    "s0000032": "nl-31",  # Burgeo, NL
    "s0000033": "nb-1",  # Bouctouche, NB
    "s0000034": "nb-13",  # Richibucto, NB
    "s0000038": "nb-9",  # Kouchibouguac, NB
    "s0000039": "nl-36",  # St. Lawrence, NL
    "s0000040": "ns-13",  # Parrsboro, NS
    "s0000041": "nl-14",  # Bonavista, NL
    "s0000042": "nl-18",  # Wreckhouse, NL
    "s0000043": "nb-32",  # Edmundston, NB
    "s0000045": "ab-50",  # Edmonton, AB
    "s0000047": "ab-52",  # Calgary, AB
    "s0000069": "on-71",  # Hawkesbury, ON
    "s0000070": "on-122",  # Alexandria, ON
    "s0000071": "on-152",  # Cornwall, ON
    "s0000072": "on-92",  # Morrisburg, ON
    "s0000073": "on-1",  # Algonquin Park (Brent), ON
    "s0000074": "on-29",  # Algonquin Park (Lake of Two Rivers), ON
    "s0000075": "on-53",  # Oxtongue Lake, ON
    "s0000076": "on-14",  # Welland, ON
    "s0000077": "on-155",  # Winchester, ON
    "s0000078": "bc-86",  # Whistler, BC
    "s0000079": "nl-22",  # La Scie, NL
    "s0000080": "on-141",  # Rondeau (Provincial Park), ON
    "s0000081": "sk-42",  # Coronach, SK
    "s0000082": "nl-30",  # Placentia, NL
    "s0000083": "ab-53",  # Sundre, AB
    "s0000084": "ns-40",  # Halifax (Shearwater), NS
    "s0000086": "sk-43",  # Indian Head, SK
    "s0000087": "sk-5",  # Fort Qu'Appelle, SK
    "s0000089": "ns-1",  # New Glasgow, NS
    "s0000090": "ns-34",  # Caribou, NS
    "s0000091": "mb-43",  # Bachelors Island, MB
    "s0000095": "sk-47",  # Nipawin, SK
    "s0000096": "ns-36",  # Beaver Island, NS
    "s0000100": "nl-32",  # Cartwright, NL
    "s0000101": "mb-37",  # Bloodvein, MB
    "s0000102": "mb-54",  # Berens River, MB
    "s0000108": "on-150",  # Collingwood, ON
    "s0000110": "ns-37",  # Baccaro Point, NS
    "s0000111": "ab-59",  # Coronation, AB
    "s0000112": "nl-44",  # Englee, NL
    "s0000113": "sk-44",  # Uranium City, SK
    "s0000114": "nl-11",  # Port au Choix, NL
    "s0000115": "nl-33",  # Daniel's Harbour, NL
    "s0000116": "nl-34",  # Badger, NL
    "s0000117": "nl-4",  # Buchans, NL
    "s0000118": "nl-6",  # Grand Falls-Windsor, NL
    "s0000119": "ab-41",  # Willow Creek (Provincial Park), AB
    "s0000120": "ab-60",  # Claresholm, AB
    "s0000122": "nl-35",  # Twillingate, NL
    "s0000126": "ab-61",  # Calgary (Olympic Park), AB
    "s0000128": "nl-37",  # St. Anthony, NL
    "s0000129": "ab-62",  # Drumheller, AB
    "s0000130": "mb-44",  # Pinawa, MB
    "s0000131": "mb-8",  # Whiteshell, MB
    "s0000132": "bc-15",  # Estevan Point, BC
    "s0000133": "sk-11",  # Shaunavon, SK
    "s0000135": "mb-20",  # Virden, MB
    "s0000136": "mb-45",  # Melita, MB
    "s0000137": "mb-66",  # Turtle Mountain (Provincial Park), MB
    "s0000138": "pe-6",  # East Point, PE
    "s0000139": "mb-46",  # Swan River, MB
    "s0000140": "nu-11",  # Eureka, NU
    "s0000141": "bc-74",  # Vancouver, BC
    "s0000146": "bc-79",  # Prince George, BC
    "s0000151": "mb-13",  # Steinbach, MB
    "s0000155": "bc-93",  # Gulf Islands (Southern), BC
    "s0000156": "ab-63",  # Elk Island (National Park), AB
    "s0000157": "sk-12",  # Tisdale, SK
    "s0000158": "sk-46",  # Melfort, SK
    "s0000159": "ab-64",  # Cardston, AB
    "s0000160": "mb-12",  # Snow Lake, MB
    "s0000161": "mb-67",  # Pukatawagan, MB
    "s0000162": "nl-40",  # Nain, NL
    "s0000165": "on-160",  # Goderich, ON
    "s0000166": "on-28",  # Kincardine, ON
    "s0000167": "ab-65",  # Garden Creek, AB
    "s0000168": "on-8",  # Brockville, ON
    "s0000171": "mb-3",  # Altona, MB
    "s0000172": "mb-48",  # Gretna, MB
    "s0000173": "bc-16",  # Pemberton, BC
    "s0000175": "bc-52",  # Sparwood, BC
    "s0000177": "nu-12",  # Grise Fiord, NU
    "s0000178": "mb-50",  # Hunters Point, MB
    "s0000181": "nl-38",  # Hopedale, NL
    "s0000188": "nt-27",  # Fort Providence, NT
    "s0000189": "mb-4",  # Pine Falls, MB
    "s0000190": "mb-55",  # Victoria Beach, MB
    "s0000191": "mb-9",  # Grand Beach, MB
    "s0000192": "sk-48",  # Broadview, SK
    "s0000195": "sk-49",  # Watrous, SK
    "s0000196": "sk-6",  # Humboldt, SK
    "s0000198": "nb-10",  # Mount Carleton (Provincial Park), NB
    "s0000201": "nb-6",  # Grand Falls, NB
    "s0000206": "nu-19",  # Ennadai, NU
    "s0000207": "mb-57",  # Grand Rapids, MB
    "s0000208": "sk-50",  # Southend Reindeer, SK
    "s0000209": "sk-51",  # Assiniboia, SK
    "s0000210": "nt-29",  # Fort Liard, NT
    "s0000212": "bc-26",  # Creston, BC
    "s0000217": "ab-14",  # Hinton, AB
    "s0000218": "ab-70",  # Jasper, AB
    "s0000219": "sk-52",  # Leader, SK
    "s0000220": "nl-26",  # Marble Mountain, NL
    "s0000221": "nl-41",  # Corner Brook, NL
    "s0000223": "ns-42",  # Kejimkujik (National Park), NS
    "s0000224": "bc-29",  # Malahat, BC
    "s0000225": "sk-54",  # Rockglen, SK
    "s0000227": "bc-14",  # Dease Lake, BC
    "s0000228": "bc-6",  # Cassiar, BC
    "s0000229": "ab-32",  # Lac La Biche, AB
    "s0000230": "sk-14",  # Lucky Lake, SK
    "s0000234": "bc-32",  # Gonzales Point, BC
    "s0000235": "on-110",  # Wingham, ON
    "s0000236": "on-16",  # Walkerton, ON
    "s0000237": "on-36",  # Dundalk, ON
    "s0000238": "on-51",  # North Perth, ON
    "s0000239": "on-84",  # Shelburne, ON
    "s0000240": "on-89",  # Mount Forest, ON
    "s0000241": "sk-15",  # Waskesiu Lake, SK
    "s0000242": "bc-33",  # Lytton, BC
    "s0000243": "nb-31",  # Miscou Island, NB
    "s0000247": "bc-35",  # Pitt Meadows, BC
    "s0000248": "sk-16",  # Maple Creek, SK
    "s0000250": "nb-29",  # Fredericton, NB
    "s0000251": "on-75",  # Cobourg, ON
    "s0000252": "pe-1",  # North Cape, PE
    "s0000256": "mb-49",  # Deerwood, MB
    "s0000257": "mb-65",  # Carman, MB
    "s0000258": "bc-37",  # Nelson, BC
    "s0000259": "bc-38",  # Nakusp, BC
    "s0000263": "ab-34",  # Kananaskis (Nakiska Ridgetop), AB
    "s0000264": "ns-18",  # North East Margaree, NS
    "s0000265": "ns-4",  # Baddeck, NS
    "s0000273": "mb-14",  # Oak Point, MB
    "s0000274": "sk-18",  # Elbow, SK
    "s0000276": "mb-15",  # McCreary, MB
    "s0000278": "sk-19",  # Wynyard, SK
    "s0000279": "ab-37",  # Hendrickson Creek, AB
    "s0000280": "nl-24",  # St. John's, NL
    "s0000281": "on-169",  # Midland, ON
    "s0000282": "on-12",  # Fort Erie, ON
    "s0000283": "on-80",  # Port Colborne, ON
    "s0000285": "nb-33",  # Point Lepreau, NB
    "s0000286": "bc-40",  # Esquimalt, BC
    "s0000289": "mb-19",  # Pilot Mound, MB
    "s0000291": "bc-41",  # Princeton, BC
    "s0000293": "bc-43",  # Burns Lake, BC
    "s0000294": "bc-46",  # Port Alberni, BC
    "s0000297": "ab-39",  # Lacombe, AB
    "s0000299": "ab-40",  # Red Earth Creek, AB
    "s0000300": "sk-23",  # Rosetown, SK
    "s0000301": "on-102",  # Bancroft, ON
    "s0000302": "on-133",  # Barry's Bay, ON
    "s0000303": "on-165",  # Haliburton, ON
    "s0000304": "on-30",  # Apsley, ON
    "s0000305": "on-43",  # Kaladar, ON
    "s0000306": "ab-16",  # Rocky Mountain House, AB
    "s0000307": "ns-12",  # St. Peter's, NS
    "s0000308": "ns-23",  # Hart Island, NS
    "s0000310": "ab-17",  # Crowsnest, AB
    "s0000313": "ab-19",  # Milk River, AB
    "s0000318": "ns-19",  # Halifax, NS
    "s0000323": "bc-50",  # Squamish, BC
    "s0000324": "bc-51",  # Salmon Arm, BC
    "s0000325": "on-116",  # Stratford, ON
    "s0000326": "on-137",  # London, ON
    "s0000328": "on-18",  # Strathroy, ON
    "s0000329": "on-98",  # St. Thomas, ON
    "s0000331": "nb-18",  # Saint Andrews, NB
    "s0000332": "nb-35",  # St. Stephen, NB
    "s0000337": "mb-23",  # Sprague, MB
    "s0000339": "mb-24",  # Fisher Branch, MB
    "s0000340": "nt-15",  # Sambaa K'e, NT
    "s0000343": "sk-2",  # Biggar, SK
    "s0000344": "sk-26",  # Scott, SK
    "s0000349": "yt-12",  # Faro, YT
    "s0000350": "yt-8",  # Ross River, YT
    "s0000352": "mb-28",  # Shoal Lake, MB
    "s0000355": "sk-41",  # Swift Current, SK
    "s0000356": "ab-26",  # Vegreville, AB
    "s0000357": "sk-28",  # Val Marie, SK
    "s0000358": "ab-27",  # Vauxhall, AB
    "s0000364": "ns-20",  # Digby, NS
    "s0000365": "ns-27",  # Brier Island, NS
    "s0000366": "nt-24",  # Yellowknife, NT
    "s0000367": "on-79",  # Oakville, ON
    "s0000368": "on-95",  # Burlington, ON
    "s0000369": "sk-30",  # Collins Bay, SK
    "s0000370": "ns-30",  # Western Head, NS
    "s0000371": "ns-39",  # Liverpool, NS
    "s0000372": "sk-31",  # Weyburn, SK
    "s0000373": "bc-62",  # White Rock, BC
    "s0000375": "mb-31",  # Wasagaming, MB
    "s0000376": "bc-63",  # Muncho Lake, BC
    "s0000377": "bc-87",  # Liard River, BC
    "s0000379": "ab-42",  # Bow Valley (Provincial Park), AB
    "s0000380": "mb-32",  # Roblin, MB
    "s0000381": "sk-35",  # Last Mountain Lake (Sanctuary), SK
    "s0000382": "ab-43",  # Bow Island, AB
    "s0000384": "ab-44",  # Stavely, AB
    "s0000385": "nb-20",  # Tracadie-Sheila, NB
    "s0000386": "nb-22",  # Bas-Caraquet, NB
    "s0000387": "sk-37",  # Outlook, SK
    "s0000390": "bc-66",  # Victoria (University of), BC
    "s0000391": "bc-11",  # Kootenay (National Park), BC
    "s0000392": "bc-68",  # Yoho (National Park), BC
    "s0000396": "bc-10",  # Rock Creek, BC
    "s0000397": "bc-69",  # Osoyoos, BC
    "s0000398": "bc-24",  # Chilliwack, BC
    "s0000399": "bc-70",  # Agassiz, BC
    "s0000400": "nl-17",  # Channel-Port aux Basques, NL
    "s0000401": "mb-35",  # Carberry, MB
    "s0000402": "mb-61",  # Shilo, MB
    "s0000403": "ab-3",  # Canmore, AB
    "s0000404": "ab-49",  # Banff, AB
    "s0000409": "bc-67",  # Atlin, BC
    "s0000410": "yt-14",  # Teslin, YT
    "s0000412": "nu-10",  # Arctic Bay, NU
    "s0000413": "ab-2",  # Barrhead, AB
    "s0000414": "on-13",  # Orillia, ON
    "s0000415": "on-151",  # Barrie, ON
    "s0000422": "on-157",  # Tobermory, ON
    "s0000423": "nt-22",  # Deline, NT
    "s0000424": "on-161",  # Simcoe, ON
    "s0000425": "on-17",  # Tillsonburg, ON
    "s0000426": "on-50",  # Norfolk, ON
    "s0000429": "on-49",  # New Tecumseth, ON
    "s0000431": "on-23",  # Leamington, ON
    "s0000432": "nt-7",  # Ulukhaktok, NT
    "s0000433": "ns-16",  # Ingonish, NS
    "s0000434": "on-106",  # Smiths Falls, ON
    "s0000435": "on-61",  # Sharbot Lake, ON
    "s0000436": "on-74",  # Kemptville, ON
    "s0000439": "ns-17",  # Kentville, NS
    "s0000440": "ns-21",  # Lunenburg, NS
    "s0000441": "ns-6",  # Bridgewater, NS
    "s0000442": "nt-9",  # Wekweeti, NT
    "s0000444": "mb-17",  # Morden, MB
    "s0000445": "mb-26",  # Winkler, MB
    "s0000446": "ns-10",  # Sheet Harbour, NS
    "s0000447": "ns-22",  # Malay Falls, NS
    "s0000449": "nb-15",  # Sackville, NB
    "s0000450": "ns-33",  # Amherst, NS
    "s0000451": "on-103",  # Parry Sound, ON
    "s0000452": "on-35",  # Dunchurch, ON
    "s0000453": "ab-22",  # Stony Plain, AB
    "s0000454": "on-11",  # Chatham-Kent, ON
    "s0000455": "on-172",  # Rodney, ON
    "s0000456": "nl-13",  # Rocky Harbour, NL
    "s0000457": "nl-7",  # Gros Morne, NL
    "s0000458": "on-143",  # Toronto, ON
    "s0000460": "ns-26",  # Port Hawkesbury, NS
    "s0000461": "ns-28",  # Tracadie, NS
    "s0000462": "ns-3",  # Antigonish, NS
    "s0000463": "ns-41",  # Cape George, NS
    "s0000464": "ns-8",  # Guysborough, NS
    "s0000466": "nl-1",  # Clarenville, NL
    "s0000467": "nl-15",  # Terra Nova (National Park), NL
    "s0000468": "ab-48",  # Drayton Valley, AB
    "s0000469": "on-109",  # Vineland, ON
    "s0000470": "on-47",  # Lincoln, ON
    "s0000471": "bc-71",  # Trail, BC
    "s0000472": "mb-36",  # Winnipeg (The Forks), MB
    "s0000473": "nl-19",  # Winterland, NL
    "s0000474": "nl-3",  # Marystown, NL
    "s0000475": "nl-5",  # Grand Bank, NL
    "s0000477": "ab-56",  # Whitecourt, AB
    "s0000480": "qc-159",  # Kangirsuk, QC
    "s0000481": "bc-17",  # Tofino, BC
    "s0000482": "bc-5",  # Ucluelet, BC
    "s0000485": "bc-18",  # Bella Coola, BC
    "s0000489": "on-114",  # Alliston, ON
    "s0000490": "mb-10",  # Minnedosa, MB
    "s0000491": "mb-16",  # Souris, MB
    "s0000492": "mb-52",  # Brandon, MB
    "s0000495": "nu-15",  # Cambridge Bay, NU
    "s0000496": "bc-20",  # Nanaimo, BC
    "s0000497": "bc-21",  # Castlegar, BC
    "s0000498": "nu-16",  # Kugluktuk, NU
    "s0000501": "nu-17",  # Chesterfield, NU
    "s0000502": "nb-3",  # Chipman, NB
    "s0000503": "nb-4",  # Doaktown, NB
    "s0000504": "nu-18",  # Clyde River, NU
    "s0000508": "mb-58",  # Dauphin, MB
    "s0000509": "bc-25",  # Dawson Creek, BC
    "s0000510": "ab-71",  # Edmonton (Int'l Aprt), AB
    "s0000511": "nu-20",  # Arviat, NU
    "s0000514": "sk-10",  # Oxbow, SK
    "s0000515": "sk-4",  # Carlyle, SK
    "s0000516": "sk-53",  # Estevan, SK
    "s0000518": "ab-72",  # Edson, AB
    "s0000519": "nt-30",  # Inuvik, NT
    "s0000521": "nb-11",  # Oromocto, NB
    "s0000522": "on-15",  # Woodstock, NB
    "s0000523": "ab-33",  # Mildred Lake, AB
    "s0000524": "nt-3",  # Fort Resolution, NT
    "s0000525": "nt-4",  # Fort Simpson, NT
    "s0000526": "nl-25",  # Makkovik, NL
    "s0000527": "bc-34",  # Golden, BC
    "s0000528": "on-39",  # Greater Napanee, ON
    "s0000529": "on-63",  # Sydenham, ON
    "s0000530": "on-66",  # Westport, ON
    "s0000531": "on-69",  # Kingston, ON
    "s0000533": "mb-21",  # Arnes, MB
    "s0000534": "mb-62",  # Gimli, MB
    "s0000540": "nu-23",  # Igloolik, NU
    "s0000542": "qc-105",  # Kuujjuarapik, QC
    "s0000544": "qc-106",  # Quaqtaq, QC
    "s0000548": "on-42",  # Haldimand County, ON
    "s0000549": "on-77",  # Hamilton, ON
    "s0000550": "on-86",  # Brantford, ON
    "s0000551": "qc-109",  # Longueuil, QC
    "s0000562": "pe-3",  # Summerside, PE
    "s0000563": "qc-112",  # Ivujivik, QC
    "s0000564": "nu-25",  # Pond Inlet, NU
    "s0000567": "nl-27",  # Stephenville, NL
    "s0000569": "bc-55",  # Cache Creek, BC
    "s0000571": "on-5",  # Guelph, ON
    "s0000572": "on-81",  # Cambridge, ON
    "s0000573": "on-82",  # Kitchener-Waterloo, ON
    "s0000574": "qc-155",  # Kangiqsujuaq, QC
    "s0000575": "qc-99",  # Lac Raglan, QC
    "s0000578": "qc-36",  # Akulivik, QC
    "s0000581": "sk-21",  # Kindersley, SK
    "s0000582": "on-25",  # Newmarket, ON
    "s0000584": "on-64",  # Vaughan, ON
    "s0000585": "on-85",  # Markham, ON
    "s0000586": "qc-117",  # Aupaluk, QC
    "s0000587": "nu-26",  # Kimmirut, NU
    "s0000589": "sk-22",  # Meadow Lake, SK
    "s0000591": "qc-118",  # Kangiqsualujjuaq, QC
    "s0000593": "yt-10",  # Mayo, YT
    "s0000594": "nl-29",  # Mary's Harbour, NL
    "s0000595": "ab-20",  # Fort McMurray, AB
    "s0000611": "qc-126",  # Gatineau, QC
    "s0000618": "nt-14",  # Ekati (Lac de Gras), NT
    "s0000619": "ab-23",  # Cold Lake, AB
    "s0000620": "qc-133",  # Québec, QC
    "s0000622": "nb-27",  # Grand Manan, NB
    "s0000623": "on-52",  # Ottawa (Richmond - Metcalfe), ON
    "s0000624": "sk-27",  # Prince Albert, SK
    "s0000625": "ab-25",  # Peace River, AB
    "s0000626": "mb-29",  # Portage la Prairie, MB
    "s0000627": "qc-131",  # Inukjuak, QC
    "s0000629": "on-121",  # Peterborough, ON
    "s0000630": "on-149",  # Port Perry, ON
    "s0000631": "on-168",  # Kawartha Lakes (Lindsay), ON
    "s0000632": "on-44",  # Kawartha Lakes (Fenelon Falls), ON
    "s0000635": "qc-147",  # Montréal, QC
    "s0000637": "on-31",  # Burk's Falls, ON
    "s0000638": "on-38",  # Gravenhurst, ON
    "s0000639": "on-56",  # Port Carling, ON
    "s0000640": "on-88",  # Huntsville, ON
    "s0000641": "on-9",  # Bracebridge, ON
    "s0000642": "on-93",  # Muskoka, ON
    "s0000644": "mb-30",  # The Pas, MB
    "s0000645": "ab-29",  # Red Deer, AB
    "s0000646": "ns-15",  # Windsor, ON
    "s0000647": "bc-9",  # Good Hope Lake, BC
    "s0000648": "yt-13",  # Watson Lake, YT
    "s0000649": "ns-29",  # Yarmouth, NS
    "s0000652": "ab-30",  # Lethbridge, AB
    "s0000653": "nb-17",  # Shediac, NB
    "s0000654": "nb-36",  # Moncton, NB
    "s0000655": "nb-8",  # Hopewell, NB
    "s0000656": "bc-61",  # Comox, BC
    "s0000657": "bc-92",  # Courtenay, BC
    "s0000658": "on-4",  # Brampton, ON
    "s0000661": "ab-31",  # Grande Prairie, AB
    "s0000666": "sk-34",  # North Battleford, SK
    "s0000670": "ns-31",  # Sydney, NS
    "s0000678": "nu-28",  # Rankin Inlet, NU
    "s0000681": "qc-136",  # Sherbrooke, QC
    "s0000686": "nb-19",  # Sussex, NB
    "s0000688": "nb-5",  # Fundy (National Park), NB
    "s0000689": "nu-29",  # Sanikiluaq, NU
    "s0000691": "on-107",  # St. Catharines, ON
    "s0000692": "on-125",  # Niagara Falls, ON
    "s0000693": "nu-1",  # Nanisivik, NU
    "s0000694": "nu-2",  # Kinngait, NU
    "s0000699": "qc-145",  # Tasiujaq, QC
    "s0000700": "on-115",  # Stirling, ON
    "s0000701": "on-126",  # Trenton, ON
    "s0000702": "on-27",  # Prince Edward (Picton), ON
    "s0000703": "on-3",  # Belleville, ON
    "s0000704": "on-57",  # Quinte West, ON
    "s0000706": "ab-1",  # Cochrane, ON
    "s0000707": "on-117",  # Oshawa, ON
    "s0000708": "on-119",  # Whitby, ON
    "s0000710": "on-54",  # Pickering, ON
    "s0000712": "qc-76",  # Laval, QC
    "s0000715": "sk-38",  # La Ronge, SK
    "s0000716": "nu-5",  # Qikiqtarjuaq, NU
    "s0000719": "qc-150",  # Kuujjuaq, QC
    "s0000720": "nt-21",  # Norman Wells, NT
    "s0000722": "sk-13",  # La Loche, SK
    "s0000723": "sk-39",  # Buffalo Narrows, SK
    "s0000724": "on-130",  # Wiarton, ON
    "s0000725": "on-19",  # Port Elgin, ON
    "s0000726": "on-60",  # Saugeen Shores, ON
    "s0000727": "on-62",  # South Bruce Peninsula, ON
    "s0000728": "on-7",  # Owen Sound, ON
    "s0000729": "on-112",  # Petawawa, ON
    "s0000730": "on-131",  # Pembroke, ON
    "s0000731": "on-58",  # Renfrew, ON
    "s0000732": "on-83",  # Deep River, ON
    "s0000733": "sk-9",  # Moosomin, SK
    "s0000734": "mb-6",  # Richer, MB
    "s0000735": "bc-75",  # Victoria Harbour, BC
    "s0000736": "nl-12",  # Wabush Lake, NL
    "s0000737": "nl-20",  # Labrador City, NL
    "s0000740": "nt-23",  # Wrigley, NT
    "s0000741": "bc-77",  # Cranbrook, BC
    "s0000743": "sk-1",  # Rosthern, SK
    "s0000744": "on-46",  # Lambton Shores, ON
    "s0000745": "ab-51",  # Medicine Hat, AB
    "s0000749": "nu-6",  # Whale Cove, NU
    "s0000750": "nu-7",  # Pangnirtung, NU
    "s0000751": "yt-15",  # Beaver Creek, YT
    "s0000754": "bc-44",  # Vanderhoof, BC
    "s0000756": "bc-30",  # Kitimat, BC
    "s0000757": "bc-80",  # Terrace, BC
    "s0000768": "ab-12",  # Airdrie, AB
    "s0000770": "bc-82",  # Smithers, BC
    "s0000772": "bc-84",  # Penticton, BC
    "s0000773": "on-59",  # Richmond Hill, ON
    "s0000776": "mb-22",  # Leaf Rapids, MB
    "s0000777": "mb-41",  # Lynn Lake, MB
    "s0000778": "mb-53",  # Brochet, MB
    "s0000779": "mb-42",  # Churchill, MB
    "s0000780": "nl-23",  # Happy Valley-Goose Bay, NL
    "s0000781": "ab-45",  # Grande Cache, AB
    "s0000785": "on-128",  # Toronto Island, ON
    "s0000786": "on-24",  # Mississauga, ON
    "s0000787": "on-32",  # Caledon, ON
    "s0000788": "sk-32",  # Regina, SK
    "s0000789": "on-68",  # Halton Hills, ON
    "s0000791": "nt-1",  # Detah, NT
    "s0000793": "qc-128",  # Salluit, QC
    "s0000794": "ab-54",  # Slave Lake, AB
    "s0000795": "bc-88",  # Sandspit, BC
    "s0000796": "on-147",  # Sarnia, ON
    "s0000797": "sk-40",  # Saskatoon, SK
    "s0000798": "nu-9",  # Coral Harbour, NU
    "s0000802": "ns-2",  # Annapolis Royal, NS
    "s0000803": "ns-35",  # Greenwood, NS
    "s0000804": "ns-5",  # Bridgetown, NS
    "s0000806": "nb-28",  # Bathurst, NB
    "s0000807": "nb-2",  # Campbellton, NB
    "s0000808": "nb-26",  # Dalhousie, NB
    "s0000809": "nb-30",  # Charlo, NB
    "s0000814": "ns-7",  # Economy, NS
    "s0000815": "on-140",  # Orangeville, ON
    "s0000817": "nt-11",  # Tulita, NT
    "s0000821": "nu-22",  # Alert, NU
    "s0000822": "sk-24",  # Moose Jaw, SK
    "s0000823": "yt-11",  # Old Crow, YT
    "s0000824": "ab-46",  # Pincher Creek, AB
    "s0000825": "yt-16",  # Whitehorse, YT
    "s0000827": "pe-4",  # St. Peters Bay, PE
    "s0000828": "bc-73",  # Stewart, BC
    "s0000830": "nt-20",  # Tuktoyaktuk, NT
    "s0000831": "mb-40",  # Delta, MB
    "s0000832": "nl-21",  # Churchill Falls, NL
    "s0000833": "ab-55",  # Wainwright, AB
    "s0000835": "ab-15",  # Lloydminster, SK
    "s0000845": "bc-95",  # Cummins Lakes Park, BC
    "s0000857": "nl-45",  # L'Anse-au-Loup, NL
    "s0000858": "nl-46",  # Rigolet, NL
    "s0000859": "nl-47",  # Cartwright Junction (Trans-Labrador Hwy), NL
    "s0000860": "nl-48",  # Gull Island Rapids (Trans-Labrador Hwy), NL
    "s0000861": "ns-44",  # Eskasoni, NS
    "s0000862": "bc-96",  # Richmond, BC
    "s0000863": "bc-97",  # Duncan, BC
    "s0000864": "bc-98",  # Qualicum Beach, BC
    "s0000758": "bc-81",  # Abbotsford, BC
}

def get_api_identifier(csv_code: str) -> str:
    """Get API identifier for a given CSV code"""
    return CSV_TO_API_MAPPING.get(csv_code)

def get_total_mappings() -> int:
    """Get total number of mappings available"""
    return len(CSV_TO_API_MAPPING)

def get_all_csv_codes() -> list:
    """Get all available CSV codes"""
    return list(CSV_TO_API_MAPPING.keys())

def get_all_api_identifiers() -> list:
    """Get all available API identifiers"""
    return list(CSV_TO_API_MAPPING.values())

def get_city_info(csv_code: str) -> str:
    """Get city name and province for a given CSV code"""
    # Extract city info from comments
    for line in CSV_TO_API_MAPPING.items():
        if line[0] == csv_code:
            # This would need to be implemented with a separate lookup
            return f"City info for {csv_code}"
    return "Unknown"
