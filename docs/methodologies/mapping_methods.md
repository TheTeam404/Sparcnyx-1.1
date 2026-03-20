# 2D Elemental Mapping Methodologies in SpectraMapper Pro

2D Elemental Mapping in LIBS is a powerful technique used to visualize the spatial distribution of elements on the surface of a sample. It involves acquiring LIBS spectra from a grid of points across the sample and then processing this data to create images (maps) where pixel intensity represents the concentration or signal strength of a specific element at that location.

## 1. Data Acquisition (External to Software)

SpectraMapper Pro does not control the LIBS hardware or data acquisition process. It assumes the user has already performed the mapping experiment:

*   **Setup:** A sample is placed on an XY translation stage.
*   **Scanning:** The laser is focused on the sample surface, and the stage moves the sample in a predefined grid pattern (e.g., raster scan).
*   **Spectral Acquisition:** At each (X,Y) coordinate point in the grid, one or more LIBS spectra are acquired and saved.
*   **File Naming/Organization:** It is crucial that the acquired spectral files can be associated with their (X,Y) coordinates. Common methods include:
    *   **Coordinate-in-Filename:** Each spectral file is named to include its coordinates (e.g., `sample_x01_y02.txt`, `map_pos_X0.5_Y1.2.csv`).
    *   **Ordered List & Dimensions:** Spectra are saved in a sequential order corresponding to the scan pattern, and the user provides the map dimensions (e.g., 20 points in X, 30 points in Y).
    *   **Single Aggregate File:** All spectra and their corresponding (X,Y) coordinates are stored in a single larger file (e.g., a CSV with columns for X, Y, Wavelength1, Wavelength2,... or X, Y, Wavelength, Intensity if in long format).

## 2. Mapping Workflow in SpectraMapper Pro

### Step 1: Data Import for Mapping

*   The user initiates the mapping data import.
*   **Input:**
    *   Select a folder containing individual spectral files (with parsable coordinates in filenames).
    *   Or, specify a single aggregate data file.
    *   If coordinates are not directly available, the user inputs the map dimensions (number of X points, number of Y points) and confirms the scan order (e.g., row-by-row, serpentine).
*   **Processing:** The software loads all spectra and attempts to construct a data structure linking each spectrum to its (X,Y) position.

### Step 2: Batch Preprocessing

*   Consistency is key for mapping. The same preprocessing pipeline (defined in Module 2: Spectral Preprocessing) is applied uniformly to *all* spectra in the mapping dataset.
*   This may include baseline correction, normalization, smoothing, etc.
*   This is a batch operation and can be time-consuming for large maps.

### Step 3: Element/Line Selection for Mapping

*   The user selects one or more elements they wish to map.
*   For each selected element, one or more characteristic emission lines are chosen. These lines should ideally be:
    *   Intense and sensitive to concentration changes.
    *   Free from significant spectral interferences from other elements in the sample matrix.
    *   Identified from a representative spectrum from the map (e.g., using Module 4: Elemental ID) or known from prior analysis.

### Step 4: Intensity Quantification Method

The user defines how the "intensity" of the selected line(s) will be extracted from each spectrum in the map dataset:

*   **Peak Height:** The raw intensity value at the exact center wavelength of the selected line.
    *   **Pros:** Simple, fast.
    *   **Cons:** Sensitive to small shifts in peak position, noise at a single point.
*   **Peak Area (Integration):** The integrated intensity over a small wavelength window around the selected line's center.
    *   **Parameters:** Integration window width.
    *   **Pros:** More robust to noise and slight peak shifts than single point height.
    *   **Cons:** Requires careful window selection to avoid including interfering peaks.
*   **Fitted Peak Amplitude/Area (Voigt Fitting):**
    *   **Principle:** For each spectrum in the map, the selected line is fitted with a Voigt profile (as in Module 3). The fitted amplitude or the area under the fitted Voigt curve is used as the intensity metric.
    *   **Pros:** Most accurate, can deconvolve minor overlaps, less sensitive to peak shape variations.
    *   **Cons:** Computationally intensive, especially for large maps with many points and multiple lines.

### Step 5: Map Generation

*   The software iterates through each (X,Y) point in the dataset.
*   For each point:
    1.  Retrieves the preprocessed spectrum.
    2.  Extracts the intensity of the selected line(s) using the chosen quantification method.
*   A 2D array (matrix) is constructed where each cell `(i,j)` corresponds to an `(X,Y)` position, and its value is the extracted intensity.
*   If multiple lines/elements are being mapped, multiple such 2D arrays are generated.

### Step 6: Map Visualization

*   The generated 2D intensity array(s) are displayed as images:
    *   **False-Color Images / Heatmaps:** Pixel color intensity directly represents the elemental signal intensity (e.g., using `matplotlib.pyplot.imshow` or `pcolormesh`).
    *   **Color Scales:** Users can choose from various colormaps (e.g., viridis, jet, grayscale) and adjust the min/max intensity limits for the color scale to highlight features.
    *   **Interpolation:** Optional interpolation (e.g., bilinear, bicubic) can be applied to the map for a smoother visual appearance, especially if the spatial resolution of the scan is coarse.
    *   **Smoothing:** Optional image smoothing filters can be applied to the final map.
    *   **Overlaying Maps:** For multi-element analysis, maps of different elements can be overlaid, for instance, by assigning them to different color channels (e.g., Red for Element A, Green for Element B, Blue for Element C) or using transparency.
    *   **Axes and Scale Bars:** Maps are displayed with X and Y axes (units in mm, µm, or step number) and optionally a color scale bar legend.

### Step 7: Interactive Map Features

*   **Pixel Value Display:** Hovering the mouse over a map pixel shows its (X,Y) coordinates and the corresponding elemental intensity value.
*   **Spectrum Browsing:** Clicking on a map pixel retrieves and displays the full LIBS spectrum acquired from that specific (X,Y) point, allowing for detailed inspection.

### Step 8: Map Export

*   **Map Data:** The raw 2D intensity arrays can be exported in formats like CSV or NumPy array (`.npy`) for further analysis in other software.
*   **Map Images:** The visualized maps can be saved as standard image files (PNG, JPG, TIFF).

Elemental mapping provides invaluable insights into sample heterogeneity, elemental correlations, and material phase distributions.