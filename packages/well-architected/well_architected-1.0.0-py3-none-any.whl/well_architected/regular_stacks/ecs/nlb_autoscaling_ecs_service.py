import aws_cdk
import constructs
import regular_constructs.autoscaling_ecs



class NlbAutoscalingEcsService(well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        container_image=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, *kwargs)

        autoscaling_ecs_cluster = regular_constructs.autoscaling_ecs.AutoscalingEcsCluster(
            self, 'AutoscalingEcs',
        )

        ecs_service = self.create_ecs_service(
            ecs_cluster=autoscaling_ecs_cluster.ecs_cluster,
            task_image_options=self.get_task_image_options(container_image)
        )

        aws_cdk.CfnOutput(
            self, "LoadBalancerDNS",
            value=ecs_service.load_balancer.load_balancer_dns_name
        )

    def get_task_image_options(self, container_image):
        return aws_cdk.aws_ecs_patterns.NetworkLoadBalancedTaskImageOptions(
            image=aws_cdk.aws_ecs.ContainerImage.from_registry(
                container_image
            )
        )

    def create_ecs_service(self, ecs_cluster=None, task_image_options=None):
        return aws_cdk.aws_ecs_patterns.NetworkLoadBalancedEc2Service(
            self, "Ec2Service",
            cluster=ecs_cluster,
            memory_limit_mib=512,
            task_image_options=task_image_options,
        )