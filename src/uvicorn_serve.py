import uvicorn
import os

if __name__ == "__main__":
    # change directory so can be run from anywhere
    os.chdir("/code/")
    uvicorn.run("app:app", host="0.0.0.0", port=80)