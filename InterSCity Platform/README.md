# Deploy InterScity

Install kubectl
Install e start minikube
https://minikube.sigs.k8s.io/docs/start/

1 - criar namespace
kubectl create namespace interscity


Aplicar
2 - kubectl apply -f 0\ -\ Persistence/


verificar persistencia
3 - kubectl get pvc -n interscity


4 - kubectl apply -f 1\ -Postgres/


5 - kubectl get pods -n interscity

6 - kubectl apply -f 2\ -\ Third\ Party\ Service/

// delete o migrate após o kong subir
7 - kubectl delete -f 2\ -\ Third\ Party\ Service/kong-migration-pod.yaml  

8 -  kubectl apply -f 3\ -\ Interscity/

9 - kubectl get pods -n interscity

OBS: em erro de baixar imagens baixe diretamente via docker pull

docker login registry.lsdi.ufma.br

aluno
public@c@o

docker pull registry.lsdi.ufma.br/interscity/data-collector:fix-1
docker pull registry.lsdi.ufma.br/interscity/resource-discovery:0.0.2

Delete o seriço tagger (se não for usar)
10 - kubectl delete -f 3\ -\ Interscity/tagger-deploy.yaml

10 - kubectl get svc -n interscity

11 - minikube -n interscity service kong-service --url
(Irá gerar duas url para o Kong)
Para testar:

curl http://{url}/upstreams 
curl http://{url}/collector/resources/data


##################

Demais comandos (não precisa executar):

eval $(minikube docker-env)

kubectl delete -f 3\ -\ Interscity/data-collector-deploy.yaml

kubectl delete -R -f .

kubectl get pods -n interscity --watch