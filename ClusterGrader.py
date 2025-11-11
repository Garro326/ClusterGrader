import Orange

# ****************** CONFIGURATIONS ****************** 
# ending image names
obverse_coin = "o.jpg"
reverse_coin = "r.jpg"
# thresholds for quality (everything below medium is "bad")
good = 0.85
medium = 0.65


# creating a dict with Cluster number as key and image_file names (list) as value
data_dict = {}
for data in in_data:
    key = str(data["Cluster"])
    value = str(data["name"])
    data_dict.setdefault(key, []).append(value)

# counting the amount of front-/rear-view images and putting it into a dict
cluster_view_amount_dict = {
    key: {
        "front": sum(img.endswith(obverse_coin) for img in cluster),
        "back": sum(img.endswith(reverse_coin) for img in cluster),
    }
    for key, cluster in data_dict.items()
}


# debug log for the amount of front & rear-view images per cluster
# print(cluster_view_amount_dict)

# new dictionaty that applies quality function on every cluster:
# The key is the cluster label, and the value is the cluster’s quality.
# For each cluster:
#   n = number of front-view images
#   m = number of back-view images
# The quality is calculated as:
#   quality = max(n, m) / (n + m)
# This measures how homogeneous the cluster is. A value close to 1 means the cluster
# contains mostly one type (front or back), while values near 0.5 indicate a mixed or less pure cluster.
quality_dict = {
    key: (max(value["front"], value["back"]) / sum((value["front"], value["back"])))
    for key, value in cluster_view_amount_dict.items()
}

# debug log for the quality of each cluster
# print(quality_dict)


# Calculate the total clustering quality as a weighted average of all cluster qualities.
# Each cluster's quality score (quality_dict[key]) is multiplied by its size (number of images in that cluster),
# so larger clusters have more influence on the final result.
# The sum of all weighted qualities is then divided by the total number of images across all clusters.
# Mathematically:  Q_global = Σ(q_i * n_i) / Σ(n_i)
# where q_i = purity of cluster i, and n_i = number of items in cluster i.
total_images = len(in_data)
global_quality = (
    sum(
        quality_dict[key] * (value["front"] + value["back"])
        for key, value in cluster_view_amount_dict.items()
    )
    / total_images
)

# debug log for the total quality of all selected clusters
# print(global_quality)

# defining columns
columns = Orange.data.Domain(
    [
        Orange.data.ContinuousVariable("Front"),
        Orange.data.ContinuousVariable("Back"),
        Orange.data.ContinuousVariable("Total"),
        Orange.data.ContinuousVariable("Quality"),
        Orange.data.ContinuousVariable("Total-Quality"),
    ],
    metas=[
        Orange.data.StringVariable("Cluster"),
        Orange.data.StringVariable("Quality-Status"),
    ],
)


# funktion that takes the quality and returns a string in traffic-light style
def check_quality(quality):
    if quality >= good:
        return "🟢 high"
    if quality < good and quality >= medium:
        return "🟡 medium"
    else:
        return "🔴 low"


# defining rows
rows = [
    [
        value["front"],
        value["back"],
        value["front"] + value["back"],
        quality_dict[key],
        global_quality,
        key,
        check_quality(quality_dict[key]),
    ]
    for key, value in cluster_view_amount_dict.items()
]

# debug log for the rows of the table
# print(rows)


table = Orange.data.Table(columns, rows)
out_data = table