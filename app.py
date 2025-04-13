
import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Futbol AI Tahmin Botu", layout="centered")
st.title("⚽ Futbol AI Tahmin Botu")
st.markdown("Tahmini oran: 1.65 - 1.85 | Kazanma ihtimali: %70+")

@st.cache_data(show_spinner=True)
def fetch_matches():
    url = "https://www.forebet.com/en/football-predictions"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    matches = []
    for row in soup.select(".rcnt .tr_0, .rcnt .tr_1"):
        try:
            teams = row.select_one(".homeTeam").text.strip() + " vs " + row.select_one(".awayTeam").text.strip()
            prediction = row.select_one(".ptext2").text.strip()
            odds = float(row.select_one(".odds_1X2_cell span.odds_bg1").text.strip())
            probability = int(row.select_one(".prob2").text.strip().replace("%", ""))

            if 1.65 <= odds <= 1.85 and probability >= 70:
                matches.append({
                    "match": teams,
                    "prediction": prediction,
                    "odds": odds,
                    "win_chance": probability
                })
        except Exception:
            continue

    return matches

if st.button("⚡ Tahminleri Getir"):
    with st.spinner("Yapay zekâ analiz ediyor..."):
        results = fetch_matches()

    if results:
        st.success(f"Toplam {len(results)} uygun maç bulundu.")
        for match in results:
            st.markdown(f"**Maç:** {match['match']}")
            st.markdown(f"👉 Tahmin: `{match['prediction']}`")
            st.markdown(f"💸 Oran: `{match['odds']}`")
            st.markdown(f"📈 Kazanma Şansı: `%{match['win_chance']}`")
            st.markdown("---")
    else:
        st.warning("Uygun maç bulunamadı ya da siteye erişilemedi.")
