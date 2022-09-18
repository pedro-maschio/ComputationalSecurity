# Sistema de Assinatura Digital RSA - AES | Segurança Computacional UnB

Este projeto é um gerador e verificador de assinaturas em arquivos feito em Python.

O programa segue os seguintes passos:
1. Um arquivo é lido e seu hash é calculado;
2. O arquivo é criptografado com AES CTR;
3. O hash e a chave do AES são criptografados com RSA OAEP;
4. São gerados arquivos contendo o arquivo criptografado, a chave do AES criptografada e o hash criptografado;
5. O arquivo, hash e chaves criptografados são lidos;
6. A chave do AES é lida e descriptografada com o RSA, depois essa chave é utilizada pra descriptografar o arquivo;
7. O hash do arquivo descriptografado é calculado e comparado com o hash descriptografado.

Durante a sua execução, o programa gera os seguintes arquivos:

1. *message.bin*: esse arquivo contém a mensagem cifrada pelo AES CTR;
2. *key.bin*: esse arquivo contém a chave AES criptografada pelo RSA
3. *hash.bin*: esse arquivo contém o Hash do arquivo cifrado

## Como executar
```
python main.py <nome_do_arquivo_a_ser_assinado>
```

Autores: Pedro Maschio (190018763) & Gabriel Martins (190013371)