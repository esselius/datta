load('ext://namespace', 'namespace_create')

def kustomize_enable_helm(path):
  watch_file(path)
  return local("kustomize build --enable-helm %s" % path, quiet=True)

namespace_create('strimzi')
k8s_yaml(kustomize_enable_helm('k8s/strimzi'))

namespace_create('kafka')
k8s_yaml(kustomize_enable_helm('k8s/kafka'))
k8s_kind('KafkaConnect$', image_json_path='{.spec.image}')
docker_build('kafka-connect', 'docker/kafka-connect')

namespace_create('postgres-operator')
k8s_yaml(kustomize('k8s/postgres-operator'))

namespace_create('postgres')
k8s_yaml(kustomize('k8s/postgres'))

k8s_yaml(kustomize('k8s/kafka-connector'))

namespace_create('minio-operator')
k8s_yaml(kustomize_enable_helm('k8s/minio-operator'))

namespace_create('minio')
k8s_yaml(kustomize('k8s/minio'))

namespace_create('hive')
k8s_yaml(kustomize_enable_helm('k8s/hive'))

namespace_create('spark-operator')
k8s_yaml(kustomize_enable_helm('k8s/spark-operator'))

namespace_create('spark')
k8s_yaml(kustomize('k8s/spark'))
k8s_kind('SparkApplication', image_json_path='{.spec.image}')
docker_build('spark-job', 'docker/spark-job')

namespace_create('starrocks-operator')
k8s_yaml(kustomize('k8s/starrocks-operator'))

namespace_create('starrocks')
k8s_yaml(kustomize('k8s/starrocks'))
