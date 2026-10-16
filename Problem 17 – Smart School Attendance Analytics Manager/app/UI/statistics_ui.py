from services.statistics_service import StatisticsService 
import streamlit as st 

class StatisticsUI:
    def __init__(
        self,
        statistics_service: StatisticsService 
    ) -> None:
        self.statistics_service = statistics_service 
    
    def display(self):
        statistics_table = self.statistics_service.get_data_table_form()
        st.dataframe(statistics_table, hide_index=True)