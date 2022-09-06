### Trabalho 2 - Segurança Computacional

O trabalho deve contemplar

Parte I: Geração de chaves
- [x] Geração de chaves (p e q primos com no mínimo de 1024 bits)

Parte II: Cifra simétrica
- [ ] Geração de chaves simétrica
- [ ] Cifração simétrica de mensagem (AES modo CTR),

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