# Elemental Identification Methodologies in SpectraMapper Pro

Once peaks have been detected and optionally fitted in a LIBS spectrum, the next crucial step is to identify the elements and ionization states responsible for these emission lines. SpectraMapper Pro facilitates this by comparing the experimental peak wavelengths against established spectral line databases.

## 1. Core Principle: Wavelength Matching

The fundamental principle of elemental identification is matching the observed wavelengths of emission peaks (λ<sub>exp</sub>) from the experimental spectrum to known wavelengths of emission lines (λ<sub>db</sub>) stored in spectral databases (e.g., NIST Atomic Spectra Database).

A match is typically considered if:
|λ<sub>exp</sub> - λ<sub>db</sub>| ≤ Tolerance

Where "Tolerance" is a user-defined value (e.g., ±0.1 nm) that accounts for instrumental calibration inaccuracies, peak fitting uncertainties, and potential shifts.

## 2. Database Sources

SpectraMapper Pro supports using pre-existing spectral line data from user-provided sources:

*   **Local SQLite Database (Primary Method):**
    *   **Format:** Users are expected to provide an SQLite database file (e.g., `nist_asd.db`).
    *   **Schema:** The database schema should ideally follow conventions similar to those used by the NIST Atomic Spectra Database. Essential tables would typically be organized per element/ion stage (e.g., `Fe_I`, `Ca_II`), and columns should include:
        *   `Wavelength` (nm, preferably in vacuum or air consistent with experimental data)
        *   `Element` (e.g., 'Fe', 'Ca')
        *   `Spectrum` (e.g., 'I' for neutral, 'II' for singly ionized)
        *   `Aki` (Transition probability, s<sup>-1</sup>) - Important for intensity considerations and quantitative analysis.
        *   `Ei`, `Ek` (Lower and Upper energy levels, cm<sup>-1</sup> or eV) - Important for Boltzmann plots.
        *   `gi`, `gk` (Statistical weights of lower and upper levels) - Important for Boltzmann plots.
        *   Relative Intensity (if available in the database)
    *   **Querying:** The software queries this database for lines within the specified `λ_exp ± Tolerance` window for selected elements/ions.

*   **Directory of CSV Files (Alternative/Fallback):**
    *   **Format:** Users can provide a directory containing subdirectories for each element, which in turn contain CSV files for each ionization stage (e.g., `nist_data_folder/Fe/Fe_I.csv`).
    *   **CSV Structure:** Each CSV file should have a header row with column names matching NIST conventions (Wavelength, Element, Spectrum, Aki, Ei, Ek, etc.).
    *   **Parsing:** The software parses these CSV files on demand or builds an in-memory index for efficient searching.

**Important Note on Database Origin:** SpectraMapper Pro **does not** include functionality to scrape or download data from the NIST website directly to create these initial databases. Users are responsible for obtaining and formatting this data into one of the supported structures.

## 3. Online NIST ASD Search (Optional Feature)

*   **Functionality:** If the `astroquery` Python package is installed and an internet connection is available, users can select an experimental peak (or a wavelength range) and initiate an online search of the NIST Atomic Spectra Database.
*   **Process:** This feature runs in a background thread to keep the UI responsive. It queries the live NIST database via `astroquery.Nist`.
*   **Results:** Found lines are displayed, and users may have an option to add these lines to a local user-specific cache or database for future offline use. This does not modify the primary `nist_asd.db` directly.
*   **Benefits:** Useful for quick lookups or when local databases might be incomplete.
*   **Limitations:** Requires internet, subject to NIST website availability and query limits.

## 4. Matching Process and Parameters

1.  **Peak List:** Input is the list of detected/fitted experimental peak wavelengths.
2.  **Element Selection:** Users can choose to search for all elements present in the database or select specific elements/ion stages of interest to narrow down the search and reduce ambiguity.
3.  **Wavelength Tolerance:** A critical user-defined parameter.
    *   Too small: May miss valid matches if calibration is slightly off.
    *   Too large: Increases the number of potential (and possibly false) matches, especially in line-rich regions.
4.  **Intensity Consideration (Optional):**
    *   If the database contains relative intensities or transition probabilities (A<sub>ki</sub>), these can be used as a secondary filter. Strong experimental peaks are more likely to correspond to database lines with high relative intensities or A<sub>ki</sub> values.
    *   However, LIBS intensities are also heavily influenced by plasma conditions and element concentrations, so this is not a strict rule.

## 5. Displaying Results

*   A table lists potential matches, typically including:
    *   Experimental Wavelength
    *   Database Wavelength
    *   Δ Wavelength (Difference)
    *   Element
    *   Ionization State (Spectrum)
    *   Transition Probability (A<sub>ki</sub>)
    *   Energy Levels (E<sub>i</sub>, E<sub>k</sub>)
    *   Statistical Weights (g<sub>i</sub>, g<sub>k</sub>)
    *   (Other data from the database)
*   Matched peaks are often highlighted or labeled on the spectrum plot.
*   Users can sort and filter the results table to aid in interpretation.

**Challenges:**
*   **Line Coincidence:** Different elements/ions can have emission lines at very similar wavelengths. Additional information (e.g., presence of other lines from the same element, relative intensities, sample knowledge) is often needed to resolve ambiguities.
*   **Database Completeness and Accuracy:** The quality of identification depends heavily on the quality of the database used.

Elemental identification in SpectraMapper Pro provides a powerful tool for qualitative analysis, forming the basis for further quantitative studies.