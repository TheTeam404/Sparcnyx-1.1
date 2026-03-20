# SpectraMapper Pro - Developer Guide

This guide is intended for developers looking to understand, maintain, or contribute to the SpectraMapper Pro codebase.

## Table of Contents

1.  [Introduction](#introduction)
2.  [Project Structure](#project-structure)
3.  [Core Technologies](#core-technologies)
4.  [Setup for Development](#setup-for-development)
5.  [Code Style and Conventions](#code-style-and-conventions)
6.  [Architecture Overview](#architecture-overview)
    *   [GUI (PyQt5/PySide6)](#gui-pyqt5pyside6)
    *   [Core Logic](#core-logic)
    *   [Data Models](#data-models)
    *   [Workers (Threading)](#workers-threading)
7.  [Key Modules Deep Dive](#key-modules-deep-dive)
    *   [`team404/main.py`](#team404mainpy)
    *   [`team404/core/`](#team404core)
    *   [`team404/gui/`](#team404gui)
    *   [`team404/database/`](#team404database)
    *   [`team404/workers/`](#team404workers)
8.  [Adding a New Preprocessing Step](#adding-a-new-preprocessing-step)
9.  [Adding a New Chemometric Method](#adding-a-new-chemometric-method)
10. [Working with Plots (Matplotlib)](#working-with-plots-matplotlib)
11. [Database Interaction](#database-interaction)
12. [Testing](#testing)
13. [Building and Packaging (Future)](#building-and-packaging-future)
14. [Contribution Guidelines](#contribution-guidelines)

---

## 1. Introduction

SpectraMapper Pro aims to be a robust and user-friendly tool for LIBS data analysis. This guide details its internal structure and development practices.

## 2. Project Structure

The project follows a modular structure:

Team404_LIBS_Analysis/
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── data/ # Example data, user databases
├── docs/ # This guide, user guide, methodologies
└── team404/ # Main application source code
├── init.py
├── app_config.py # Application-wide configurations
├── main.py # Main application entry point
├── assets/ # Icons, UI resources, templates
├── core/ # Core processing algorithms, data handling
├── database/ # Database interaction (NIST, user)
├── gui/ # PyQt GUI components (windows, tabs, widgets)
├── plotting/ # Matplotlib integration
├── utils/ # Helper functions, constants, logging
└── workers/ # QThread implementations for background tasks
└── tests/ # Unit and integration tests


## 3. Core Technologies

*   **Python:** 3.9+
*   **GUI:** PyQt5 (or PySide6 if migrated)
*   **Numerical Computing:** NumPy
*   **Scientific Computing:** SciPy (signal processing, optimization, special functions)
*   **Data Handling:** Pandas (for tabular data, especially peak lists, results)
*   **Machine Learning:** Scikit-learn (PCA, PLS, classification)
*   **Plotting:** Matplotlib (embedded in Qt)
*   **Database:** SQLite3 (for local NIST ASD)

## 4. Setup for Development

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url> Team404_LIBS_Analysis
    cd Team404_LIBS_Analysis
    ```
2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    # Activate it:
    # Windows: venv\Scripts\activate
    # macOS/Linux: source venv/bin/activate
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    pip install -r requirements-dev.txt # If you create one for dev tools like pytest, flake8
    ```
4.  **Run the Application:**
    ```bash
    python team404/main.py
    ```

## 5. Code Style and Conventions

*   **PEP 8:** Follow PEP 8 guidelines for Python code. Use a linter like Flake8.
*   **Docstrings:** Use Google-style or NumPy-style docstrings for all modules, classes, and functions.
*   **Type Hinting:** Utilize Python type hints for better code clarity and static analysis.
*   **Comments:** Write clear comments for complex logic.
*   **Naming:**
    *   Modules: `lowercase_with_underscores.py`
    *   Classes: `PascalCase`
    *   Functions/Methods: `snake_case`
    *   Constants: `UPPERCASE_WITH_UNDERSCORES`
*   **Qt Specific:**
    *   UI elements often prefixed with `ui_` or a descriptive prefix (e.g., `preprocess_tab_widget`).
    *   Signal/slot connections should be clear.

## 6. Architecture Overview

The application is designed with a separation of concerns:

### GUI (PyQt5/PySide6)
*   Located in `team404/gui/`.
*   `main_window.py`: The central QMainWindow.
*   `tabs/`: Each functional module is implemented as a QWidget (or a custom class inheriting QWidget) and added as a tab to a QTabWidget in the main window.
*   `widgets/`: Reusable custom widgets (e.g., plot canvas, parameter inputs).
*   `dialogs/`: Standard dialogs (Preferences, About, Error).
*   The GUI is responsible for user interaction and displaying data. It should delegate heavy processing to the core logic.

### Core Logic
*   Located in `team404/core/`.
*   Contains modules for each type of data processing:
    *   `file_io.py`: Loading and saving spectra, projects.
    *   `spectrum_handler.py`: Represents a single spectrum and its processing state.
    *   `preprocessing_algorithms.py`: Implementations of baseline correction, smoothing, etc.
    *   `peak_algorithms.py`: Peak detection and fitting (e.g., Voigt).
    *   `elemental_identifier.py`: Logic for matching peaks against databases.
    *   `quantitative_analyzer.py`: Boltzmann plot calculations.
    *   `mapping_processor.py`: Handles batch processing for 2D maps.
    *   `chemometrics_tools.py`: Wrappers around Scikit-learn methods.
*   These modules should be GUI-agnostic.

### Data Models
*   Located in `team404/core/data_models.py` (or within specific handlers).
*   Defines classes to represent data structures like `Spectrum`, `Project`, `Peak`, `ElementalMap`.
*   Pandas DataFrames are often used for tabular data internally.

### Workers (Threading)
*   Located in `team404/workers/`.
*   Subclasses of `QThread` (or `QObject` moved to a thread) for long-running tasks to prevent GUI freezing.
*   Examples: Online NIST search, batch preprocessing for maps, complex model training.
*   Use Qt signals to communicate progress and results back to the GUI thread.

## 7. Key Modules Deep Dive

### `team404/main.py`
*   The entry point of the application.
*   Initializes `QApplication`.
*   Creates and shows the `MainWindow`.
*   Starts the Qt event loop.

### `team404/core/`
*   **`project_manager.py`**: Handles loading, saving, and managing project state (list of spectra, processing parameters, results).
*   **`spectrum_handler.py`**: A class that encapsulates a single LIBS spectrum (wavelengths, intensities). It should also manage its processing history (applied steps and parameters) and provide methods to get the current state of the spectrum (raw, preprocessed).
*   **`preprocessing_algorithms.py`**: Contains functions for each preprocessing step (e.g., `subtract_baseline_als(spectrum_data, lambda_val, p_val)`). These functions should take NumPy arrays as input and return processed NumPy arrays.
*   **`peak_algorithms.py`**:
    *   Peak detection: `find_peaks_scipy(intensity_array, **kwargs)`.
    *   Voigt fitting: `fit_voigt_profile(wavelength_roi, intensity_roi, initial_guesses)`. Uses `scipy.optimize.curve_fit` and a Voigt profile function (e.g., `scipy.special.voigt_profile` or a custom implementation).
*   **`elemental_identifier.py`**: Queries the database (via `nist_db_connector.py`) and matches experimental peaks.

### `team404/gui/`
*   **`main_window.py`**: Sets up the main UI layout, menu bar, toolbar, status bar, and tab widget. Connects signals from UI elements to handler methods.
*   **`tabs/base_tab.py`**: (Optional but good practice) A base class for all functional tabs, providing common structure or methods.
*   **`tabs/*_tab.py`**: Each tab module (e.g., `preprocessing_tab.py`) creates its specific UI layout, connects its widgets to core logic, and updates its display based on data changes.
*   **`widgets/spectrum_plot_widget.py`**: A custom QWidget that embeds a Matplotlib `FigureCanvasQTAgg` for displaying spectra. Provides methods for plotting, updating plots, and handling plot interactions (zoom, pan, peak selection).

### `team404/database/`
*   **`nist_db_connector.py`**:
    *   Manages connections to the SQLite database (`nist_asd.db`).
    *   Provides methods to query for spectral lines based on element, ion stage, and wavelength range (e.g., `get_lines(element, ion_stage, w_min, w_max)`).
    *   Handles parsing of CSV files if that fallback is used.
*   **`user_custom_db.py`**: (Optional) For managing user-added lines or custom databases.

### `team404/workers/`
*   **`base_worker.py`**: A base `QObject` (or `QThread`) class defining common signals like `started`, `finished`, `progress`, `error`, `result_ready`.
*   Each specific worker (e.g., `MappingGenerationWorker`) inherits from this, implements its `run()` method to perform the task, and emits signals accordingly.

## 8. Adding a New Preprocessing Step

1.  **Core Logic (`preprocessing_algorithms.py`):**
    *   Implement a new Python function that takes a spectrum's data (NumPy arrays for wavelengths and intensities) and relevant parameters as input.
    *   The function should return the processed intensity array.
    *   Add clear docstrings and type hints.
    *   Example: `def new_filter_method(intensities, param1, param2): ... return processed_intensities`
2.  **GUI (`preprocessing_tab.py` and `parameter_input_widgets.py`):**
    *   Add the new method's name to the list of available preprocessing steps in `preprocessing_tab.py`.
    *   Create necessary QWidgets (e.g., QSpinBox, QLineEdit) in `parameter_input_widgets.py` (or directly in the tab) for the new method's parameters.
    *   Update `preprocessing_tab.py` to:
        *   Show/hide the relevant parameter widgets when the new method is selected.
        *   Gather parameter values from these widgets.
        *   Call the core logic function with the spectrum data and parameters.
        *   Update the preview plot with the result.
3.  **Data Model/Project Management (if parameters need saving):**
    *   Ensure the `ProjectManager` can save and load the name of this new step and its parameters as part of a processing pipeline.
4.  **Documentation:**
    *   Update `docs/user_guide.md` and `docs/methodologies/preprocessing_methods.md`.

## 9. Adding a New Chemometric Method

1.  **Core Logic (`chemometrics_tools.py`):**
    *   Implement a function that takes a dataset (e.g., multiple spectra as a 2D NumPy array, target variables if applicable) and parameters.
    *   Utilize Scikit-learn or other relevant libraries.
    *   The function should return results (e.g., PCA scores/loadings, model predictions, metrics).
2.  **GUI (`chemometrics_tab.py`):**
    *   Add the new method to the UI for selection.
    *   Create input widgets for its parameters.
    *   Call the core function (potentially in a worker thread if time-consuming).
    *   Display results (plots, tables).
3.  **Documentation:** Update user guide and methodologies.

## 10. Working with Plots (Matplotlib)

*   Use `matplotlib.backends.backend_qt5agg.FigureCanvasQTAgg` to embed Matplotlib plots in Qt widgets.
*   Create a `Figure` and `Axes` object.
*   Plot data using standard Matplotlib commands (`ax.plot()`, `ax.imshow()`, etc.).
*   Call `canvas.draw()` to refresh the plot.
*   For interactivity (zoom, pan), use `matplotlib.backends.backend_qt5agg.NavigationToolbar2QT`.
*   The `plotting/plot_canvas.py` can encapsulate a reusable Matplotlib canvas widget.
*   `plotting/plot_functions.py` can hold common plotting routines to avoid code duplication.

## 11. Database Interaction

*   All direct SQLite interaction should be handled by `nist_db_connector.py`.
*   Use parameterized queries to prevent SQL injection vulnerabilities (though less critical for a local, user-provided DB, it's good practice).
    ```python
    # Example in nist_db_connector.py
    cursor.execute("SELECT wavelength, rel_intensity FROM Fe_I WHERE wavelength BETWEEN ? AND ?", (w_min, w_max))
    ```
*   Handle potential `sqlite3.Error` exceptions.

## 12. Testing

*   Located in the `tests/` directory.
*   Use `pytest` as the testing framework.
*   **Unit Tests (`tests/test_core/`):** Test individual functions and methods in the core logic modules. Mock external dependencies (like file system access or complex GUI parts if testing core logic called by GUI).
*   **GUI Tests (`tests/test_gui/`):** (Can be more complex) Use `pytest-qt` to test GUI interactions, widget states, and signal emissions. These are often more like integration tests.
*   Aim for good test coverage, especially for critical algorithms.
*   `conftest.py` can be used for shared fixtures.

## 13. Building and Packaging (Future)

*   For creating standalone executables, consider tools like:
    *   **PyInstaller:** Bundles the Python application and its dependencies.
    *   **cx_Freeze:** Another option for freezing Python scripts.
*   This will involve creating a build script (e.g., a `.spec` file for PyInstaller).

## 14. Contribution Guidelines

(If this were an open-source project)
1.  **Fork the repository.**
2.  **Create a new branch** for your feature or bug fix (`git checkout -b feature/my-new-feature` or `bugfix/issue-123`).
3.  **Make your changes.**
4.  **Write tests** for your changes.
5.  **Ensure all tests pass.**
6.  **Follow code style guidelines.**
7.  **Update documentation** if necessary.
8.  **Submit a Pull Request** with a clear description of your changes.

---
This developer guide provides a starting point. It will evolve as the project grows.