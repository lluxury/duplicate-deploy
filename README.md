# duplicate-deploy

[TOC]

~~~bash
DEMO_HOME=$(mktemp -d)
DEMO_HOME=~/hello
BASE=$DEMO_HOME/base
mkdir -p $BASE
curl -s -o "$BASE/#1.yaml" "https://raw.githubusercontent.com\
/kubernetes-sigs/kustomize\
/master/examples/helloWorld\
/{configMap,deployment,kustomization,service}.yaml"
~~~

tree $DEMO_HOME
/home/yann/hello
└── base
    ├── configMap.yaml
    ├── deployment.yaml
    ├── kustomization.yaml
    └── service.yaml

#### first step follow example

~~~bash
kustomize build $BASE
sed -i.bak 's/app: hello/app: my-hello/' \
    $BASE/kustomization.yaml
kustomize build $BASE | grep -C 3 app:    
~~~

build and temporary modify build, work



~~~bash
OVERLAYS=$DEMO_HOME/overlays
mkdir -p $OVERLAYS/staging
mkdir -p $OVERLAYS/production
~~~

parallel with base



###### create template file

this step could be finish by snip

~~~bash
cat <<'EOF' >$OVERLAYS/staging/kustomization.yaml
namePrefix: staging-
commonLabels:
  variant: staging
  org: acmeCorporation
commonAnnotations:
  note: Hello, I am staging!
resources:
- ../../base
patches:
- path: map.yaml
EOF
~~~



~~~bash
cat <<EOF >$OVERLAYS/production/kustomization.yaml
namePrefix: production-
commonLabels:
  variant: production
  org: acmeCorporation
commonAnnotations:
  note: Hello, I am production!
resources:
- ../../base
patches:
- path: deployment.yaml
EOF
~~~



~~~bash
cat <<EOF >$OVERLAYS/production/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: the-deployment
spec:
  replicas: 10
EOF
~~~

location

~~~bash
tree $DEMO_HOME

├── base
│   ├── configMap.yaml
│   ├── deployment.yaml
│   ├── kustomization.yaml
│   ├── kustomization.yaml.bak
│   └── service.yaml
└── overlays
    ├── production
    │   ├── deployment.yaml
    │   └── kustomization.yaml
    └── staging
        ├── kustomization.yaml
        └── map.yaml

~~~



check yaml file

~~~bash
diff \
  <(kustomize build $OVERLAYS/staging) \
  <(kustomize build $OVERLAYS/production) |\
  more
~~~





~~~bash
kustomize build $OVERLAYS/staging
kustomize build $OVERLAYS/production

kustomize build $OVERLAYS/staging |\
    kubectl apply -f -

kustomize build $OVERLAYS/production |\
   kubectl apply -f -
~~~

