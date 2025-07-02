import streamlit as st
import pandas as pd
import io

def clean_csv(df):
    """Remove empty rows and columns."""
    df.dropna(how='all', inplace=True)
    df.dropna(axis=1, how='all', inplace=True)
    return df

def main():
    st.set_page_config(page_title="CSV Cleaner for Shopify", layout="centered")
    st.title("🧼 CSV Cleaner for Shopify")
    st.write("Upload your product CSV and clean it before importing into Shopify.")

    uploaded_file = st.file_uploader("📤 Upload a CSV file", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
        except UnicodeDecodeError:
            df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
            st.warning("Encoding issue detected. Loaded with fallback encoding (ISO-8859-1).")

        st.subheader("👁️ Preview Original CSV")
        st.dataframe(df.head())

        st.subheader("🧹 Cleaning Options")

        if st.button("Clean CSV"):
            cleaned_df = clean_csv(df)
            st.success("CSV cleaned successfully!")

            st.subheader("🔍 Preview Cleaned CSV")
            st.dataframe(cleaned_df.head())

            with st.expander("✏️ Rename Columns"):
                rename_cols = {}
                for col in cleaned_df.columns:
                    new_name = st.text_input(f"Rename '{col}'", value=col)
                    rename_cols[col] = new_name
                cleaned_df.rename(columns=rename_cols, inplace=True)

            csv_buffer = io.StringIO()
            cleaned_df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue().encode("utf-8")

            st.download_button(
                label="⬇️ Download Cleaned CSV",
                data=csv_data,
                file_name="cleaned_shopify_csv.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()