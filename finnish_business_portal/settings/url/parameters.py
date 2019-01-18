

REGISTERS = dict(
    tr="Finnish Trade Register (Finnish: KAUPPAREKISTERIN KUULUTUSTIEDOT)",
    bis="Finnish Business Information System (Finnish: YTJ:n tietopankki)"
)

# NOTE: 
#   Open Data require search parameters to be in camelCase
#   This application uses snake_case
#   
#   Transformation from snake_case to camelCase
#   is done elsewhere/later

META = dict(
    register = f"Register to use as source: {', '.join(REGISTERS.keys())}",
    total_results = "bool, whether to show total results or not"
)

SEARCH = dict(
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

