"""
START seed data for the lookup tables:
    address_state
    federal_regulator
    hmda_institution_type
    sbl_institution_type
These are accessed in db_revisions/versions/* scripts and in test/migrations/test_lookup_tables_data_seed .
"""

address_state_seed = [
    {"code": "AL", "name": "Alabama"},
    {"code": "AK", "name": "Alaska"},
    {"code": "AZ", "name": "Arizona"},
    {"code": "AR", "name": "Arkansas"},
    {"code": "CA", "name": "California"},
    {"code": "CO", "name": "Colorado"},
    {"code": "CT", "name": "Connecticut"},
    {"code": "DE", "name": "Delaware"},
    {"code": "FL", "name": "Florida"},
    {"code": "GA", "name": "Georgia"},
    {"code": "HI", "name": "Hawaii"},
    {"code": "ID", "name": "Idaho"},
    {"code": "IL", "name": "Illinois"},
    {"code": "IN", "name": "Indiana"},
    {"code": "IA", "name": "Iowa"},
    {"code": "KS", "name": "Kansas"},
    {"code": "KY", "name": "Kentucky"},
    {"code": "LA", "name": "Louisiana"},
    {"code": "ME", "name": "Maine"},
    {"code": "MD", "name": "Maryland"},
    {"code": "MA", "name": "Massachusetts"},
    {"code": "MI", "name": "Michigan"},
    {"code": "MN", "name": "Minnesota"},
    {"code": "MS", "name": "Mississippi"},
    {"code": "MO", "name": "Missouri"},
    {"code": "MT", "name": "Montana"},
    {"code": "NE", "name": "Nebraska"},
    {"code": "NV", "name": "Nevada"},
    {"code": "NH", "name": "New Hampshire"},
    {"code": "NJ", "name": "New Jersey"},
    {"code": "NM", "name": "New Mexico"},
    {"code": "NY", "name": "New York"},
    {"code": "NC", "name": "North Carolina"},
    {"code": "ND", "name": "North Dakota"},
    {"code": "OH", "name": "Ohio"},
    {"code": "OK", "name": "Oklahoma"},
    {"code": "OR", "name": "Oregon"},
    {"code": "PA", "name": "Pennsylvania"},
    {"code": "RI", "name": "Rhode Island"},
    {"code": "SC", "name": "South Carolina"},
    {"code": "SD", "name": "South Dakota"},
    {"code": "TN", "name": "Tennessee"},
    {"code": "TX", "name": "Texas"},
    {"code": "UT", "name": "Utah"},
    {"code": "VT", "name": "Vermont"},
    {"code": "VA", "name": "Virginia"},
    {"code": "WA", "name": "Washington"},
    {"code": "WV", "name": "West Virginia"},
    {"code": "WI", "name": "Wisconsin"},
    {"code": "WY", "name": "Wyoming"},
    {"code": "DC", "name": "District of Columbia"},
    {"code": "AS", "name": "American Samoa"},
    {"code": "GU", "name": "Guam"},
    {"code": "MP", "name": "Northern Mariana Islands"},
    {"code": "PR", "name": "Puerto Rico"},
    {"code": "UM", "name": "United States Minor Outlying Islands"},
    {"code": "VI", "name": "Virgin Islands, U.S."},
]

federal_regulator_seed = [
    {"id": "FCA", "name": "Farm Credit Administration"},
    {"id": "FDIC", "name": "Federal Deposit Insurance Corporation"},
    {"id": "FHFA", "name": "Federal Housing Finance Agency"},
    {"id": "FRS", "name": "Federal Reserve System"},
    {"id": "NCUA", "name": "National Credit Union Administration"},
    {"id": "OCC", "name": "Office of the Comptroller of the Currency"},
    {"id": "OTS", "name": "Office of Thrift Supervision (only valid until July 21, 2011)"},
]

sbl_institution_type_seed = [
    {"id": "1", "name": "Bank or savings association."},
    {"id": "2", "name": "Minority depository institution."},
    {"id": "3", "name": "Credit union."},
    {"id": "4", "name": "Nondepository institution."},
    {"id": "5", "name": "Community development financial institution (CDFI)."},
    {"id": "6", "name": "Other nonprofit financial institution."},
    {"id": "7", "name": "Farm Credit System institution."},
    {"id": "8", "name": "Government lender."},
    {"id": "9", "name": "Commercial finance company."},
    {"id": "10", "name": "Equipment finance company."},
    {"id": "11", "name": "Industrial loan company."},
    {"id": "12", "name": "Online lender."},
    {"id": "13", "name": "Other"},
]

hmda_institution_type_seed = [
    {"id": "1", "name": "National Bank (OCC supervised)"},
    {"id": "2", "name": "State Member Bank (FRS Supervised)"},
    {"id": "3", "name": "State non-member bank (FDIC supervised)"},
    {"id": "4", "name": "State Chartered Thrift (FDIC supervised)"},
    {"id": "5", "name": "Federal Chartered Thrift (OCC supervised)"},
    {"id": "6", "name": "Credit Union (NCUA supervised)"},
    {"id": "7", "name": "Federal Branch or Agency of Foreign Banking Organization (FBO)"},
    {"id": "8", "name": "Branch or Agency of FBO (FRS supervised)"},
    {"id": "9", "name": "MBS of national Bank (OCC supervised)"},
    {"id": "10", "name": "MBS of state member bank (FRS supervised)"},
    {"id": "11", "name": "MBS of state non-member bank (FDIC supervised)"},
    {"id": "12", "name": "MBS of Bank Holding Company (BHC) (FRS supervised)"},
    {"id": "13", "name": "MBS of credit union (NCUA supervised)"},
    {"id": "14", "name": "independent MBS, no depository affiliation"},
    {"id": "15", "name": "MBS of Savings and Loan Holding Co"},
    {"id": "16", "name": "MBS of state chartered Thrift"},
    {"id": "17", "name": "MBS of federally chartered thrift (OCC supervised)"},
    {"id": "18", "name": "Affiliate of depository institution. MBS is in the same ownership org as a depository."},
]

"""
END seed data for the lookup tables:
"""
