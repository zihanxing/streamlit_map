

# Natural Disaster Prediction Dashboard

This Streamlit application, titled 'Natural Disaster Prediction in the United States', is the front end part of the AIPI 510 Project developed by Nicholas Conterno, Sri Veerisetti, and Zihan (Zach) Xing. The app utilizes data-driven insights to predict and display natural disaster impacts across the United States.

![Alt text](<UI.png>)

### Features

- **Interactive Map**: Visualize natural disaster data across different states in the US.
- **Time Filtering**: Filter data based on the year, including predictions for 2024.
- **State Filtering**: View data for a specific state.
- **Risk Level Analysis**: Filter predictions for 2024 based on risk levels (Low, Medium, High).
- **Detailed Metrics**: View detailed metrics like total deaths, total damage, and total disasters.

### How to Run

1. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Streamlit App**:
   Execute the following command:
   ```bash
   streamlit run app.py
   ```

### Data Sources

- US State Boundaries: [US State Boundaries Dataset](https://public.opendatasoft.com/explore/dataset/us-state-boundaries/export/)
- The main data for natural disaster predictions is loaded from a CSV file (`data/predictions/merged.csv`).

### Dependencies

- Streamlit
- Pandas
- Folium
- Streamlit-Folium (for integrating Folium maps with Streamlit)

### Application Structure

1. **Filters**: 
   - Time Filters (`display_time_filters`): For selecting the year.
   - State Filter (`display_state_filter`): For selecting a specific state.
   - Risk Level Filter (`display_risk_level`): For filtering predictions based on risk level (2024 only).

2. **Map Visualization** (`display_map`):
   - Generates an interactive map showing natural disaster data.

3. **Data Presentation**:
   - Display disaster metrics like total deaths, total damage, and total disasters for selected filters.

### Reference

Chowdhury, Z. (2023). streamlit-map-dashboard [Software]. GitHub. https://github.com/zakariachowdhury/streamlit-map-dashboard
