import uvicorn
from os import getenv

if __name__ == "__main__":
    default_port = 8000
    port = int(getenv("PORT", default_port))

    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=True)
