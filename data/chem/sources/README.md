# EU Candidate List source file

ECHA blocks automated downloads, so the EU list is added by hand, usually twice a year (ECHA updates the Candidate List around January and June).

1. Open https://echa.europa.eu/candidate-list-table in your browser.
2. Use the page's export button to download the full table as Excel.
3. Rename the file `echa-candidate-list.xlsx` and upload it to this folder on GitHub (Add file > Upload files), replacing the old one, on a new branch.
4. Open a pull request. The Chemical lists workflow rebuilds `data/chem/svhc-eu.json` and commits it to your branch. Merge when the check passes.

The UK list is downloaded from HSE automatically on the 1st of each month.
