# SpectraMapper Pro - User Guide

Welcome to SpectraMapper Pro, your comprehensive solution for Laser-Induced Breakdown Spectroscopy (LIBS) data analysis. This guide will help you understand the features and workflow of the software.

## Table of Contents

1.  [Introduction](#introduction)
2.  [System Requirements](#system-requirements)
3.  [Installation](#installation)
4.  [Getting Started](#getting-started)
    *   [Launching the Application](#launching-the-application)
    *   [Main Interface Overview](#main-interface-overview)
5.  [Module 1: Project & Data Management](#module-1-project--data-management)
    *   [Creating a New Project](#creating-a-new-project)
    *   [Loading an Existing Project](#loading-an-existing-project)
    *   [Importing Spectral Data](#importing-spectral-data)
    *   [Managing Spectra](#managing-spectra)
6.  [Module 2: Spectral Preprocessing](#module-2-spectral-preprocessing)
    *   [Overview of Preprocessing Steps](#overview-of-preprocessing-steps)
    *   [Applying Preprocessing Steps](#applying-preprocessing-steps)
    *   [Available Methods and Parameters](#available-methods-and-parameters)
        *   [Cosmic Ray/Spike Removal](#cosmic-rayspike-removal)
        *   [Baseline Correction](#baseline-correction)
        *   [Smoothing/Noise Reduction](#smoothingnoise-reduction)
        *   [Normalization](#normalization)
7.  [Module 3: Peak Analysis & Fitting](#module-3-peak-analysis--fitting)
    *   [Peak Detection](#peak-detection)
    *   [Voigt Profile Fitting](#voigt-profile-fitting)
8.  [Module 4: Elemental Identification](#module-4-elemental-identification)
    *   [Using Local NIST Databases](#using-local-nist-databases)
    *   [Using CSV Spectral Line Data](#using-csv-spectral-line-data)
    *   [Online NIST ASD Search (Optional)](#online-nist-asd-search-optional)
    *   [Matching Parameters and Results](#matching-parameters-and-results)
9.  [Module 5: Quantitative Analysis & Plasma Diagnostics](#module-5-quantitative-analysis--plasma-diagnostics)
    *   [Boltzmann Plot for Plasma Temperature](#boltzmann-plot-for-plasma-temperature)
    *   [Calibration Curves (Future)](#calibration-curves-future)
10. [Module 6: 2D Elemental Mapping](#module-6-2d-elemental-mapping)
    *   [Importing Mapping Data](#importing-mapping-data)
    *   [Preprocessing for Maps](#preprocessing-for-maps)
    *   [Selecting Lines for Mapping](#selecting-lines-for-mapping)
    *   [Generating and Visualizing Maps](#generating-and-visualizing-maps)
    *   [Interactive Map Features](#interactive-map-features)
    *   [Exporting Maps](#exporting-maps)
11. [Module 7: Advanced Chemometrics](#module-7-advanced-chemometrics)
    *   [Principal Component Analysis (PCA)](#principal-component-analysis-pca)
    *   [Partial Least Squares Regression (PLS-R) Framework](#partial-least-squares-regression-pls-r-framework)
    *   [Classification Models Framework](#classification-models-framework)
12. [Preferences and Settings](#preferences-and-settings)
13. [Saving and Exporting Results](#saving-and-exporting-results)
14. [Troubleshooting](#troubleshooting)
15. [Contact & Support](#contact--support)

---

## 1. Introduction

SpectraMapper Pro is designed for scientists, researchers, and technicians working with LIBS data. It offers a comprehensive suite of tools for data import, preprocessing, peak analysis, elemental identification, quantitative analysis, 2D elemental mapping, and advanced chemometrics.

## 2. System Requirements

*   **Operating System:** Windows 10/11, macOS (latest versions recommended), Linux (most distributions).
*   **Python:** Version 3.9 or newer.
*   **RAM:** Minimum 4GB, 8GB or more recommended for large datasets and mapping.
*   **Disk Space:** Minimum 500MB for installation, plus space for data and projects.
*   **Dependencies:** See `requirements.txt` (installed automatically if using pip).

## 3. Installation

1.  **Prerequisites:** Ensure you have Python 3.9+ and pip installed.
2.  **Download:** Obtain the SpectraMapper Pro software package (or clone the repository if contributing).
3.  **Install Dependencies:**
    ```bash
    cd path/to/Team404_LIBS_Analysis
    pip install -r requirements.txt
    ```
4.  **Run the Application:**
    ```bash
    cd path/to/Team404_LIBS_Analysis/team404
    python main.py
    ```

## 4. Getting Started

### Launching the Application

Navigate to the `team404` directory and run `python main.py` from your terminal.

### Main Interface Overview

The main window of SpectraMapper Pro is organized into several tabs, each corresponding to a major functional module:

*   **Project & Data:** Manage projects and import/view spectral data.
*   **Preprocessing:** Apply various preprocessing steps to your spectra.
*   **Peak Analysis:** Detect and fit peaks in your spectra.
*   **Elemental ID:** Identify elements using spectral line databases.
*   **Quantitative:** Perform quantitative analysis like Boltzmann plots.
*   **2D Mapping:** Create and visualize elemental distribution maps.
*   **Chemometrics:** Apply multivariate analysis techniques.

Common elements include:
*   **Menu Bar:** Access to File, Edit, View, Tools, Help.
*   **Toolbar:** Quick access to common actions.
*   **Status Bar:** Displays information about current operations and progress.

## 5. Module 1: Project & Data Management

This module is your starting point for any analysis.

### Creating a New Project
*   Go to `File > New Project`.
*   Specify a project name and location.
*   A project file (e.g., `.libs_proj`) will be created to store all your settings, data references, and results.

### Loading an Existing Project
*   Go to `File > Open Project`.
*   Browse and select your project file.

### Importing Spectral Data
*   Click the "Import Spectra" button or go to `File > Import > Spectra`.
*   **Supported Formats:** `.txt`, `.csv`, `.asc`, `.spc` (and other user-configurable delimited text files).
*   **Multi-file Import:** Select multiple files at once.
*   **File Format Configuration:** If the automatic parsing fails, a dialog will appear allowing you to specify:
    *   Delimiter (comma, tab, space, etc.)
    *   Number of header rows to skip
    *   Comment character
    *   Wavelength and Intensity column indices/names.
*   Imported spectra will appear in the "Loaded Spectra" list.

### Managing Spectra
*   **Selection:** Select one or more spectra from the list to view or process.
*   **Preview:** A plot of the selected raw spectrum (or the currently processed version) will be displayed.
*   **Metadata:** View basic metadata if available from filenames or headers.
*   **Remove Spectra:** Remove selected spectra from the current project (does not delete original files).

## 6. Module 2: Spectral Preprocessing

Improve the quality of your spectra before further analysis.

### Overview of Preprocessing Steps
Preprocessing is applied sequentially. You can add, remove, reorder, and parameterize steps. A live preview shows the effect of the currently selected step and all preceding steps.

### Applying Preprocessing Steps
1.  Select one or more spectra from the "Loaded Spectra" list in the "Project & Data" tab. The selected spectra will be available in the Preprocessing tab.
2.  In the "Preprocessing" tab, choose a spectrum to work with from the dropdown list (if multiple are loaded for individual processing) or note that batch mode applies to all selected spectra for mapping.
3.  **Add Step:** Click "Add Step" and choose a preprocessing method from the list.
4.  **Parameterize:** Adjust the parameters for the selected step in the panel provided. The plot will update in real-time.
5.  **Reorder Steps:** Drag and drop steps in the list to change their order of application.
6.  **Remove Step:** Select a step and click "Remove Step".
7.  **Apply to All Selected / Batch:** Once satisfied, apply the defined pipeline to all selected spectra.

### Available Methods and Parameters

#### Cosmic Ray/Spike Removal
*   **Median Filter Based:**
    *   *Parameters:* Window Size, Threshold Factor.
*   **Derivative-Based:**
    *   *Parameters:* Window Size, Threshold Factor.
*   **Hampel Filter:**
    *   *Parameters:* Window Size, Standard Deviation Threshold.

#### Baseline Correction
*   **Polynomial Fitting:**
    *   *Parameters:* Polynomial Order, Fitting Regions (interactive selection on plot).
*   **Iteratively Reweighted Least Squares (IRLS) / Asymmetric Least Squares (ALS):**
    *   *Parameters:* Lambda (smoothness), p (asymmetry).
*   **Wavelet Transform Based:**
    *   *Parameters:* Wavelet Family (e.g., 'db4'), Decomposition Level, Thresholding Method.
*   **Rubberband / Convex Hull:**
    *   *Parameters:* (Often parameter-less or minimal).
*   **SNIP (Sensitive Nonlinear Iterative Peak-clipping):**
    *   *Parameters:* Window Size, Number of Iterations.

#### Smoothing/Noise Reduction
*   **Savitzky-Golay Filter:**
    *   *Parameters:* Window Length (odd integer), Polynomial Order.
*   **Moving Average:**
    *   *Parameters:* Window Length.
*   **Median Filter:**
    *   *Parameters:* Window Length.
*   **Gaussian Filter:**
    *   *Parameters:* Sigma (standard deviation of Gaussian kernel).

#### Normalization
*   **To Max Intensity:** Scales spectrum so its maximum intensity is 1.
*   **To Total Area/Sum:** Scales spectrum so the sum of its intensities (or area under curve) is 1.
*   **To Specific Peak/Wavelength (Internal Standard):**
    *   *Parameters:* Wavelength of reference peak/region.
*   **Standard Normal Variate (SNV):** Centers data to mean zero and scales to unit variance.
*   **Multiplicative Scatter Correction (MSC):**
    *   *Parameters:* Reference Spectrum (option to use mean of current batch).

## 7. Module 3: Peak Analysis & Fitting

Identify and characterize emission lines.

### Peak Detection
1.  Ensure your spectrum is preprocessed.
2.  Go to the "Peak Analysis" tab.
3.  Select a peak detection method:
    *   **Derivative-Based:** Adjust parameters like window size, derivative order, threshold.
    *   **SciPy `find_peaks`:** Adjust parameters like Minimum Height, Prominence, Distance, Width.
4.  Detected peaks will be listed in a table (Wavelength, Intensity) and marked on the spectrum plot.

### Voigt Profile Fitting
1.  **Select Peaks:** Select one or more detected peaks from the table or by clicking on the plot.
2.  Click "Fit Selected Peaks".
3.  **Voigt Fitting:** The software will attempt to fit a Voigt profile to each selected peak.
    *   **Function:** `scipy.special.voigt_profile` or a numerical approximation.
    *   **Parameters Fitted:** Peak Center, Amplitude, Gaussian Width (σ<sub>G</sub>), Lorentzian Width (σ<sub>L</sub>).
    *   **Initial Guesses:** Automatically estimated from detected peak properties.
    *   **Bounds:** (Advanced) Users may be able to set bounds for fit parameters.
4.  **Results:** The peak table will be updated with fitted parameters (Center, Amplitude, σ<sub>G</sub>, σ<sub>L</sub>, Voigt FWHM, R² goodness-of-fit).
5.  **Visualization:** The fitted profile will be overlaid on the spectral data for the selected peak.

## 8. Module 4: Elemental Identification

Match detected peaks to known elemental emission lines.

### Using Local NIST Databases
1.  **Database Setup:**
    *   Ensure you have a pre-existing SQLite database (e.g., `nist_asd.db`) with spectral line data. The schema should ideally follow NIST ASD conventions.
    *   In `Preferences` or the `Elemental ID` tab, specify the path to your SQLite database.
2.  **Matching Process:**
    *   After peak detection/fitting, go to the `Elemental ID` tab.
    *   **Select Elements/Ions:** Choose the elements and ionization states you are interested in (e.g., Fe I, Ca II).
    *   **Set Wavelength Tolerance:** Define a matching window (e.g., ±0.1 nm).
    *   Click "Identify Elements".
3.  **Results:** Potential matches will be displayed in a table: Experimental Wavelength, Database Wavelength, Element, Ion State, Transition Probability (Aki), Energies (Ei, Ek), etc. Matched peaks will be highlighted on the spectrum.

### Using CSV Spectral Line Data
1.  **Data Setup:**
    *   Organize your spectral line data into CSV files, typically one file per element/ion stage (e.g., `Fe_I.csv`). CSVs should have NIST-like headers.
    *   In `Preferences` or the `Elemental ID` tab, specify the directory containing these CSV folders.
2.  The matching process is similar to using the SQLite database.

### Online NIST ASD Search (Optional)
*   If `astroquery` is installed and an internet connection is available.
*   Select a peak or specify a wavelength range.
*   Click "Search NIST Online". Results will be fetched and displayed.
*   Option to add found lines to a user-specific local cache/database.

### Matching Parameters and Results
*   **Wavelength Tolerance:** Crucial for accurate matching.
*   **Relative Intensity Threshold:** (Optional) Consider only database lines above a certain relative intensity if available in the database.
*   **Results Table:** Sortable and filterable.

## 9. Module 5: Quantitative Analysis & Plasma Diagnostics

Extract quantitative information from your spectra.

### Boltzmann Plot for Plasma Temperature (T<sub>e</sub>)
1.  Go to the "Quantitative" tab.
2.  **Line Selection:**
    *   Identify multiple emission lines of the *same element and ionization state* (e.g., several Fe I lines).
    *   These lines must have known transition probabilities (A<sub>ki</sub>), upper energy levels (E<sub>k</sub> or E<sub>i</sub> depending on convention used), and statistical weights (g<sub>k</sub> or g<sub>i</sub>). This data should come from your elemental identification step.
    *   Select these lines from a table populated with identified lines having the necessary atomic data.
3.  **Calculation:** The software will calculate ln(Iλ / A<sub>ki</sub>g<sub>k</sub>) and E<sub>k</sub> for each selected line (where I is the measured line intensity).
4.  **Plotting:** A plot of ln(Iλ / A<sub>ki</sub>g<sub>k</sub>) vs. E<sub>k</sub> will be generated.
5.  **Linear Fit:** A linear regression is performed on these points.
    *   The plasma temperature T<sub>e</sub> is derived from the slope of the fit (-1 / k<sub>B</sub>T<sub>e</sub>, where k<sub>B</sub> is Boltzmann's constant).
6.  **Results:** The calculated T<sub>e</sub> and the R² value of the fit will be displayed.

### Calibration Curves (Future)
This feature may be implemented in future versions to allow for concentration determination based on standard samples.

## 10. Module 6: 2D Elemental Mapping

Visualize the spatial distribution of elements on a sample surface.

### Importing Mapping Data
1.  Go to the "2D Mapping" tab.
2.  Click "Import Map Data".
3.  **Data Format:**
    *   **Folder of Spectra:** Select a folder containing individual spectral files. Filenames must encode X,Y coordinates (e.g., `map_x01_y01.txt`, `map_x01_y02.txt`). The software will attempt to parse these.
    *   **Single File:** (Advanced) A single file containing all spectra and their X,Y coordinates.
    *   You may need to specify map dimensions (number of X points, number of Y points) if coordinates are not directly in filenames or if spectra are in a flat list by acquisition order.
4.  A progress bar will indicate loading and initial processing.

### Preprocessing for Maps
*   Apply a consistent preprocessing pipeline (defined as in Module 2) to *all* spectra in the mapping dataset. This is done in batch mode.

### Selecting Lines for Mapping
1.  **Choose Elements/Lines:**
    *   Select one or more elements of interest.
    *   For each element, select one or more characteristic emission lines (e.g., identified via Module 4 on a representative spectrum, or manually entered wavelength).
2.  **Quantification Method:** Choose how line intensity will be quantified for each point in the map:
    *   **Peak Height:** Intensity at the exact line center.
    *   **Peak Area:** Integrated intensity over a small window around the line (define window width).
    *   **Fitted Peak Amplitude/Area:** (Most accurate, computationally intensive) Perform Voigt fitting for the selected line on each spectrum.

### Generating and Visualizing Maps
1.  Click "Generate Map(s)". A progress bar will show the status.
2.  The software iterates through each (X,Y) spectrum, extracts the chosen line intensity, and builds a 2D data array.
3.  **Visualization:**
    *   Maps are displayed as false-color images or heatmaps.
    *   **Color Scales:** Choose from various colormaps (e.g., viridis, jet, grayscale). Adjust min/max intensity limits for the color scale.
    *   **Interpolation:** Apply interpolation (e.g., bilinear, bicubic) for smoother maps.
    *   **Overlay:** (If mapping multiple elements/lines) Option to overlay maps, perhaps using different color channels or transparency.
    *   **Axes:** X,Y axes displayed with appropriate units or step numbers.

### Interactive Map Features
*   **Hover:** Mouse over a pixel on the map to see its (X,Y) coordinates and the corresponding intensity value.
*   **Click:** Click on a map pixel to display the full LIBS spectrum acquired from that specific point. This spectrum can then be analyzed further in other modules.

### Exporting Maps
*   **Map Data:** Save the raw 2D intensity array(s) as CSV or NumPy (`.npy`) files.
*   **Map Image:** Save the visualized map as an image (PNG, JPG, TIFF).

## 11. Module 7: Advanced Chemometrics

Explore multivariate relationships within your spectral datasets. Requires a batch of spectra (e.g., from multiple samples or mapping data).

**Preprocessing for Chemometrics:** Spectra are typically interpolated to a common wavelength axis, baseline-corrected, and normalized (e.g., SNV, MSC) before applying these methods. This is often an automated pipeline within this module.

### Principal Component Analysis (PCA)
1.  Load a batch of preprocessed spectra.
2.  Select PCA from the chemometrics tools.
3.  **Parameters:** Number of principal components to calculate.
4.  **Results:**
    *   **Scores Plots:** 2D (PC1 vs PC2, etc.) or 3D (PC1 vs PC2 vs PC3) plots showing sample groupings. Points can be labeled by sample name/ID.
    *   **Loadings Plots:** Show which wavelengths contribute most to each principal component.
    *   **Explained Variance:** Table or plot showing the percentage of variance explained by each PC.

### Partial Least Squares Regression (PLS-R) Framework
This provides a framework. You'll typically need external concentration data.
1.  Load spectra (X variables) and corresponding known concentrations/property values (Y variable).
2.  Select PLS-R.
3.  **Parameters:** Number of latent variables.
4.  **Results:**
    *   Predicted vs. Actual plot.
    *   Metrics: R², RMSE (Root Mean Square Error), RMSECV (if cross-validation is performed).

### Classification Models Framework
(e.g., PLS-DA, SVM, k-NN)
This provides a framework. You'll need class labels for your spectra.
1.  Load spectra and assign class labels to each.
2.  Select a classification model.
3.  **Parameters:** Model-specific (e.g., number of components for PLS-DA, kernel for SVM).
4.  **Training & Validation:** The model is trained. Cross-validation is recommended.
5.  **Results:**
    *   Confusion Matrix.
    *   Accuracy, Precision, Recall, F1-Score.
    *   ROC curves (for binary classifiers).

## 12. Preferences and Settings
*   Accessible via `Edit > Preferences` or `Tools > Preferences`.
*   **General:** Default project directory, UI theme (if available).
*   **Data Paths:** Default paths for NIST SQLite database, CSV spectral line data directory.
*   **Plotting:** Default line colors, styles.
*   **Analysis Defaults:** Default tolerance for elemental ID, default parameters for certain algorithms.

## 13. Saving and Exporting Results
*   **Projects:** Save your entire analysis session (data references, processing pipelines, results) using `File > Save Project` or `File > Save Project As`.
*   **Spectra:**
    *   Export processed spectra as `.txt` or `.csv`.
*   **Peak Lists:**
    *   Export tables of detected/fitted peaks as `.csv`.
*   **Elemental ID Results:**
    *   Export tables of matched elements as `.csv`.
*   **Quantitative Results:**
    *   Export Boltzmann plot data and T<sub>e</sub> as `.txt` or `.csv`.
*   **Maps:**
    *   Export map data arrays as `.csv` or `.npy`.
    *   Export map images as `.png`, `.jpg`, `.tiff`.
*   **Chemometrics Results:**
    *   Export PCA scores/loadings, PLS model coefficients, classification metrics as `.csv`.
*   **Plots:** Most plots will have an option to "Save Plot As Image" (PNG, SVG, PDF).

## 14. Troubleshooting

*   **Slow Performance:**
    *   Ensure you have sufficient RAM.
    *   Processing large datasets or many maps can be time-consuming. Look for progress bars.
    *   Reduce the number of points in maps or the complexity of preprocessing for quicker previews.
*   **Incorrect File Parsing:**
    *   Use the "Configure File Format" dialog during import to specify correct delimiters, headers, and column indices.
*   **Elemental ID No Matches:**
    *   Check wavelength calibration of your spectrometer.
    *   Increase wavelength tolerance (but be cautious of false positives).
    *   Ensure your database/CSV files contain the expected elements for your sample.
    *   Verify path to database is correct in Preferences.
*   **Errors during Analysis:**
    *   Note any error messages displayed.
    *   Check the application log (View > Log Console or `logs/app.log`) for more details.

## 15. Contact & Support

*   **Issue Tracker:** (If applicable, e.g., GitHub Issues page for the project)
*   **Developer Contact:** (Your name/email or project email)

---
Thank you for using SpectraMapper Pro!