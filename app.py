import streamlit as st
import matplotlib.pyplot as plt

# Page Replacement Algorithms
def fifo(pages, frames):
    page_set = set()
    page_queue = []
    page_faults = 0
    steps = []

    for page in pages:
        if page not in page_set:
            if len(page_set) < frames:
                page_set.add(page)
                page_queue.append(page)
            else:
                removed_page = page_queue.pop(0)
                page_set.remove(removed_page)
                page_set.add(page)
                page_queue.append(page)
            page_faults += 1
        steps.append(list(page_queue))

    return page_faults, steps


def lru(pages, frames):
    page_set = set()
    page_map = {}
    page_faults = 0
    steps = []

    for i, page in enumerate(pages):
        if page not in page_set:
            if len(page_set) < frames:
                page_set.add(page)
            else:
                lru_page = min(page_map, key=page_map.get)
                page_set.remove(lru_page)
                del page_map[lru_page]
                page_set.add(page)
            page_faults += 1
        page_map[page] = i
        steps.append(sorted(page_set, key=lambda x: page_map[x]))

    return page_faults, steps


def optimal(pages, frames):
    page_set = set()
    page_queue = []
    page_faults = 0
    steps = []

    for i, page in enumerate(pages):
        if page not in page_set:
            if len(page_set) < frames:
                page_set.add(page)
                page_queue.append(page)
            else:
                future_pages = pages[i + 1 :]
                replace_page = -1
                farthest_index = -1
                for p in page_set:
                    if p not in future_pages:
                        replace_page = p
                        break
                    else:
                        index = future_pages.index(p)
                        if index > farthest_index:
                            farthest_index = index
                            replace_page = p
                page_set.remove(replace_page)
                page_queue.remove(replace_page)
                page_set.add(page)
                page_queue.append(page)
            page_faults += 1
        steps.append(list(page_queue))

    return page_faults, steps


# Streamlit UI
st.title("Page Replacement Algorithm Simulator")

# Input fields
pages_input = st.text_input(
    "Enter Page Reference String (e.g., 1,2,3,4,1,2):", "7,0,1,2,0,3,0,4,2,3"
)
frames_input = st.number_input(
    "Enter Number of Frames:", min_value=1, max_value=10, value=3, step=1
)

algorithm = st.selectbox(
    "Select Algorithm", ("FIFO", "LRU", "Optimal"), index=0
)

if st.button("Simulate"):
    try:
        pages = list(map(int, pages_input.split(",")))
        frames = int(frames_input)

        if algorithm == "FIFO":
            faults, steps = fifo(pages, frames)
        elif algorithm == "LRU":
            faults, steps = lru(pages, frames)
        elif algorithm == "Optimal":
            faults, steps = optimal(pages, frames)

        st.success(f"Page Faults using {algorithm}: {faults}")

        # Display Memory Steps
        st.write("Memory State at each step:")
        for i, step in enumerate(steps):
            st.write(f"Step {i + 1}: {step}")

        # Plot Comparison Graph
        fifo_faults, _ = fifo(pages, frames)
        lru_faults, _ = lru(pages, frames)
        opt_faults, _ = optimal(pages, frames)

        algorithms = ["FIFO", "LRU", "Optimal"]
        faults_data = [fifo_faults, lru_faults, opt_faults]

        fig, ax = plt.subplots(figsize=(8, 6))
        bars = ax.bar(
            algorithms, faults_data, color=["#4C72B0", "#55A868", "#C44E52"], width=0.5
        )
        
        ax.set_title("Page Faults Comparison", fontsize=14, weight="bold")
        ax.set_xlabel("Algorithm", fontsize=12)
        ax.set_ylabel("Number of Page Faults", fontsize=12)
        ax.grid(axis="y", linestyle="--", alpha=0.7)
        
        # Add fault count on top of bars
        for bar, value in zip(bars, faults_data):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.5,
                str(value),
                ha="center",
                va="bottom",
                fontsize=11,
            )

        st.pyplot(fig)

    except ValueError:
        st.error("Invalid input! Please enter a valid page reference string (numbers only).")
