# Peak Detection and Fitting Methodologies in SpectraMapper Pro

After preprocessing, the next step in analyzing LIBS spectra is often to identify and characterize the emission peaks. This involves detecting the locations of peaks and then fitting them with a mathematical profile (like Voigt) to extract parameters such as precise peak center, height, width, and area.

## 1. Peak Detection

Peak detection algorithms aim to find the wavelength positions and approximate intensities of emission lines.

*   **Derivative-Based Methods:**
    *   **Principle:** Emission peaks correspond to local maxima.
        *   **First Derivative:** Peaks are located where the first derivative of the spectrum crosses zero (from positive to negative).
        *   **Second Derivative:** Peaks correspond to minima in the second derivative of the spectrum.
    *   Smoothing (e.g., via Savitzky-Golay filter which can also compute derivatives) is often applied before or during derivative calculation to reduce noise sensitivity.
    *   **Parameters:** Smoothing window/order, threshold for peak height/prominence to filter out noise peaks.
    *   **Pros:** Conceptually simple, can be effective.
    *   **Cons:** Sensitive to noise if not properly smoothed; thresholding is critical.

*   **SciPy `find_peaks` Wrapper:**
    *   **Principle:** SpectraMapper Pro utilizes the robust `scipy.signal.find_peaks` function from the SciPy library. This function identifies local maxima based on several user-configurable criteria.
    *   **Key Parameters:**
        *   `height`: Minimum peak height.
        *   `threshold`: Minimum vertical distance between a peak and its direct neighbors.
        *   `distance`: Minimum horizontal distance (in data points) between neighboring peaks.
        *   `prominence`: The vertical distance between a peak and its lowest contour line on either side, before encountering a higher peak. Helps distinguish significant peaks from minor fluctuations.
        *   `width`: Minimum peak width at a certain fraction of its height.
    *   **Pros:** Flexible and powerful due to multiple criteria, widely used.
    *   **Cons:** Parameter tuning might be required for optimal performance on diverse datasets.

**Output of Peak Detection:**
Typically a list of peaks, with each entry containing the detected wavelength (peak center) and its intensity (peak height at the center). This list serves as input for peak fitting and elemental identification.

## 2. Peak Fitting (Voigt Profile)

While peak detection gives an approximate location and height, fitting a theoretical profile to the detected peaks provides more accurate parameters, especially for resolving overlapping peaks and characterizing line shapes. The Voigt profile is commonly used for LIBS peaks as it is a convolution of Gaussian and Lorentzian profiles, representing various broadening mechanisms.

*   **Voigt Profile Function:**
    *   The Voigt profile `V(x; A, x₀, σ_G, σ_L)` is defined by:
        *   `A`: Amplitude or height of the peak.
        *   `x₀`: Center wavelength of the peak.
        *   `σ_G` (or FWHM<sub>G</sub>): Standard deviation (or Full Width at Half Maximum) of the Gaussian component, related to Doppler and instrumental broadening.
        *   `σ_L` (or FWHM<sub>L</sub>): Half-width at half-maximum (or FWHM) of the Lorentzian component, related to pressure (Stark) and natural broadening.
    *   SpectraMapper Pro uses `scipy.special.voigt_profile` (which uses `sigma` for Gaussian width and `gamma` for Lorentzian half-width) or a similar numerical approximation.

*   **Fitting Process (Non-linear Least Squares):**
    1.  **Selection:** User selects one or more detected peaks for fitting.
    2.  **Region of Interest (ROI):** For each peak, a small wavelength region around the detected center is considered for fitting.
    3.  **Initial Guesses:** Automatic estimation of initial parameters for the Voigt function is crucial for convergence:
        *   `A`: Detected peak height.
        *   `x₀`: Detected peak wavelength.
        *   `σ_G`, `σ_L`: Estimated from the detected peak width, possibly with an initial assumption about the G/L ratio or by analyzing the shape near the peak.
    4.  **Bounds:** (Optional, user-configurable) Constraints can be set for each parameter (e.g., width must be positive, center must be within a small range of detected).
    5.  **Optimization:** `scipy.optimize.curve_fit` is used to find the Voigt parameters that minimize the sum of squared differences between the observed spectral data in the ROI and the Voigt profile.
    6.  **Goodness-of-Fit:** An R-squared (R²) value or Chi-squared (χ²) value is typically calculated to assess how well the fitted profile matches the data.

*   **Output of Peak Fitting:**
    For each fitted peak, the table is updated with:
    *   Fitted Peak Center (more accurate wavelength)
    *   Fitted Amplitude/Height
    *   Fitted Gaussian Width (σ<sub>G</sub> or FWHM<sub>G</sub>)
    *   Fitted Lorentzian Width (σ<sub>L</sub> or FWHM<sub>L</sub>)
    *   Calculated Voigt FWHM
    *   Peak Area (calculated by integrating the fitted Voigt profile)
    *   R² (Goodness-of-fit)

**Considerations:**
*   **Overlapping Peaks:** For severely overlapping peaks, more sophisticated deconvolution techniques might be needed, possibly involving fitting multiple Voigt profiles simultaneously to a wider region. The current implementation focuses on fitting individual or moderately overlapping peaks.
*   **Computational Cost:** Fitting many peaks, especially with tight convergence criteria, can be computationally intensive.

By combining robust peak detection with accurate Voigt profile fitting, SpectraMapper Pro aims to provide reliable characterization of spectral lines, which is fundamental for subsequent elemental identification and quantitative analysis.