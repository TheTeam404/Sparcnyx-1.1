# tests/test_core/test_element_recognizer.py

"""
Unit tests for the Vector Space Model element recognition engine.
"""

import pytest
import numpy as np

from team404.core.element_recognizer import (
    compute_variable_bands,
    _count_peaks_in_band,
    _cosine_similarity,
    VectorSpaceElementRecognizer,
    WavelengthMatchFrequencyScorer,
)
from team404.core.data_models import Peak


# ------------------------------------------------------------------ #
# Helpers
# ------------------------------------------------------------------ #

def make_peak(wl: float) -> Peak:
    return Peak(detected_wavelength_nm=wl, detected_intensity=1000.0)


# ------------------------------------------------------------------ #
# compute_variable_bands
# ------------------------------------------------------------------ #

class TestComputeVariableBands:
    def test_sparse_spectrum_uses_50nm_bands(self):
        """0–2 peaks per 50 nm → d = 50 nm (Eq. 2, Paper 1)."""
        bands = compute_variable_bands(200.0, 800.0, 5)   # ~0.4 peaks/50 nm
        assert all(be - bs <= 50.0 + 1e-9 for bs, be in bands), "Expected ≤50 nm bands"
        widths = [be - bs for bs, be in bands]
        assert max(widths) <= 50.0 + 1e-9

    def test_medium_density_uses_10nm_bands(self):
        """3–5 peaks per 50 nm → d = 10 nm."""
        # 50 peaks over 500 nm → 5 peaks per 50 nm → medium boundary
        bands = compute_variable_bands(200.0, 700.0, 50)
        widths = [be - bs for bs, be in bands]
        assert max(widths) <= 10.0 + 1e-9

    def test_dense_spectrum_uses_5nm_bands(self):
        """More than 5 peaks per 50 nm → d = 5 nm."""
        # 200 peaks over 500 nm → 20 peaks per 50 nm → dense
        bands = compute_variable_bands(200.0, 700.0, 200)
        widths = [be - bs for bs, be in bands]
        assert max(widths) <= 5.0 + 1e-9

    def test_bands_cover_full_range(self):
        bands = compute_variable_bands(250.0, 850.0, 30)
        assert abs(bands[0][0] - 250.0) < 1e-9
        assert abs(bands[-1][1] - 850.0) < 1e-9

    def test_bands_are_contiguous_and_non_overlapping(self):
        bands = compute_variable_bands(300.0, 700.0, 20)
        for i in range(len(bands) - 1):
            assert abs(bands[i][1] - bands[i + 1][0]) < 1e-9, \
                f"Gap or overlap between band {i} and {i+1}"

    def test_single_point_range(self):
        bands = compute_variable_bands(400.0, 400.0, 0)
        assert len(bands) == 1


# ------------------------------------------------------------------ #
# _count_peaks_in_band
# ------------------------------------------------------------------ #

class TestCountPeaksInBand:
    def test_counts_peaks_inside_band(self):
        wls = [300.0, 320.5, 349.9, 350.1]  # 350.1 is outside [300, 350)
        assert _count_peaks_in_band(wls, 300.0, 350.0) == 3

    def test_empty_list(self):
        assert _count_peaks_in_band([], 300.0, 400.0) == 0

    def test_peak_exactly_at_start_included(self):
        assert _count_peaks_in_band([300.0], 300.0, 350.0) == 1

    def test_peak_exactly_at_end_excluded(self):
        # Half-open interval [start, end)
        assert _count_peaks_in_band([350.0], 300.0, 350.0) == 0


# ------------------------------------------------------------------ #
# _cosine_similarity
# ------------------------------------------------------------------ #

class TestCosineSimilarity:
    def test_identical_vectors_score_one(self):
        v = np.array([1.0, 2.0, 3.0])
        assert pytest.approx(_cosine_similarity(v, v), abs=1e-9) == 1.0

    def test_orthogonal_vectors_score_zero(self):
        a = np.array([1.0, 0.0, 0.0])
        b = np.array([0.0, 1.0, 0.0])
        # b has non-zero at index 1; projected a at index 1 is 0 → dot = 0
        assert pytest.approx(_cosine_similarity(a, b), abs=1e-9) == 0.0

    def test_zero_standard_vector_returns_zero(self):
        a = np.array([1.0, 2.0, 3.0])
        b = np.zeros(3)
        assert _cosine_similarity(a, b) == 0.0

    def test_projection_mask_correctly_applied(self):
        # v_b has non-zero only at indices 0, 2
        v_a = np.array([3.0, 0.0, 4.0])
        v_b = np.array([3.0, 0.0, 4.0])
        score = _cosine_similarity(v_a, v_b)
        assert pytest.approx(score, abs=1e-6) == 1.0

    def test_score_clipped_to_one(self):
        v = np.array([5.0, 5.0])
        assert _cosine_similarity(v, v) <= 1.0

    def test_mismatched_sizes_return_zero(self):
        a = np.array([1.0, 2.0])
        b = np.array([1.0, 2.0, 3.0])
        assert _cosine_similarity(a, b) == 0.0


# ------------------------------------------------------------------ #
# VectorSpaceElementRecognizer
# ------------------------------------------------------------------ #

class TestVectorSpaceElementRecognizer:
    def setup_method(self):
        self.rec = VectorSpaceElementRecognizer()

    def test_returns_empty_list_with_no_peaks(self):
        results = self.rec.recognize_elements(
            peaks=[],
            db_lines_by_element={"Fe I": [{"wavelength_nm": 300.0}]},
            wl_min=200.0, wl_max=800.0
        )
        assert results == []

    def test_returns_empty_list_with_no_db_lines(self):
        peaks = [make_peak(300.0)]
        results = self.rec.recognize_elements(
            peaks=peaks,
            db_lines_by_element={},
            wl_min=200.0, wl_max=800.0
        )
        assert results == []

    def test_perfect_match_gives_high_score(self):
        """Same set of wavelengths in peaks and DB → near-perfect cosine."""
        wls = [300.0, 350.0, 400.0, 450.0, 500.0, 550.0, 600.0]
        peaks = [make_peak(w) for w in wls]
        db_lines = [{"wavelength_nm": w} for w in wls]
        results = self.rec.recognize_elements(
            peaks=peaks,
            db_lines_by_element={"Fe I": db_lines},
            wl_min=200.0, wl_max=800.0,
            threshold=0.0
        )
        assert len(results) == 1
        assert results[0]['element'] == "Fe I"
        assert results[0]['score'] >= 0.90, f"Expected ≥0.9, got {results[0]['score']}"

    def test_no_overlap_gives_zero_below_threshold(self):
        """DB lines in completely different bands than experimental peaks."""
        exp_peaks = [make_peak(w) for w in [200.0, 201.0, 202.0]]
        db_lines = [{"wavelength_nm": w} for w in [700.0, 701.0, 702.0]]
        results = self.rec.recognize_elements(
            peaks=exp_peaks,
            db_lines_by_element={"Ca II": db_lines},
            wl_min=200.0, wl_max=800.0,
            threshold=0.5
        )
        # Score should be 0 (no overlap) and thus below threshold
        assert results == []

    def test_results_sorted_by_score_descending(self):
        """Multiple elements → results come back highest-score-first."""
        peaks = [make_peak(w) for w in [300.0, 350.0, 400.0]]
        db_good = [{"wavelength_nm": w} for w in [300.0, 350.0, 400.0]]
        db_poor = [{"wavelength_nm": w} for w in [500.0, 550.0, 600.0]]
        results = self.rec.recognize_elements(
            peaks=peaks,
            db_lines_by_element={"Top": db_good, "Bottom": db_poor},
            wl_min=200.0, wl_max=800.0,
            threshold=0.0
        )
        scores = [r['score'] for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_threshold_filters_low_scores(self):
        peaks = [make_peak(300.0)]
        db_lines = [{"wavelength_nm": 700.0}]  # No overlap
        results = self.rec.recognize_elements(
            peaks=peaks,
            db_lines_by_element={"Mg I": db_lines},
            wl_min=200.0, wl_max=800.0,
            threshold=0.5
        )
        assert all(r['score'] >= 0.5 for r in results)

    def test_build_sample_vector_shape_matches_bands(self):
        peaks = [make_peak(w) for w in [300.0, 350.0, 500.0]]
        v, bands = self.rec.build_sample_vector(peaks, 200.0, 800.0)
        assert len(v) == len(bands)
        assert v.dtype == float or np.issubdtype(v.dtype, np.floating)


# ------------------------------------------------------------------ #
# WavelengthMatchFrequencyScorer
# ------------------------------------------------------------------ #

class TestWavelengthMatchFrequencyScorer:
    def setup_method(self):
        self.scorer = WavelengthMatchFrequencyScorer()

    def test_all_matching_gives_score_one(self):
        peaks = [make_peak(300.0), make_peak(400.0)]
        db_lines = [{"wavelength_nm": 300.0}, {"wavelength_nm": 400.0}]
        results = self.scorer.score_elements(
            peaks=peaks,
            db_lines_by_element={"Fe I": db_lines},
            tolerance_nm=0.1,
            threshold=0.0
        )
        assert len(results) == 1
        assert pytest.approx(results[0]['score'], abs=1e-6) == 1.0

    def test_no_matching_gives_score_zero(self):
        peaks = [make_peak(300.0)]
        db_lines = [{"wavelength_nm": 700.0}]
        results = self.scorer.score_elements(
            peaks=peaks,
            db_lines_by_element={"Ca II": db_lines},
            tolerance_nm=0.05,
            threshold=0.0
        )
        assert results[0]['score'] == 0.0

    def test_partial_match_gives_correct_fraction(self):
        peaks = [make_peak(300.0), make_peak(400.0)]
        db_lines = [
            {"wavelength_nm": 300.0},   # match
            {"wavelength_nm": 500.0},   # no match
        ]
        results = self.scorer.score_elements(
            peaks=peaks,
            db_lines_by_element={"X": db_lines},
            tolerance_nm=0.1,
            threshold=0.0
        )
        assert pytest.approx(results[0]['score'], abs=1e-6) == 0.5
        assert results[0]['n_matched'] == 1
        assert results[0]['n_db_lines'] == 2

    def test_no_peaks_returns_empty(self):
        results = self.scorer.score_elements(
            peaks=[],
            db_lines_by_element={"Fe I": [{"wavelength_nm": 300.0}]},
            tolerance_nm=0.1
        )
        assert results == []

    def test_results_sorted_descending(self):
        peaks = [make_peak(300.0), make_peak(400.0)]
        db_good = [{"wavelength_nm": 300.0}, {"wavelength_nm": 400.0}]
        db_poor = [{"wavelength_nm": 300.0}, {"wavelength_nm": 500.0}]
        results = self.scorer.score_elements(
            peaks=peaks,
            db_lines_by_element={"Good": db_good, "Poor": db_poor},
            tolerance_nm=0.1,
            threshold=0.0
        )
        scores = [r['score'] for r in results]
        assert scores == sorted(scores, reverse=True)
