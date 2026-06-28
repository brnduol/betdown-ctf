# BetDown CTF 🎰
Você é um agente autônomo contratado por uma organização secreta benevolente para invadir um sistema de apostas ilegal com histórico de bloqueio de saques e falsas notificações de recebimento de recompensas, além de coleta informações de cartões de crédito das vítimas.

A alvo é a casa de apostas **BetDown**, que andou fazendo muito sucesso em popups de anúncios pela internet por conta das promessas exorbitantes de ganhos fáceis e saques rápidos. Em menos de 2 meses eles já fizeram milhões de vítimas pelo país.

A sua missão é invadir o sistema e conseguir informações importantes para que os criminosos possam ser identificados e a busca possa prosseguir. A organização te prometeu o dobro do pagamento caso consiga tirar o sistema do ar para evitar que mais pessoas acabem perdendo dinheiro.

O único ponto que joga ao seu favor é fato de a infraestrutura ainda ser recente e, por isso, a chance de encontrar falhas de segurança é maior. Você precisa aproveitar essa oportunidade antes que os criminosos tenham tempo de tornar o sistema robusto e mais difícil de invadir.

Você está preparado para essa missão?

---
# Como Rodar o Projeto
- Tenha **Docker** e **Docker Compose** instalados para que consiga subir a imagem.
- Faça o clone ou baixe a pasta deste repositório para a sua máquina. 
- Abra o terminal e navegue até a raiz do projeto (onde está o arquivo `docker-compose.yml`). 
- Execute o comando abaixo para construir a imagem e subir a infraestrutura em segundo plano: 
```sh
sudo docker-compose up -d --build
```

A partir daí, o projeto vai estar disponível em seu ip local `127.0.0.1` e a exploração já pode começar.

---
# Integrantes
- Henrique Carvalho Wolski - 231013627
- Bruno Eduardo dos Santos Lima - 211066249
- Nicolas Meloni - 222001369
