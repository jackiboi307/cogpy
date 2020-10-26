import os
for filename in os.listdir():
    if filename.endswith(".py"):
        with open(filename[:-3]+".bat", "w") as f:
            f.write(f"@echo all\npy {filename}")
