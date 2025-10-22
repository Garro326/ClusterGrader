import Orange

# debug looking into the key values of the table
#print([m.name for m in in_data.domain.metas])


# creating a dict with Cluster as key and image_file names (list) as value
data_dict = {}
for data in in_data:
    key = str(data["Cluster"])
    value = str(data["name"])
    data_dict.setdefault(key, []).append(value)

# counting the amount of front-/rear-view images and putting it into a dict
cluster_view_amount_dict = {
                            key:{
                                 "front": sum(img.endswith("o.jpg") for img in cluster),
                                 "back": sum(img.endswith("r.jpg") for img in cluster)}
                                for key, cluster in data_dict.items()}


        
# debug log for the amount of front/rear-view images
#print(cluster_view_amount_dict)

# new dict that applies quality function on every cluster
quality_dict = {
                key: (max(value["front"], value["back"])/ 
                      sum((value["front"], value["back"])))
                for key, value in cluster_view_amount_dict.items()}

# debug log for the quality of each cluster
#print(quality_dict)


# total cluster quality (gewichteter Mittelwert)
total_images = len(in_data)
global_quality = sum(
                     quality_dict[key] * 
                     (value["front"] + value["back"])
                     for key, value in cluster_view_amount_dict.items()
                     )/total_images
                     
# debug log for the total quality of all selected clusters
#print(global_quality)

# defining columns
columns = Orange.data.Domain([
                             Orange.data.ContinuousVariable("Front"),
                             Orange.data.ContinuousVariable("Back"),
                             Orange.data.ContinuousVariable("Total"),
                             Orange.data.ContinuousVariable("Quality"),
                             Orange.data.ContinuousVariable("Total-Quality")
                             ],
                             metas=[Orange.data.StringVariable("Cluster")]
                             )

# defining rows
rows = [
        [
         value["front"],
         value["back"],
         value["front"] + value["back"],
         quality_dict[key],
         global_quality,
         key,
         ]
        for key, value in cluster_view_amount_dict.items()
        ]

# debug log for the rows of the table
# print(rows)

table = Orange.data.Table(columns, rows)
out_data = table