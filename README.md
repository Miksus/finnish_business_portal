# Finnish Business Portal

The purpose of this project is to provide convenient access to Finnish Patent and Registration Office's 
(Patentti- ja Rekisterihallitus) open data. The aim is to help in automation of acquiring corporate customers' or suppliers'
addresses, registration information and other public information for various purposes.

The project is built in a way that require very little maintenance (in case the owner of the APIs decide on releasing new APIs, delete or rename old ones, change parameters et cetera, does not break the library). This is achieved by making as few assumptions as possible and acquiring the layout of the APIs directly from the provider in every run of the software. Only changes in the structure of the APIs or the output format may cause need for maintenance. 

If you want to disable the logging, please freely set the level as desired.

## Getting Started

Please see demo.ipynb for examples and tutorial.

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
