# ClusterGrader

**ClusterGrader** is a Python script designed for use with **Orange Data Mining**.  
It evaluates how "pure" or homogeneous image clusters are based on their composition of *front-view* and *rear-view* images.  
The script outputs a new Orange Table summarizing per-cluster and global quality metrics.

---

## Features

- Reads an Orange data table (`in_data`) containing at least two meta columns:
  - `"Cluster"` — cluster label assigned by Orange (e.g., from a clustering widget)
  - `"name"` — the corresponding image file name  
- Groups all image names by their cluster label.
- Counts how many **front** (`*.o.jpg`) and **rear** (`*.r.jpg`) images are in each cluster.
- Calculates a **quality score per cluster** using the *purity* formula:  quality = max(front, back) / (front + back)
→ A value close to `1` means the cluster contains mostly one type (front or back); a value around `0.5` means the cluster is mixed.
- Computes an overall (global) cluster quality as a **weighted average** across all clusters: Q_global = Σ(q_i * n_i) / Σ(n_i), 
where `q_i` is the purity of cluster *i*, and `n_i` is its size.
- Outputs all results as a new `Orange.data.Table` for direct visualization in Orange (e.g., via *Data Table* or *Scatter Plot*).

---

## Output Table Structure

| Column            | Description                             |
|-------------------|-----------------------------------------|
| **Cluster**       | Cluster label (string)                  |
| **Front**         | Number of front-view images             |
| **Back**          | Number of rear-view images              |
| **Total**         | Total images in the cluster             |
| **Quality**       | Cluster purity (0–1)                    |
| **Total-Quality** | Global purity score (same for all rows) |

---

## Quick: How to Use in Orange

1. Add a **Python Script** widget to your Orange workflow.  
2. Connect the output of your clustering result **to a Data Table widget first**, and then connect the Data Table **to the Python Script widget**.  
This way, you can verify that the "Cluster" and "name" columns are present before running the script.
3. Paste this code into the widget editor.  
4. Connect the output of the Script widget to a **Data Table** or **Scatter Plot** to visualize results.  

A detailed user manual is also available, providing a step-by-step guide on how to use ClusterGrader.
It includes explanations of different distance metrics, clustering methods, and how to interpret the resulting quality values.

---

## Example Interpretation

**TODO**

- **Quality ≈ 1.0 → good cluster** (contains only front or only back images)  
- **Quality ≈ 0.7 → moderate cluster** (mostly one type, some mixing)  
- **Quality ≤ 0.5 → poor cluster** (strongly mixed)

---

## License

**TODO**

---

## Author

Developed by **Dominik Schmitt Klink & Lisa Haußmann**  
as part of a small research project in collaboration with **Prof. Dr. Karsten Tolle**, *Big Data Lab Frankfurt* at **Goethe-Universität Frankfurt**.  
Project: *"<PROJECT TITLE>"*

