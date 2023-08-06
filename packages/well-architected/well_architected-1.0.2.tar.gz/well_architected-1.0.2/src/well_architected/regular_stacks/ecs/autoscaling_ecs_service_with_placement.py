import aws_cdk
import constructs
import regular_constructs.autoscaling_ecs



class AutoscalingEcsServiceWithPlacement(well_architected_stack.Stack):

    def __init__(self, scope: constructs.Construct, id: str,
        container_image=None,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        autoscaling_ecs_cluster = regular_constructs.autoscaling_ecs.AutoscalingEcsCluster(
            self, 'AutoscalingEcs',
        )
        ecs_service = autoscaling_ecs_cluster.create_ecs_service(
            container_image=container_image,
            placement_constraints=[
                aws_cdk.aws_ecs.PlacementConstraint.distinct_instances()
            ]
        )

        ecs_service.add_placement_strategies(
            aws_cdk.aws_ecs.PlacementStrategy.packed_by(
                aws_cdk.aws_ecs.BinPackResource.MEMORY
            )
        )
        ecs_service.add_placement_strategies(
            aws_cdk.aws_ecs.PlacementStrategy.spread_across(
                aws_cdk.aws_ecs.BuiltInAttributes.AVAILABILITY_ZONE
            )
        )