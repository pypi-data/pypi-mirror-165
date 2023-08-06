import aws_cdk
import constructs


class AutoscalingEcsCluster(constructs.Construct):

    def __init__(
        self, scope: constructs.Construct, id: str,
        vpc=None,
        autoscaling_group=None,
        create_autoscaling_group_provider=True,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)
        self.vpc = self.get_vpc(vpc)
        self.ecs_cluster = self.create_ecs_cluster(self.vpc)
        if create_autoscaling_group_provider:
            self.create_autoscaling_group_provider(autoscaling_group)

    def get_vpc(self, vpc=None):
        if vpc:
            return vpc
        else:
            return aws_cdk.aws_ec2.Vpc(
                self, 'Vpc',
                max_azs=2,
            )

    def create_ecs_cluster(self, vpc):
        return aws_cdk.aws_ecs.Cluster(
            self, 'EcsCluster',
            vpc=vpc
        )

    def create_autoscaling_group(self):
        return aws_cdk.aws_autoscaling.AutoScalingGroup(
            self, "AutoScalingGroup",
            instance_type=aws_cdk.aws_ec2.InstanceType("t2.micro"),
            machine_image=aws_cdk.aws_ecs.EcsOptimizedImage.amazon_linux2(),
            vpc=self.vpc,
        )

    def create_autoscaling_group_provider(self, autoscaling_group=None):
        self.ecs_cluster.add_asg_capacity_provider(
            aws_cdk.aws_ecs.AsgCapacityProvider(
                self, "AsgCapacityProvider",
                auto_scaling_group=autoscaling_group if autoscaling_group else self.create_autoscaling_group()
            )
        )

    def create_ecs_service(
        self, security_group=None,
        network_mode=None, container_image=None,
        placement_constraints=None,
    ):
        return aws_cdk.aws_ecs.Ec2Service(
            self, "Service",
            cluster=self.ecs_cluster,
            task_definition=self.create_task_definition(
                network_mode=network_mode,
                container_image=container_image,
            ),
            security_groups=[security_group] if security_group else None,
            placement_constraints=placement_constraints,
        )

    def create_task_definition(self, network_mode=None, container_image=None):
        task_definition = aws_cdk.aws_ecs.Ec2TaskDefinition(
            self, "TaskDefinition",
            network_mode=network_mode
        )
        self.create_container(
            task_definition=task_definition,
            container_image=container_image,
        )
        return task_definition

    @staticmethod
    def get_port_mappings():
        return aws_cdk.aws_ecs.PortMapping(
            container_port=80,
            protocol=aws_cdk.aws_ecs.Protocol.TCP
        )

    def create_container(self, task_definition=None, container_image=None):
        task_definition.add_container(
            "Container",
            image=aws_cdk.aws_ecs.ContainerImage.from_registry(container_image),
            cpu=100,
            memory_limit_mib=256,
            essential=True,
        ).add_port_mappings(
            self.get_port_mappings()
        )