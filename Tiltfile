load('ext://namespace', 'namespace_create')

def kustomize_enable_helm(path):
  watch_file(path)
  return local("kustomize build --enable-helm %s" % path, quiet=True)

namespace_create('strimzi')
k8s_yaml(kustomize_enable_helm('k8s/strimzi'))

namespace_create('kafka')
k8s_yaml(kustomize_enable_helm('k8s/kafka'))

namespace_create('postgres-operator')
k8s_yaml(kustomize_enable_helm('k8s/postgres-operator'))

namespace_create('postgres')
k8s_yaml(kustomize_enable_helm('k8s/postgres'))
