# SpectraMapper Pro (Team404 LIBS Analysis Software) - Version 0.1.0-alpha

SpectraMapper Pro is a desktop software application designed for advanced analysis of Laser-Induced Breakdown Spectroscopy (LIBS) data. It aims to provide scientists, researchers, and technicians with a comprehensive suite of tools for importing, processing, analyzing, and visualizing LIBS spectra and generating elemental maps.

## Core Philosophy

*   **Modularity:** Clear separation of UI, core logic, and data management.
*   **User-Centric:** Intuitive workflow, visual feedback, and contextual help.
*   **Accuracy & Robustness:** Careful algorithm implementation with error handling.
*   **Performance:** Optimized processing, with threading for long operations.
*   **Extensibility:** Designed for future additions of new modules or techniques.
*   **Data Integrity & Reproducibility:** Reliable data handling and saving of configurations.

## Key Features (Planned/In Development)

*   **Project Management:** Create, load, and save LIBS analysis projects.
*   **Data Import:** Support for various text-based spectral formats (.txt, .csv, .asc) with configurable parsing.
*   **Spectral Preprocessing:**
    *   Cosmic Ray/Spike Removal (Median filter, Hampel)
    *   Baseline Correction (Polynomial, ALS, Wavelet, Rubberband, SNIP)
    *   Smoothing/Noise Reduction (Savitzky-Golay, Moving Average, Median, Gaussian)
    *   Normalization (Max Intensity, Area, SNV, MSC)
    *   Live preview of preprocessing effects.
*   **Peak Analysis & Fitting:**
    *   Peak Detection (Derivative-based, SciPy `find_peaks`)
    *   Voigt Profile Fitting for detected peaks.
    *   Table display of peak parameters (detected and fitted).
*   **Elemental Identification:**
    *   Matching peaks against user-provided spectral line databases (SQLite or CSV collections).
    *   **No NIST database scraping included.** User must provide their own database files.
    *   (Optional) Online NIST ASD search via `astroquery` if installed.
    *   Display of potential elemental matches with relevant atomic data.
*   **Quantitative Analysis & Plasma Diagnostics:**
    *   Boltzmann Plot for plasma temperature (T<sub>e</sub>) estimation.
    *   (Future) Saha-Boltzmann plots, Calibration Curves.
*   **2D Elemental Mapping:**
    *   Import spectral datasets for mapping (folder of files or aggregate file).
    *   User-defined map dimensions and coordinate assignment.
    *   Batch preprocessing of map data.
    *   Line intensity quantification (peak height, area, fit parameters).
    *   Visualization of 2D elemental maps (heatmaps/false-color).
    *   Interactive map: click to view spectrum at a point.
    *   Export map data and images.
*   **Advanced Chemometrics (Scikit-learn based):**
    *   Automated preprocessing pipeline for chemometric input.
    *   Principal Component Analysis (PCA) with scores and loadings plots.
    *   Framework for Partial Least Squares Regression (PLS-R).
    *   Framework for Classification models (PLS-DA, SVM, k-NN).
*   **Graphical User Interface (GUI):**
    *   Modern, intuitive interface built with PyQt5/PySide6.
    *   Tab-based organization of functionalities.
    *   Interactive and exportable plots (Matplotlib).
    *   Progress indicators for long operations.

## Target User

Scientists, researchers, and technicians working with LIBS data for material analysis, elemental composition, process control, and general research.

## Setup and Installation

**Prerequisites:**

*   Python (3.9 or newer recommended)
*   `pip` (Python package installer)

**Installation Steps:**

1.  **Clone the repository (or download the source code):**
    ```bash
    git clone https://github.com/your_org/Team404_LIBS_Analysis.git
    cd Team404_LIBS_Analysis
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Prepare Spectral Line Databases (User Responsibility):**
    *   **SQLite:** If you have a NIST ASD (or similar) database in SQLite format (e.g., `nist_asd.db`), place it in a known location. You will configure the path to this database within the software (File > Preferences > Paths).
    *   **CSV Files:** Alternatively, you can organize NIST (or similar) data into a directory structure of CSV files (e.g., `nist_data_folder/Fe/Fe_I.csv`). You will configure the path to the parent directory (`nist_data_folder`) in the software preferences.
    *   **The software does NOT include any database scraping tools or pre-packaged databases.**

## Running the Application

Once dependencies are installed and your virtual environment is active:

```bash
python team404/main.py