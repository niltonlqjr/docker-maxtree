# A instalação do docker é feita pelo tutorial disponivel no site de documentação do proprio docker:
# https://docs.docker.com/engine/install/debian/
#instalar pacotes necessários para as chaves GPG do docker
sudo apt-get update
sudo apt-get install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
#Adicionar o repositorio no gerenciador de pacotes APT
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" |   sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
#Atualizar o gerenciador de pacotes com o novo repositorio
sudo apt-get update
#instalar os componentes necessarios para o docker
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
#para que o usuario possa executar os containers sem alterar a permissão do arquivo /var/run/docker.sock
#adicionar o usuário no grupo docker
sudo usermod -a -G docker manut
#testar o docker com o container hello-world e remover o container apos sua execucao
docker run --rm hello-world
