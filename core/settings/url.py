


PARAMS_REGISTERS = dict(
    tr="Finnish Trade Register (Finnish: KAUPPAREKISTERIN KUULUTUSTIEDOT)",
    bis="Finnish Business Information System (Finnish: YTJ:n tietopankki)"
)





URL_BASE = "http://avoindata.prh.fi/{register}/v1?totalResults={total_results}"
PARAMS_SEARCH = dict(
    max_results = "Maximum results to show",
    results_from = "Number of result to start with",
    name = "name of the company of to search",
    business_id = "Business ID (Finnish: Y-tunnus)",
    registered_office = "City where the organization is registered",
    street_address_post_code = "Visiting address",
    company_form = "Form of the company",
    business_line = "Industry name",
    business_line_code = "Industry code",
    company_registration_from = "Registeration date",
)

# NOTE: 
#   Open Data require search parameters to be in camelCase
#   This application uses snake_case
#   
#   Transformation from snake_case to camelCase
#   is done elsewhere/later

URL_BASE_BY_BUSINESSID = "http://avoindata.prh.fi/{register}/v1/{business_id}"