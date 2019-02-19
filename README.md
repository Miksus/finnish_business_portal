# Finnish Business Portal

The purpose of this project is to provide convenient access to Finnish Patent and Registration Office's 
(Patentti- ja Rekisterihallitus) open data. The aim is to help in automation of acquiring corporate customers' or suppliers'
addresses, registration information and other public information for various purposes.

The project is built in a way that require very little maintenance (in case the owner of the APIs decide on releasing new APIs, delete or rename old ones, change parameters et cetera, does not break the library). This is achieved by making as few assumptions as possible and acquiring the layout of the APIs directly from the provider in every run of the software. Only changes in the structure of the APIs or the output format may cause need for maintenance. 

If you want to disable the logging, you are free to set the level as desired from the source. The source code should be relatively readable.

## Getting Started

Please download the source to your project and call the package. Please see demo.ipynb for thorough examples and tutorial.

Importing and getting list of APIs:
```python
import finnish_business_portal as busportal
busportal.SearchModel.api_infos
```

<br>Initiating a search portal and getting the list of parameters for the API:
```python
portal = busportal.SearchModel("BisCompany", wait_time=2, loop_results=False, deep=True)
portal.parameter_infos
```
The first argument is the name of the API (pick one from busportal.SearchModel.api_options or busportal.SearchModel.api_infos).
Keyword Arguments are:
- wait_time: seconds to wait before each web query (be nice to the provider)
- loop_results: whether to loop all found entries and causing additional queries.
- deep: whether to visit all of the detailed URI pages and returing more detailed data (and more web queries)

<br>Initiating a search and returning the data as Pandas dataframe:
```python
portal.search(name=["name of first company", "name of second company"], company_registration_from="1800-01-01")
mydata_as_listofdicts = portal.results
samedata_as_dataframe = portal.results.to_frame(False).results
```

Note that inputted lists indicate multiple different searches (but one results data) and strings as 
keyword argument values are just constant for all of them. This allows the library to be used versatily and
easily integrated with reading the parameter lists (for example list of supplier names) from Excel, CSV etc.

The boolean value in the to_frame indicate if the dataframe is turned as flat (no inner list of dicts) or not.

### Prerequisites

```
Python 3
Pandas
Requests
```

## Authors

* **Mikael Koli** - [Miksus](https://github.com/Miksus)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
