import aws_cdk
import constructs
import regular_constructs.autoscaling_ecs




class NlbAutoscalingFargateService(well_architected_stack.Stack):

    def __init__(self, scope: constructs.Construct, id: str,
        container_image=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        autoscaling_ecs_cluster = regular_constructs.autoscaling_ecs.AutoscalingEcsCluster(
            self, 'EcsCluster',
            create_autoscaling_group_provider=False
        )

        fargate_service = self.create_fargate_service(
            ecs_cluster=autoscaling_ecs_cluster.ecs_cluster,
            container_image=container_image,
        )

        self.add_security_group_ingress_rule(
            security_group=fargate_service.service.connections.security_groups[0],
            vpc_cidr_block=autoscaling_ecs_cluster.vpc.vpc_cidr_block,
        )

        fargate_service.service.auto_scale_task_count(
            max_capacity=2
        ).scale_on_cpu_utilization(
            "CpuScaling",
            target_utilization_percent=50,
            scale_in_cooldown=aws_cdk.Duration.seconds(60),
            scale_out_cooldown=aws_cdk.Duration.seconds(60),
        )

        aws_cdk.CfnOutput(
            self, "LoadBalancerDNS",
            value=fargate_service.load_balancer.load_balancer_dns_name
        )

    def create_fargate_service(self, ecs_cluster=None, container_image=None):
        return aws_cdk.aws_ecs_patterns.NetworkLoadBalancedFargateService(
            self, "EcsFargateService",
            cluster= ecs_cluster,
            task_image_options=aws_cdk.aws_ecs_patterns.NetworkLoadBalancedTaskImageOptions(
                image=aws_cdk.aws_ecs.ContainerImage.from_registry(container_image)
            )
        )

    def add_security_group_ingress_rule(self, vpc_cidr_block=None, security_group=None):
        return security_group.add_ingress_rule(
            peer = aws_cdk.aws_ec2.Peer.ipv4(vpc_cidr_block),
            connection = aws_cdk.aws_ec2.Port.tcp(80),
            description="Allow http inbound from VPC"
        )