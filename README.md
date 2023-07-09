# USARA NPS Rankings

Python scripts that import race results and generate overall rankings.

# Full Setup / Usage

0. Install Python v3.11 (or newer)
1. Download and unzip [usara-nps-rankings-main.zip](usara-nps-rankings-main.zip)
  - Or if you have git installed, `git clone https://github.com/linville/usara-nps-rankings.git`
2. Open a terminal or cmd prompt and change into the `usara-nps-rankings-main` directory.
  - Verify Python works by running `python3 --version`
3. Create a new Python virtual environment
  - `python3 -m venv .venv`
4. Activate your Python virtual environment
  - macOS/Linux: `source .venv/bin/activate`
  - Windows: `.venv\Scripts\activate.bat`
5. Install Python dependencies (currently just OpenPYXL)
  - `pip install -r requirements.txt`
6. Create a directory `source_data` and put all the race result `.xlsx` files in there.
7. Run `python3 generate_rankings.py source_data`
8. This will create two files:
  - `ranking_output_web/individual_ranking_data.js`
  - `ranking_output_web/team_ranking_data.js`

Open the `ranking_output_web/team_rankings.html` (and `individual_rankings.html`) and see if things look right.


# Normal Usage

If you have already been through the full setup, to regenerate rankings, you only need to re-activate your existing Python virtual environment and run the `generate_rankings.py` command.

1. Open a terminal or cmd prompt and change into the `usara-nps-rankings-main` directory.
2. Double check Python works: `python3 --version`
3. Activate your Python virtual environment
  - macOS/Linux: `source .venv/bin/activate`
  - Windows: `.venv\Scripts\activate.bat`
4. Put all the results into the `source_data` directory
5. Run `python3 generate_rankings.py source_data`

# Uploading Results

1. Login to your Squarespace account and click on the USARA website from the Dashboard.
2. Click on Rankings -> Current Rankings
3. Double-click on any text to bring up the editor.
4. With any text highlighted, click on the Link button like you were going to turn that text into a link (you won't, but this is how we get to the place to upload files).
5. Click on the **gear** icon, to the right of the example.com URL.
6. Click on **File** in the left-hand side-bar.
7. **Delete** the existing `team_ranking_data.js` and `individual_ranking_data.js` files.
8. Scroll down to and select the **Upload File**.
9. Upload the the new team and individual ranking files.
10. Hit the **Save** button, then close out the link editor.
11. Check the USARA website and ensure the results still work.


# Documentation

Quick reference to various docs used in the development of this.

- [DataTables](https://datatables.net)
  - [Child rows (show extra / detailed information)](https://datatables.net/examples/api/row_details.html)
  - [Custom Combobox Filtering](https://www.clintmcmahon.com/add-a-custom-search-filter-to-datatables-header/)
