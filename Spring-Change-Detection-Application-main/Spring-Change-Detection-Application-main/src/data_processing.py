
import pandas as pd
from typing import List
from config import REQUIRED_COLUMNS,VP_COLUMNS_KEY, VU_COLUMNS_KEY
import streamlit as st 

#__TODO: Clean the dataframe_________________________________
def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize DataFrame columns:
      - Convert all-X columns to 0/1 integers
      - Strip and lowercase text columns
      - Fill other NaNs with zeros

    Args:
        df: Input DataFrame to clean.

    Returns:
        A new DataFrame with cleaned data.
    """
    df = df.copy()
    for col in df.columns:
        s = df[col]
        # normalize checkbox columns (all 'X' → 1, else 0)
        if s.dropna().astype(str).str.upper().isin({'X'}).all():
            df[col] = s.astype(str).str.upper().eq('X').astype(int)
        # strip whitespace & lowercase text
        elif pd.api.types.is_object_dtype(s):
            df[col] = s.fillna('').astype(str).str.strip().str.lower()
        # fill other missing values with 0
        else:
            df[col] = s.fillna(0)
    return df

#__TODO: Generate the result_________________________________
def generate_results_df(
    old_df: pd.DataFrame,
    new_df: pd.DataFrame,
    pta_type: str = "VP"
) -> pd.DataFrame:
    """
    Compare old and new PTA DataFrames to detect spring changes.

    Steps:
      1. Annotate original Excel row numbers
      2. Clean both DataFrames.
      3. Determine composite key columns by PTA type. (VP, VU)
      4. Sequence duplicates to handle identical keys.
      5. Perform full outer merge on keys + sequence.
      6. Normalize reference strings and mass columns.
      7. Compute mass differences/status and detect reference changes.
      8. Classify each record as New, Spring Changed, or Unchanged.
      9. assemble result and select metadata columns
      
    Args:
        old_df: Original PTA DataFrame.
        new_df: Updated PTA DataFrame.
        pta_type: Either "VP" or "VU" to select appropriate key columns.

    Returns:
        A DataFrame with comparison metadata and change classification.
    """
    
    #__TODO: Annotate original row numbers_________________________________
    old = old_df.copy()
    new = new_df.copy()
    
    old["__old_id"] = old.index + 3
    new["__new_id"] = new.index + 3
    
    #__TODO: Clean the dataframes__________________________________________
    old = clean_dataframe(old)
    new = clean_dataframe(new)
    
    #__TODO: Choose composite-key columns___________________________________
    if pta_type == "VP":
        keys = VP_COLUMNS_KEY
    else:
        keys = VU_COLUMNS_KEY
        
    keys = [k for k in keys if k in old.columns and k in new.columns]
    
    #__TODO: sequence duplicates for identical composite keys_________________
    old['__seq'] = old.groupby(keys).cumcount()
    new['__seq'] = new.groupby(keys).cumcount()
    
    #__TODO: Full outer merge ________________________________________________
    merged = pd.merge(
        old, new,
        on = keys + ['__seq'],
        how="outer",
        suffixes = ("_old", "_new"),
        indicator=True
    )
    
    #__TODO: Normalize reference string and mass columns _______________________
    ref_old = f"{REQUIRED_COLUMNS['reference']}_old"
    ref_new = f"{REQUIRED_COLUMNS['reference']}_new"
    mass_old = f"{REQUIRED_COLUMNS['mass']}_old"
    mass_new = f"{REQUIRED_COLUMNS['mass']}_new"

    for col in (ref_old, ref_new):
        merged[col] = (
            merged.get(col, "")
            .fillna("")
            .astype(str)
            .str.replace(r"\.0$", "", regex=True)
            .str.strip()
        )

    merged[mass_old] = merged.get(mass_old, 0).fillna(0).astype(float)
    merged[mass_new] = merged.get(mass_new, 0).fillna(0).astype(float)
    
    #__TODO: Compute mass differences/status and detect reference changes __________
    merged["Mass Difference"] = merged[mass_new] - merged[mass_old]
    merged["Mass Status"] = merged["Mass Difference"].apply(
        lambda d: "Increased" if d > 0 else ("Decreased" if d < 0 else "Unchanged")
    )
    merged["Reference Status"] = merged.apply(
        lambda r: "Change" if r[ref_old] != r[ref_new] else "No Change", axis=1
    )
    
    #__TODO: Classify each record as New ____________________________________________
    def classify(row: pd.Series) -> str:
        if row["_merge"] == "right_only":
            return "New"
        # we drop 'left_only' rows later
        return "Spring Changed" if row[ref_old] != row[ref_new] else "Unchanged"
    
    merged["Change Type"] = merged.apply(classify, axis=1)
    
    # filter out deleted cars
    merged = merged[merged["_merge"] != "left_only"]
    
    #__TODO: Assemble data _________________________________________________________
    
    result_cols = keys + [
        ref_new, ref_old, mass_new, mass_old,
        'Mass Difference', 'Mass Status', 'Reference Status', 'Change Type',
        '__new_id', '__old_id'
    ]
    result_df = merged[result_cols].rename(columns={
        ref_new: 'New Reference',
        ref_old: 'Old Reference',
        mass_new: 'New Mass',
        mass_old: 'Old Mass',
        '__new_id': 'Cell ID New',
        '__old_id': 'Cell ID Old'
    })

    # sort ascending by the new-cell ID
    result_df = result_df.sort_values('Cell ID New', ascending=True).reset_index(drop=True)
    st.session_state['results'] = result_df
    return result_df
