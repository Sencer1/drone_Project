import kagglehub

# Download latest version
path = kagglehub.dataset_download("banuprasadb/visdrone-dataset")

print("Path to dataset files:", path)