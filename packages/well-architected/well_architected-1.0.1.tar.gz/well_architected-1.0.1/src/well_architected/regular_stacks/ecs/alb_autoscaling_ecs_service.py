import aws_cdk
import constructs

import regular_constructs.autoscaling_ecs


class AlbAutoscalingEcsService(well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        container_image=None,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        autoscaling_ecs_cluster = regular_constructs.autoscaling_ecs.AutoscalingEcsCluster(
            self, 'AutoscalingEcs',
        )
        aws_cdk.CfnOutput(
            self, "LoadBalancerDNS",
            value=self.get_application_load_balancer_dns_name(
                vpc=autoscaling_ecs_cluster.vpc,
                service=autoscaling_ecs_cluster.create_ecs_service(
                    container_image=container_image,
                ),
            )
        )

    @staticmethod
    def container_port():
        return 80

    def create_application_load_balancer(self, vpc):
        return aws_cdk.aws_elasticloadbalancingv2.ApplicationLoadBalancer(
            self, "ApplicationLoadBalancer",
            vpc=vpc,
            internet_facing=True
        )

    def get_application_load_balancer_dns_name(self, vpc=None, service=None):
        application_load_balancer = self.create_application_load_balancer(vpc)
        application_load_balancer.add_listener(
            "PublicListener",
            port=self.container_port(),
            open=True
        ).add_targets(
            "Targets",
            port=self.container_port(),
            targets=[service],
            health_check=self.create_health_check(),
        )
        return application_load_balancer.load_balancer_dns_name

    @staticmethod
    def create_health_check():
        return aws_cdk.aws_elasticloadbalancingv2.HealthCheck(
            interval=aws_cdk.Duration.seconds(60),
            path="/health",
            timeout=aws_cdk.Duration.seconds(5)
        )