### Trabalho 2 - Segurança Computacional

O trabalho deve contemplar

Parte I: Geração de chaves
- [x] Geração de chaves (p e q primos com no mínimo de 1024 bits)

Parte II: Cifra simétrica
- [x] Geração de chaves simétrica
- [x] Cifração simétrica de mensagem (AES modo CTR),

Parte III: Geração da assinatura
- [ ] Cálculo de hashes da mensagem em claro (função de hash SHA-3)
- [ ] Assinatura da mensagem (cifração do hash da mensagem usando OAEP)
- [ ] Formatação do resultado (caracteres especiais e informações para verificação em
BASE64)

Parte IV: Verificação:
- [ ] Parsing do documento assinado e decifração da mensagem (de acordo com a
formatação usada, no caso BASE64)
- [ ] Decifração da assinatura (decifração do hash)
- [ ] Verificação (cálculo e comparação do hash do arquivo)


A pontuação máxima será conferida aos trabalhos que realmente implementarem as 
seguintes primitivas: 
a.  geração de chaves com teste de primalidade (Miller-Rabin) 
b.  geração de chave e cifração AES 
c.  cifração e decifração RSA com OAEP 
d.  formatação/parsing 
e.  AES modo CTR 