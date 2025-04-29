# main.py

import os
import streamlit.web.cli as stcli
import sys

def main():
    host = os.getenv("COMMAND", "localhost")
    port = os.getenv("PORT", "5672")

    # Set environment variables for consumer to read
    os.environ["RABBITMQ_HOST"] = host
    os.environ["RABBITMQ_PORT"] = port

    # Launch Streamlit app
    sys.argv = ["streamlit", "run", "src/dashboard.py"]
    sys.exit(stcli.main())

if __name__ == "__main__":
    main()
