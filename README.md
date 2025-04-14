Estrutura básica do projeto.

Inicialmente construído para estudos, foi desenvolvido como um sistema de cálculo de frete com interface gráfica, feito em Python + Tkinter, utilizando:
Distância real via OpenStreetMap (Nominatim + OSRM)
Cálculo de combustível com consumo médio e preço do dia
Simulação de pedágios
Lucro customizado
Armazenamento dos fretes no SQLite (frete.db)
Calculadora de Frete - Python + Tkinter
Projeto desenvolvido em Python com interface gráfica para que calcula o frete de maneira simples e funcional, simulando trajetos reais entre endereços.

Funcionalidades
Com uma Interface amigável e campos para preenchimento:

- Origem e destino (endereços completos)
- Tipo de combustível (Gasolina, Álcool, Diesel, Gás)
- Consumo médio do veículo (km/l)
- Valor do combustível atual
- Lucro desejado no frete

Cálculo automático:
Distância real entre endereços via [OpenStreetMap + OSRM](https://project-osrm.org/)

- Consumo total em litros
- Custo estimado com combustível
- Valor simulado de pedágios
- Lucro e valor total final.

Banco de dados local:
Utiliza SQLite para armazenar cada frete calculado
Tabela: CADASTRO_FRETE

Tecnologias utilizadas

- Python
- Tkinter (interface gráfica)
- SQLite3 (banco de dados local)
- Requests (requisições HTTP)
- OpenStreetMap (via Nominatim + OSRM)

Como usar:
Clone o repositório:
Instale a dependência necessária:
pip install requests
Execute o projeto:
python main.py
Preencha os campos e clique em "Calcular Frete"

Observações.:
A distância é obtida automaticamente usando o sistema de rotas públicas da
OSRM. Caso não esteja disponível no momento, um valor padrão será usado.
Pedágios ainda são simulados, mas o sistema está preparado para incluir
integração futura com APIs de pedágios reais.

Desenvolvido por Alexandre Santos
Contato alexandre.zero11@gmail.com

Futuras melhorias
Tela de histórico de fretes
Exportação para PDF ou Excel
Integração com dados reais de pedágios
Modo Web com Flask ou FastAPI
Autenticação de usuários.
