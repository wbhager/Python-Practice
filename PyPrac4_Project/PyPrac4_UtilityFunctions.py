# Necessary utility functions for PyPrac4 project

def validate_dataframe(df, required_columns):
    """This utility function will make sure that each csv file has the required columns 
        necessary before being read in, ensuring consistency."""
    if df.empty:
        raise ValueError("Nothing to load in, the dataframe is empty.")
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Dataframe is missing one or more pivotal columns: {missing}. File will not be ingested into a dataframe after all.")



