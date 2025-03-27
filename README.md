# Page-Replacement-Simulator

This project is a simulator designed to explore how page replacement algorithms work in operating systems. It focuses on three popular algorithms: **FIFO (First-In-First-Out)**, **LRU (Least Recently Used)**, and **Optimal**. The goal is to analyze their behavior by tracking page faults and visualizing performance with an interactive interface.

---

## What It Does
- Simulates FIFO, LRU, and Optimal page replacement algorithms.
- Allows users to set the number of memory frames and input a custom page request sequence.
- Displays the number of page faults for each algorithm to compare efficiency.
- Provides a visual representation of memory state changes at each step.
- Generates a bar chart to compare page faults across all algorithms.

---

## Getting Started

### Requirements
- Python 3.x installed (any recent version should work).
- Required libraries:
```bash
pip install streamlit matplotlib
```

---

## Setup Steps
1. Clone the Repository:
```bash
git clone https://github.com/gobarihimanshu071/Page-Replacement-Simulator.git
```

2. Move into the project folder:
```bash
cd Page-Replacement-Simulator
```

3. Install Required Libraries:
```bash
pip install -r requirements.txt
```

4. Run the Application:
```bash
streamlit run main.py
```

---

## How to Use It
1. **Enter Page Reference String:** Provide a comma-separated list of pages (e.g., `1,2,3,4,1,2,5`).
2. **Set Number of Frames:** Select the number of available memory frames.
3. **Choose Algorithm:** Select from FIFO, LRU, or Optimal.
4. **Run Simulation:** Click the **Run Simulation** button to generate the results.
5. **Visualize Results:**
   - Check page faults and memory state changes.
   - Compare page faults across algorithms with a bar graph.

---

## Project Breakdown
- **main.py:** Contains the complete logic, UI, and algorithm simulations.
- **LICENSE:** License information for the project.
- **README.md:** Project documentation and usage instructions.

---

## Algorithms Explained
- **FIFO (First-In-First-Out):** Removes the oldest page when a new page needs to be loaded.
- **LRU (Least Recently Used):** Removes the least recently used page to make room for a new one.
- **Optimal:** Removes the page that will not be used for the longest period of time.

---

## Tools Used
- **Python:** Handles the core logic and processing.
- **Streamlit:** Builds an interactive and user-friendly GUI.
- **Matplotlib:** Generates bar charts for performance comparison.

---

## Feedback or Ideas
This project is a work in progress.  
You can:
- Report bugs or suggest features by opening an issue.
- Contribute by submitting a pull request.
- Provide any feedback to help improve the project.
