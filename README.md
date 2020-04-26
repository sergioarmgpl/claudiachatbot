# Service Mesh and Serverless Chatbots with Linkerd, K8s and OpenFaaS - Lab

## Kubernetes Cluster Creation
1. Create a Digital Ocean k8s cluster
2. Instalar Kubectl
```
curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
```

# Installing OpenFaaS
## Helm Installation and configuration
Download and install helm
```
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```
Adding some useful charts to helm
```
helm repo add stable https://kubernetes-charts.storage.googleapis.com/
```
Adding OpenFaaS Helm Chart
```
helm repo add openfaas https://openfaas.github.io/faas-netes/
```
Some useful OpenFaaS documentation:
- Source: https://docs.openfaas.com/deployment/kubernetes/
Chart
- Readme: https://github.com/openfaas/faas-netes/blob/master/chart/openfaas/README.md
- Helm readme: https://github.com/openfaas/faas-netes/blob/master/HELM.md
- Detail: https://github.com/openfaas/faas-netes/blob/master/chart/openfaas/README.md
Creating OpenFaaS Namespace:
```
kubectl create ns openfaas 
```
Installing nginx-ingress to give public access to openfaas
```
helm install nginx-ingress --namespace openfaas stable/nginx-ingress
```
Creating default user and password login
```
kubectl -n openfaas create secret generic basic-auth --from-literal=basic-auth-password=kubeconeu123 --from-literal=basic-auth-user=admin
```
## Create values.yaml file
```
async: "false"
basic_auth: "false"
faasIdler: 
  dryRun: "false"
  inactivityDuration: "1m"
gateway: 
  readTimeout: "900s"
  replicas: "2"
  upstreamTimeout: "800s"
  writeTimeout: "900s"
queueWorker: 
  replicas: "2"    
functionNamespace: "openfaas"
```
# Suggested installation
```
helm install openfaas --namespace openfaas openfaas/openfaas -f values.yaml
```

## test just dry-run(optional)
```
helm install openfaas --namespace openfaas openfaas/openfaas -f values.yaml --dry-run    
```
## Check deployment
```
kubectl -n openfaas get deployments -l "release=openfaas, app=openfaas"
```
## Create ingress rule with nginx-ingress to expose OpenFaaS
```
kubectl create -f public-openfaas.yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.class: nginx
  name: public-openfaas
  namespace: openfaas
spec:
  rules:
    - host: openfaas.curzona.net
      http:
        paths:
          - backend:
              serviceName: gateway
              servicePort: 8080
            path: /
  # Optional section if you are using TLS
  tls:
      - hosts:
          - openfaas.curzona.net
        secretName: openfaas-cert
```

## Installing faas cli
```
curl -sSL https://cli.openfaas.com | sudo sh
```
## login to OpenFaaS via CLI
```
faas-cli login --username admin --password kubeconeu123 --gateway openfaas.curzona.net 
```
## OpenFaaS Logout
```
faas-cli logout --gateway openfaas.curzona.net
```
Note: use the option --tls-no-verify for self signed certifies

# Linkerd installation
Steps
```
curl -sL https://run.linkerd.io/install | sh
```
Add the following line to ~/.profile
```
export PATH=$PATH:$HOME/.linkerd2/bin
```
Run .profile to load the updated PATH
```
. ~/.profile
```
Check the version of linkerd cli
```
linkerd version
```
Pre-check before linkerd installation, look if there is not another installation
```
linkerd check --pre
```
Install Linkerd

