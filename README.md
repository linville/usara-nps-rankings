# USARA NPS Rankings

Python scripts that import race results and generate overall rankings.

# Standalone Usage

0. Setup a Python venv and install OpenPYXL.
   - Directions TBD.
1. Create a directory `source_data` and put all the race result `.xlsx` files in there.
2. Run `python3 generate_rankings.py source_data`
3. This will create a file `ranking_output_web/ranking_data.js`

Open the `ranking_output_web/rankings.html` and see if things look right.

# Documentation

Quick reference to various docs used in the development of this.

- [DataTables](https://datatables.net)
  - [Child rows (show extra / detailed information)](https://datatables.net/examples/api/row_details.html)
  - [Custom Combobox Filtering](https://www.clintmcmahon.com/add-a-custom-search-filter-to-datatables-header/)
