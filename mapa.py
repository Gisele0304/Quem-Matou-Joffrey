
import folium
from pathlib import Path
from dados import evidencias


def criar_mapa():

    coordenadas = {
        "Fortaleza Vermelha": [42.0000, 12.0000],
        "Salão Principal": [42.0010, 12.0010]
    }

    mapa = folium.Map(
        location=coordenadas["Fortaleza Vermelha"],
        zoom_start=16,
        tiles="OpenStreetMap"
    )

    for local, posicao in coordenadas.items():

        evidencias_local = [
            evidencia for evidencia in evidencias
            if evidencia["local"] == local
        ]

        descricao = f"<b>{local}</b><br><br>"

        if local == "Fortaleza Vermelha":
            descricao += "Local relacionado ao crime.<br><br>"

        if evidencias_local:

            descricao += "<b>Evidências:</b><br>"

            for evidencia in evidencias_local:
                descricao += (
                    f"{evidencia['codigo']} - "
                    f"{evidencia['nome']}<br>"
                )

        else:
            descricao += "Nenhuma evidência cadastrada."

        cor = "red" if local == "Fortaleza Vermelha" else "blue"

        folium.Marker(
            location=posicao,
            popup=folium.Popup(descricao, max_width=300),
            tooltip=local,
            icon=folium.Icon(
                color=cor,
                icon="info-sign"
            )
        ).add_to(mapa)

    arquivo = Path(__file__).with_name("mapa_investigacao.html")

    mapa.save(str(arquivo))

    return str(arquivo)


if __name__ == "__main__":

    arquivo = criar_mapa()

    print("Mapa criado:", arquivo)
