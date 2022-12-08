# Quarto Configuration

## Quarto Dependencies

Before running the Quarto container you will need to install the required Python dependencies on the container

1. Navigate to `/influxdb/quarto-docker`
2. Create a Python virtual environment with `python3 -m venv env` so you have a fresh Python environment with no dependencies initially.
3. Activate, or enter the environment with `source env/bin/activate`.
4. Run this command to install all Python dependencies: `pip install plotly jupyter pandas numpy influxdb-client`. This step may take a while as the dependencies and all implicit dependencies are installed.
5. Use the command `pip freeze > requirements.txt` to save the dependency list to `requirements.txt`.
6. To deactivate, or exit the Python virtual environment, use `deactivate`.
7. The Quarto container can now be built properly.