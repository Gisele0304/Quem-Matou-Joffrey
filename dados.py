suspeitos = [
    {
        "codigo": "S1",
        "nome": "Tyrion Lannister",
        "relacao": "Tio da vítima",
        "motivo": "Humilhações públicas e rivalidade familiar"

    },
    {
            "codigo": "S2",
            "nome": "Sansa Stark",
            "relacao": "Antiga prometida da vítima",
            "motivo": "Sofria maus-tratos, desejo de vingança pela morte de seu pai"
    
    },
    {
            "codigo": "S3",
            "nome": "Petyr Baelish (Mindinho)",
            "relacao": "Conselheiro da vítima",
            "motivo": "Ambição de poder e interesses políticos"
    
    },
    {
            "codigo": "S4",
            "nome": "Olenna Tyrell",
            "relacao": "Avó da esposa da vítima",
            "motivo": "Proteger os interesses de sua família e sua neta"
    
    },
    {
            "codigo": "S5",
            "nome": "Margaery Tyrell",
            "relacao": "Esposa da vítima",
            "motivo": "Proteger os interesses de sua família e sua própria posição"
    
    },
    {
        "codigo": "S6",
        "nome": "Dontos Hollard",
        "relacao": "Bobo da corte",
        "motivo": "Participação na fuga de Sansa"
    }
]

vitima = {
    "codigo": "V1",
    "nome": "Joffrey Baratheon",
    "cargo": "Rei dos Sete Reinos",
    "causa_morte": "Envenenamento",
    "local": "Fortaleza Vermelha",
    "evento": "Casamento Púrpura"
}

evidencias = [
    {
        "codigo": "E1",
        "nome": "Taça de Joffrey",
        "tipo": "Objeto",
        "descricao": "Taça utilizada pelo rei durante o banquete.",
        "local": "Salão Principal",
        "importancia": "Alta"
    },
    {
        "codigo": "E2",
        "nome": "Rede de cabelo de Sansa",
        "tipo": "Objeto",
        "descricao": "Acessório utilizado por Sansa durante o casamento.",
        "local": "Salão Principal",
        "importancia": "Alta"
    },
    {
        "codigo": "E3",
        "nome": "Vinho do casamento",
        "tipo": "Substância",
        "descricao": "Vinho servido durante a celebração.",
        "local": "Salão Principal",
        "importancia": "Alta"
    },
    {
        "codigo": "E4",
        "nome": "Torta do casamento",
        "tipo": "Alimento",
        "descricao": "Alimento servido durante o banquete.",
        "local": "Salão Principal",
        "importancia": "Média"
    },
    {
        "codigo": "E5",
        "nome": "Depoimento dos convidados",
        "tipo": "Depoimento",
        "descricao": "Relatos das pessoas presentes durante o casamento.",
        "local": "Salão Principal",
        "importancia": "Média"
    },
    {
        "codigo": "E6",
        "nome": "Fuga de Sansa",
        "tipo": "Registro",
        "descricao": "Informações sobre a saída de Sansa da Fortaleza Vermelha.",
        "local": "Fortaleza Vermelha",
        "importancia": "Média"
    },
    {
        "codigo": "E7",
        "nome": "Comportamento dos convidados",
        "tipo": "Observação",
        "descricao": "Observações sobre as atitudes dos convidados durante o banquete.",
        "local": "Salão Principal",
        "importancia": "Baixa"
    }
]

print("Total de suspeitos:", len(suspeitos))
print("Total de evidências:", len(evidencias))

for evidencia in evidencias:
    print(evidencia["codigo"], evidencia["nome"])