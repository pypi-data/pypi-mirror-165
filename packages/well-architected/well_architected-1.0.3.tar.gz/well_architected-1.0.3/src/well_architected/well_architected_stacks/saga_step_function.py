import aws_cdk
import constructs

import well_architected_constructs.api_lambda
import well_architected_constructs.dynamodb_table
import well_architected_constructs.lambda_function

import well_architected_stack

class SagaStepFunction(well_architected_stack.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bookings_record = well_architected_constructs.dynamodb_table.DynamodbTableConstruct(
            self, 'DynamodbTable',
            partition_key='booking_id',
            sort_key='booking_type',
            error_topic=self.error_topic,
        ).dynamodb_table

        flight_reservation_function = self.create_bookings_lambda_function(
            function_name='flights/reserve_flight',
            table=bookings_record,
            error_topic=self.error_topic,
        )
        flight_confirmation_function = self.create_bookings_lambda_function(
            function_name='flights/confirm_flight',
            table=bookings_record,
            error_topic=self.error_topic,
        )
        flight_cancellation_function = self.create_bookings_lambda_function(
            function_name='flights/cancel_flight',
            table=bookings_record,
            error_topic=self.error_topic,
        )

        hotel_reservation_function = self.create_bookings_lambda_function(
            function_name="hotels/reserve_hotel",
            table=bookings_record,
            error_topic=self.error_topic,
        )

        hotel_confirmation_function = self.create_bookings_lambda_function(
            function_name='hotels/confirm_hotel',
            table=bookings_record,
            error_topic=self.error_topic,
        )

        hotel_cancellation_function = self.create_bookings_lambda_function(
            function_name="hotels/cancel_hotel",
            table=bookings_record,
            error_topic=self.error_topic,
        )

        payment_processing_function = self.create_bookings_lambda_function(
            function_name="payments/process_payment",
            table=bookings_record,
            error_topic=self.error_topic,
        )

        payment_refund_function = self.create_bookings_lambda_function(
            function_name="payments/refund_payment",
            table=bookings_record,
            error_topic=self.error_topic,
        )

        '''
        Saga Step Function Follows a strict order:
        1) Reserve Flights and Hotel
        2) Take Payment
        3) Confirm Flight and Hotel booking
        '''

        # 1) Reserve Flights and Hotel
        cancel_hotel_reservation = self.create_cancellation_task(
            task_name='CancelHotelReservation',
            lambda_function=hotel_cancellation_function,
            next_step=aws_cdk.aws_stepfunctions.Fail(
                self, "Sorry, We Couldn't make the booking"
            )
        )

        cancel_flight_reservation = self.create_cancellation_task(
            task_name='CancelFlightReservation',
            lambda_function=flight_cancellation_function,
            next_step=cancel_hotel_reservation,
        )

        refund_payment = self.create_cancellation_task(
            task_name='RefundPayment',
            lambda_function=payment_refund_function,
            next_step=cancel_flight_reservation
        )

        saga_state_machine = aws_cdk.aws_stepfunctions.StateMachine(
            self, 'StateMachine',
            definition=(
                aws_cdk.aws_stepfunctions.Chain
                    .start(
                        self.create_step_function_task_with_error_handler(
                            task_name='ReserveHotel',
                            lambda_function=hotel_reservation_function,
                            error_handler=cancel_hotel_reservation,
                        )
                    )
                    .next(
                        self.create_step_function_task_with_error_handler(
                            task_name='ReserveFlight',
                            lambda_function=flight_reservation_function,
                            error_handler=cancel_flight_reservation,
                        )
                    )
                    .next(
                        self.create_step_function_task_with_error_handler(
                            task_name='TakePayment',
                            lambda_function=payment_processing_function,
                            error_handler=refund_payment,
                        )
                    )
                    .next(
                        self.create_step_function_task_with_error_handler(
                            task_name='ConfirmHotelBooking',
                            lambda_function=hotel_confirmation_function,
                            error_handler=refund_payment,
                        )
                    )
                    .next(
                        self.create_step_function_task_with_error_handler(
                            task_name='ConfirmFlight',
                            lambda_function=flight_confirmation_function,
                            error_handler=refund_payment,
                        )
                    )
                    .next(
                        aws_cdk.aws_stepfunctions.Succeed(
                            self, 'We have made your booking!'
                        )
                    )
            ),
            timeout=aws_cdk.Duration.minutes(5)
        )

        saga_lambda = self.create_lambda_function(
            error_topic=self.error_topic,
            function_name='saga_lambda',
            environment_variables={
                'statemachine_arn': saga_state_machine.state_machine_arn
            },
        )

        saga_state_machine.grant_start_execution(saga_lambda)

        well_architected_constructs.api_lambda.create_rest_api_lambda(
            self,
            error_topic=self.error_topic,
            lambda_function=saga_lambda
        )
        well_architected_constructs.api_lambda.create_http_api_lambda(
            self,
            error_topic=self.error_topic,
            lambda_function=saga_lambda
        )

    def create_stepfunctions_task(
        self, task_name=None, lambda_function=None
    ):
        return aws_cdk.aws_stepfunctions_tasks.LambdaInvoke(
            self, task_name,
            lambda_function=lambda_function,
            result_path=f'$.{task_name}Result'
        )

    def create_cancellation_task(
        self, task_name=None, lambda_function=None, next_step=None
    ):
        return self.create_stepfunctions_task(
            task_name=task_name,
            lambda_function=lambda_function,
        ).add_retry(
            max_attempts=3
        ).next(
            next_step
        )

    def create_step_function_task_with_error_handler(
        self, task_name=None, lambda_function=None, error_handler=None
    ):
        return self.create_stepfunctions_task(
            task_name=task_name,
            lambda_function=lambda_function,
        ).add_catch(
            error_handler,
            result_path=f"$.{task_name}Error"
        )

    def create_lambda_function(
        self, function_name=None, environment_variables=None,
        error_topic=None,
    ):
        return well_architected_constructs.lambda_function.LambdaFunctionConstruct(
            self, function_name,
            function_name=function_name,
            error_topic=error_topic,
            environment_variables=environment_variables,
        ).lambda_function

    def create_bookings_lambda_function(
        self, table: aws_cdk.aws_dynamodb.Table=None,
        function_name=None, error_topic=None
    ):
        function = self.create_lambda_function(
            function_name=function_name,
            error_topic=error_topic,
            environment_variables={
                'TABLE_NAME': table.table_name
            }
        )
        table.grant_read_write_data(function)
        return function