# ==========================
# Step 1: load the data
def load(path):
    try:
        return open(path).read()
    except:
        pass
