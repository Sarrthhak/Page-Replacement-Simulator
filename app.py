import streamlit as st
import matplotlib.pyplot as plt

# FIFO Algorithm
def fifo(pages, frames):
    memory, page_faults = [], 0
    memory_states = []
    
    for page in pages:
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                memory.pop(0)
                memory.append(page)
            page_faults += 1
        memory_states.append(memory[:])
    
    return page_faults, memory_states

# LRU Algorithm
def lru(pages, frames):
    memory, page_faults = [], 0
    memory_states = []
    page_indices = {}
    
    for i, page in enumerate(pages):
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                lru_page = min(memory, key=lambda p: page_indices[p])
                memory.remove(lru_page)
                memory.append(page)
            page_faults += 1
        page_indices[page] = i
        memory_states.append(memory[:])
    
    return page_faults, memory_states

# Optimal Algorithm
def optimal(pages, frames):
    memory, page_faults = [], 0
    memory_states = []
    
    for i, page in enumerate(pages):
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                future_indices = []
                for mem_page in memory:
                    if mem_page in pages[i:]:
                        future_indices.append(pages[i:].index(mem_page))
                    else:
                        future_indices.append(float('inf'))
                
                replace_index = future_indices.index(max(future_indices))
                memory[replace_index] = page
            page_faults += 1
        memory_states.append(memory[:])
    
    return page_faults, memory_states

# Function to run the selected algorithm. It takes type of algorithm, pages sequence and no. of frames as arguments
def run_algorithm(algorithm, pages, frames):
    if algorithm == "FIFO":
        return fifo(pages, frames)
    elif algorithm == "LRU":
        return lru(pages, frames)
    elif algorithm == "Optimal":
        return optimal(pages, frames)

# Interface of Streamlit
st.title("Page Replacement Algorithm Simulator")
st.write(
    "This application simulates and compares the performance of different page replacement algorithms: "
    "FIFO, LRU, and Optimal. Enter the page reference string and number of frames, select an algorithm, "
    "and visualize the results."
)

# Initialize session state for inputs
if "pages_input" not in st.session_state:
    st.session_state.pages_input = ""
if "frames" not in st.session_state:
    st.session_state.frames = 3

# Input for page reference string and number of frames
pages_input = st.text_input(
    "Enter page reference string (comma-separated):", value=st.session_state.pages_input
)
frames = st.number_input(
    "Enter number of frames:", min_value=1, max_value=10, value=st.session_state.frames
)

# Algorithm selection
algorithm = st.selectbox("Select Algorithm", ["FIFO", "LRU", "Optimal"])

# Add Run and Clear buttons side by side with tighter spacing
col1, col2, _ = st.columns([1, 1, 3])

# Adding run simulation button
with col1:
    run_clicked = st.button("Run Simulation")

# Adding clear button
with col2:
    clear_clicked = st.button("Clear")

# Handling the run simulation button
if run_clicked:
    if pages_input:
        pages = list(map(int, pages_input.split(",")))
        page_faults, memory_states = run_algorithm(algorithm, pages, frames)

        st.write(f"**Number of Page Faults:** {page_faults}")
        st.write("**Memory State Changes:**")

        # Split the states into columns to display them side by side
        columns = st.columns(4)  # 4 columns for better layout
        for i, state in enumerate(memory_states):
            with columns[i % 4]:  # Distribute memory states into columns
                st.write(f"Step {i+1}: {state}")

        # Scroll to the results after running the simulation
        st.markdown(
            """
            <script>
                var element = document.getElementById('results');
                if (element) {
                    element.scrollIntoView({behavior: 'smooth', block: 'start'});
                }
            </script>
            """,
            unsafe_allow_html=True,
        )

        # Place an invisible anchor where results are displayed
        st.markdown('<div id="results"></div>', unsafe_allow_html=True)

        # Bar graph to compare page faults
        fig, ax = plt.subplots(figsize=(8, 6))  # Increased figure size
        algorithms = ["FIFO", "LRU", "Optimal"]
        faults = [
            fifo(pages, frames)[0],
            lru(pages, frames)[0],
            optimal(pages, frames)[0],
        ]
        colors = ["#4C72B0", "#55A868", "#C44E52"]  # Professional color palette
        ax.bar(algorithms, faults, color=colors, width=0.6, edgecolor="black")

        ax.set_ylabel("Page Faults", fontsize=12, fontweight="bold")
        ax.set_xlabel("Algorithm", fontsize=12, fontweight="bold")
        ax.set_title("Comparison of Page Faults Across Algorithms", fontsize=14, fontweight="bold")
        ax.grid(axis="y", linestyle="--", alpha=0.7)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        st.pyplot(fig)

        # Find algorithms with minimum and maximum page faults
        min_faults = min(faults)
        max_faults = max(faults)
        
        best_algorithms = [algorithms[i] for i, fault in enumerate(faults) if fault == min_faults]
        worst_algorithms = [algorithms[i] for i, fault in enumerate(faults) if fault == max_faults]
        
        # Format the insights properly
        best_algorithm_str = ", ".join(best_algorithms)
        worst_algorithm_str = ", ".join(worst_algorithms)
        
        # Display insights after the graph
        st.write("## Insights")
        st.write(f"- **Best Performing Algorithm(s):** {best_algorithm_str} with only {min_faults} page faults.")
        st.write(f"- **Least Efficient Algorithm(s):** {worst_algorithm_str} with {max_faults} page faults.")
        st.write("- FIFO performs better when the order of page references is predictable.")
        st.write("- LRU works well when recent pages are more likely to be accessed again soon.")
        st.write("- Optimal gives the best performance but requires future knowledge of page references.")
    else:
        st.warning("Please enter a valid page reference string!")

# Handling the clear button
if clear_clicked:
    st.session_state.pages_input = ""
    st.session_state.frames = 3
    st.rerun()
