# -----------------------------
# NIFTY Option Chain Visualization
# -----------------------------
if index_option == "NIFTY 50":
    st.subheader(f"NIFTY Option Chain for Expiry: {expiry}")
    try:
        option_chain = nse_optionchain_scrapper('NIFTY', expiry)
        ce_data = pd.DataFrame(option_chain.get('CE', []))
        pe_data = pd.DataFrame(option_chain.get('PE', []))

        if not ce_data.empty and not pe_data.empty:
            # Interactive Plot: Strike Price vs Open Interest
            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=ce_data['strikePrice'],
                y=ce_data['openInterest'],
                name='Call OI',
                marker_color='green',
                opacity=0.7
            ))

            fig.add_trace(go.Bar(
                x=pe_data['strikePrice'],
                y=pe_data['openInterest'],
                name='Put OI',
                marker_color='red',
                opacity=0.7
            ))

            fig.update_layout(
                title=f"NIFTY Options Open Interest (Expiry: {expiry})",
                xaxis_title="Strike Price",
                yaxis_title="Open Interest",
                barmode='group',
                template="plotly_dark"
            )

            st.plotly_chart(fig, use_container_width=True)

            # Optional: show top 10 CE and PE data tables
            st.markdown("**Top 10 Call Options (CE)**")
            st.dataframe(ce_data.head(10))
            st.markdown("**Top 10 Put Options (PE)**")
            st.dataframe(pe_data.head(10))

        else:
            st.info("Option chain data not available.")

    except Exception as e:
        st.warning(f"Could not fetch NIFTY option chain: {e}")
