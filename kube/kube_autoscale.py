#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Project : docker-dashboard
# @Time    : 2018/10/28 11:02 AM
# @Author  : zhangchengcheng
# @FileName: kube_autoscale.py
# @Github  : https://github.com/sweetcczhang
"""

from kube import basic
from kubernetes.client.rest import ApiException
import kubernetes
from datetime import datetime
import pytz


class AutoScale(basic.Client):

    def create_auto_scale(self, namespace, name, labels, deploy_name, min_replicas, max_replicas, metrics):

        body = {
            'apiVersion': 'autoscaling/v2beta2',
            'kind': 'HorizontalPodAutoscaler',
            'metadata': {
                'name': name,
                'labels': labels
            },
            'spec': {
                'scaleTargetRef': {
                    'apiVersion': 'v1',
                    'kind': 'Deployment',
                    'name': deploy_name
                },
                'minReplicas': min_replicas,
                'maxReplicas': max_replicas,
                'metrics': metrics
            }
        }
        try:
            result = self.auto_client.create_namespaced_horizontal_pod_autoscaler(namespace=namespace, body=body)
            return result
        except ApiException as e:
            print("Exception when calling AutoscalingV1Api->create_namespaced_horizontal_pod_autoscaler: %s\n" % e)
            return None

    def list_auto_scaling(self, namespace=None):
        lists = []
        try:
            if namespace is None:
                api_response = self.auto_client.list_horizontal_pod_autoscaler_for_all_namespaces().items
            else:
                api_response = self.auto_client.list_namespaced_horizontal_pod_autoscaler(namespace=namespace).items
            for api in api_response:
                create_time = api.metadata.creation_timestamp
                now_time = datetime.utcnow().replace(tzinfo=pytz.timezone("UTC"))
                days = (now_time - create_time).days
                create_time = str(create_time)
                create_time = create_time[:len(create_time) - 6]
                name = api.metadata.name
                min_replicas = api.spec.min_replicas
                max_replicas = api.spec.max_replicas
                kind = api.spec.scale_target_ref.kind
                names = api.spec.scale_target_ref.name
                target = kind + '/' + names
                current_replicas = api.status.current_replicas
                temp = {'name': name, 'days': days, 'createTime': create_time, 'minReplicas': min_replicas,
                        'maxReplicas': max_replicas, 'target': target, 'CurrentReplicas': current_replicas}
                lists.append(temp)
            print (api_response)
        except ApiException as e:
            print("Exception when calling AutoscalingV1Api->list_horizontal_pod_autoscaler_for_all_namespaces: %s\n" % e)
        return len(lists), lists

    def delete_auto_scaling(self, name, namespace):
        """
        删除指定的auto scaling
        :param name:
        :param namespace:
        :return:
        """
        result = False
        try:
            body = kubernetes.client.V1DeleteOptions(propagation_policy='Foreground', grace_period_seconds=5)
            self.auto_client.delete_namespaced_horizontal_pod_autoscaler(name=name, namespace=namespace, body=body)
            result = True

        except ApiException as e:
            print e
        return result


if __name__ == '__main__':
    auto = AutoScale()
    auto.list_auto_scaling()
