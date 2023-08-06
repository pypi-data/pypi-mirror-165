import constructs
import regular_constructs.autoscaling_ecs



class AutoscalingEcsCluster(well_architected_stack.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        regular_constructs.autoscaling_ecs.AutoscalingEcsCluster(
            self, 'AutoscalingEcs',
        )