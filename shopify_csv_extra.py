import streamlit as st
import pandas as pd
import io
import re

def clean_csv(df):
    df.dropna(how='all', inplace=True)
    df.dropna(axis=1, how='all', inplace=True)
    # Remove all non-alphanumeric ASCII characters from all string columns
    def clean_str(val):
        if isinstance(val, str):
            # Keep only A-Z, a-z, 0-9, and whitespace
            return re.sub(r'[^A-Za-z0-9\s]', '', val)
        return val
    df = df.applymap(clean_str)
    return df

def merge_csvs(df1, df2, merge_column):
    try:
        merged = pd.merge(df1, df2, on=merge_column, how='left')
        return merged
    except Exception as e:
        st.error(f"Error while merging: {e}")
        return None

def column_mapper(df, mapping_dict):
    return df.rename(columns=mapping_dict)

def main():
    st.set_page_config(page_title="CSV Pro Toolkit for Shopify", layout="centered")
    st.title("🛠️ Shopify CSV Pro Toolkit")

    st.markdown("This tool helps Shopify sellers clean, merge, and reformat product CSV files.")

    tab1, tab2, tab3 = st.tabs(["📤 Clean CSV", "🔀 Merge CSVs", "🧩 Column Mapper"])

    with tab1:
        st.header("📤 Clean CSV")
        uploaded_file = st.file_uploader("Upload CSV", type="csv", key="clean_csv")
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
            except UnicodeDecodeError:
                df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
                st.warning("Encoding issue. Using fallback.")

            if st.button("Clean"):
                df_clean = clean_csv(df)
                st.success("Cleaned!")

                st.subheader("Preview")
                st.dataframe(df_clean.head())

                csv_buffer = io.StringIO()
                df_clean.to_csv(csv_buffer, index=False)
                st.download_button("Download Cleaned CSV", csv_buffer.getvalue(), file_name="cleaned.csv", mime="text/csv")

    with tab2:
        st.header("🔀 Merge Two CSVs")
        col1, col2 = st.columns(2)
        with col1:
            csv1 = st.file_uploader("Upload Main CSV", type="csv", key="main_csv")
        with col2:
            csv2 = st.file_uploader("Upload CSV to Merge", type="csv", key="merge_csv")

        if csv1 and csv2:
            df1 = pd.read_csv(csv1)
            df2 = pd.read_csv(csv2)

            common_cols = list(set(df1.columns).intersection(set(df2.columns)))
            if common_cols:
                key_col = st.selectbox("Select column to merge on", common_cols)
                if st.button("Merge CSVs"):
                    merged_df = merge_csvs(df1, df2, key_col)
                    if merged_df is not None:
                        st.success("Merged successfully!")
                        st.dataframe(merged_df.head())

                        csv_buffer = io.StringIO()
                        merged_df.to_csv(csv_buffer, index=False)
                        st.download_button("Download Merged CSV", csv_buffer.getvalue(), file_name="merged.csv", mime="text/csv")
            else:
                st.error("No matching columns found to merge.")

    with tab3:
        st.header("🧩 Column Mapping for Shopify")
        file = st.file_uploader("Upload CSV to Map", type="csv", key="map_csv")
        if file:
            df = pd.read_csv(file)
            st.dataframe(df.head(3))

            st.subheader("Map Your Columns to Shopify Format")
            mapping = {}
            for col in df.columns:
                new_col = st.text_input(f"Map '{col}' to:", value=col)
                mapping[col] = new_col

            if st.button("Apply Mapping"):
                mapped_df = column_mapper(df, mapping)
                st.dataframe(mapped_df.head())

                csv_buffer = io.StringIO()
                mapped_df.to_csv(csv_buffer, index=False)
                st.download_button("Download Mapped CSV", csv_buffer.getvalue(), file_name="shopify_mapped.csv", mime="text/csv")

if __name__ == "__main__":
    main()
