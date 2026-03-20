# Preprocessing Methodologies in SpectraMapper Pro

Preprocessing is a critical step in LIBS data analysis to enhance the quality of spectra by removing noise, artifacts, and unwanted variations. This prepares the data for more accurate subsequent analyses like peak detection, elemental identification, and quantitative measurements. SpectraMapper Pro offers a suite of configurable preprocessing steps that can be applied sequentially.

## 1. Cosmic Ray / Spike Removal

Cosmic rays or detector spikes can introduce sharp, narrow, and intense artifacts in spectra that do not correspond to actual elemental emissions. These need to be removed to avoid misinterpretation.

*   **Median Filter Based:**
    *   **Principle:** A median filter is applied over a moving window. If the intensity of a central point deviates significantly (by a threshold factor times the local standard deviation or a similar metric) from the median of its neighbors, it's considered a spike and replaced (e.g., by the median).
    *   **Parameters:** Window Size, Threshold Factor.
    *   **Pros:** Simple and effective for isolated spikes.
    *   **Cons:** May slightly broaden sharp real peaks if the window is too large or threshold too low.

*   **Derivative-Based Spike Detection:**
    *   **Principle:** Spikes often exhibit very high first or second derivatives. The algorithm identifies points where the derivative exceeds a certain threshold and replaces them.
    *   **Parameters:** Window Size (for derivative calculation, e.g., Savitzky-Golay), Threshold.
    *   **Pros:** Can be sensitive to sharp spikes.
    *   **Cons:** Sensitive to general noise if not properly thresholded.

*   **Hampel Filter:**
    *   **Principle:** For each point, the median and Median Absolute Deviation (MAD) are calculated within a window. If the point deviates from the median by more than 'n' times the MAD, it is replaced by the median.
    *   **Parameters:** Window Size, Standard Deviation Threshold (n_sigmas).
    *   **Pros:** Robust to outliers within the window.

## 2. Baseline Correction

The LIBS plasma continuum emission and other background sources create a varying baseline underlying the sharp atomic peaks. Accurate baseline correction is essential for correct peak intensity/area determination.

*   **Polynomial Fitting:**
    *   **Principle:** A low-order polynomial (e.g., 1st to 5th order) is fitted to regions of the spectrum assumed to be baseline (i.e., devoid of peaks). This fitted polynomial is then subtracted from the entire spectrum.
    *   **Parameters:** Polynomial Order, Fitting Regions (user-selected or automatically detected).
    *   **Pros:** Simple, computationally inexpensive.
    *   **Cons:** Can be poor if peak-free regions are hard to define or if the baseline is complex and not well-represented by a simple polynomial. Can distort peak shapes if fitted through peak regions.

*   **Iteratively Reweighted Least Squares (IRLS) / Asymmetric Least Squares (ALS):**
    *   **Principle (ALS):** Fits a smooth curve (baseline) to the spectrum. In each iteration, weights are assigned to data points. Points above the current baseline fit (likely peaks) are given lower weights (or higher penalties if the baseline goes above them for an asymmetric variant), causing the baseline to fit primarily to the lower envelope of the spectrum.
    *   **Parameters:** `lambda` (smoothness parameter - penalizes curvature), `p` (asymmetry parameter - penalizes the baseline going above the signal).
    *   **Pros:** Generally robust and can adapt to complex baselines without requiring manual peak-free region selection.
    *   **Cons:** Parameter tuning (`lambda`, `p`) can be crucial and sometimes iterative.

*   **Wavelet Transform Based Correction:**
    *   **Principle:** A discrete wavelet transform decomposes the spectrum into different frequency components. The baseline typically corresponds to low-frequency (approximation) coefficients, while peaks and noise are in higher-frequency (detail) coefficients. By thresholding or removing approximation coefficients related to the baseline and reconstructing the signal, the baseline can be removed.
    *   **Parameters:** Wavelet Family (e.g., 'db4', 'sym8'), Decomposition Level, Thresholding Method/Value.
    *   **Pros:** Can be very effective for complex and fluctuating baselines.
    *   **Cons:** Requires careful selection of wavelet parameters; can be computationally more intensive.

*   **Rubberband / Convex Hull Based:**
    *   **Principle:** Imagine stretching a "rubberband" or finding the convex hull beneath the spectrum. This forms the baseline.
    *   **Pros:** Intuitive, can be effective for certain types of baselines.
    *   **Cons:** May not be suitable for all baseline shapes, especially those with significant dips not related to peaks.

*   **SNIP (Sensitive Nonlinear Iterative Peak-clipping):**
    *   **Principle:** An iterative algorithm that estimates the baseline by repeatedly applying a clipping filter. It's designed to be less sensitive to peak widths than some other methods.
    *   **Parameters:** Window Size (or range of window sizes), Number of Iterations.
    *   **Pros:** Good for spectra with varying peak widths and densities.

## 3. Smoothing / Noise Reduction

Reduces random noise in the spectrum, which can improve peak detection and fitting.

*   **Savitzky-Golay Filter:**
    *   **Principle:** Fits a low-order polynomial to a moving window of data points and uses the polynomial to estimate the smoothed value at the central point.
    *   **Parameters:** Window Length (odd integer), Polynomial Order (less than window length).
    *   **Pros:** Effective at preserving peak shape, height, and width better than simple moving averages, especially if parameters are chosen well. Can also compute derivatives.
    *   **Cons:** Requires careful parameter selection.

*   **Moving Average Filter:**
    *   **Principle:** Replaces each data point with the average of its neighboring points within a defined window.
    *   **Parameters:** Window Length.
    *   **Pros:** Simple to implement, reduces noise.
    *   **Cons:** Can significantly broaden peaks and reduce their height if the window is too large.

*   **Median Filter:**
    *   **Principle:** Replaces each data point with the median of its neighboring points within a defined window.
    *   **Parameters:** Window Length.
    *   **Pros:** Effective at removing shot noise or spikes while preserving edges (less peak broadening than moving average for similar window sizes).
    *   **Cons:** Can sometimes remove fine details.

*   **Gaussian Filter:**
    *   **Principle:** Convolves the spectrum with a Gaussian kernel.
    *   **Parameters:** Sigma (standard deviation of the Gaussian kernel, controls the degree of smoothing).
    *   **Pros:** Smooths effectively, well-defined mathematical properties.
    *   **Cons:** Will broaden peaks.

## 4. Normalization

Adjusts the scale of spectral intensities to account for variations in overall signal strength due to laser power fluctuations, sample ablation differences, or changes in detection efficiency. This is crucial for comparing spectra or for quantitative analysis.

*   **To Max Intensity (0-1 Scale):**
    *   **Principle:** Divides all intensities in a spectrum by the maximum intensity value found in that spectrum. The resulting spectrum will have a maximum intensity of 1.
    *   **Pros:** Simple, ensures all spectra are on a comparable Y-axis scale.
    *   **Cons:** Sensitive to single outlier spikes if not removed prior. Information about absolute intensity differences between samples is lost.

*   **To Total Area / Sum of Intensities:**
    *   **Principle:** Divides all intensities by the sum of all intensities in the spectrum (or the integrated area under the curve).
    *   **Pros:** Accounts for overall signal output.
    *   **Cons:** Sensitive to baseline offsets if not corrected. Information about absolute intensity differences is lost.

*   **To a Specific Wavelength / Peak Intensity (Internal Standard Principle):**
    *   **Principle:** Divides all intensities by the intensity (or area) of a specific reference peak within the spectrum. This reference peak should ideally be from an element with constant concentration or a matrix line that is stable.
    *   **Parameters:** Wavelength/region of the reference peak.
    *   **Pros:** Can correct for variations in ablation volume and plasma conditions if a good internal standard is available.
    *   **Cons:** Relies on the presence and stability of a suitable reference peak.

*   **Standard Normal Variate (SNV):**
    *   **Principle:** For each spectrum, subtracts its mean intensity and then divides by its standard deviation of intensities. ( `(X - mean(X)) / std(X)` ).
    *   **Pros:** Corrects for both additive (baseline shifts) and multiplicative (scaling) effects on a per-spectrum basis. Widely used in chemometrics.
    *   **Cons:** Information about absolute intensities is lost. Assumes variations are uniform across wavelengths.

*   **Multiplicative Scatter Correction (MSC):**
    *   **Principle:** Attempts to correct for light scattering effects. Each spectrum is regressed against a reference spectrum (often the mean spectrum of the dataset). The offset and slope from this regression are then used to correct the original spectrum.
    *   **Parameters:** Reference Spectrum.
    *   **Pros:** Can be very effective in removing scatter effects that cause wavelength-dependent scaling and offset.
    *   **Cons:** Requires a good reference spectrum. More computationally intensive than SNV.

---

Proper selection and parameterization of these preprocessing steps depend on the specific characteristics of the LIBS data and the goals of the analysis. It is often an iterative process.