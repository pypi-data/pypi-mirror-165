
from typing import List, Optional

from promoted_python_delivery_client.client.delivery_request import DeliveryRequest
from promoted_python_delivery_client.model.cohort_membership import CohortMembership
from promoted_python_delivery_client.model.request import Request


class DeliveryRequestValidator():
    def validate(self, request: DeliveryRequest, is_shadow_traffic: bool) -> List[str]:
        validation_errors: List[str] = []

        req = request.request
        if req is None:
            return ["Request must be set"]

        # Check the ids.
        validation_errors.extend(self.validate_ids(request.request, request.experiment))

        # Insertion start should be >= 0
        if request.insertion_start < 0:
            validation_errors.append("Insertion start must be greater or equal to 0")

        return validation_errors

    def validate_ids(self, request: Request, experiment: Optional[CohortMembership]) -> List[str]:
        validation_errors: List[str] = []

        if request.request_id:
            validation_errors.append("Request.requestId should not be set")

        if request.user_info is None:
            validation_errors.append("Request.userInfo should be set")
        elif not request.user_info.log_user_id:
            validation_errors.append("Request.userInfo.logUserId should be set")

        if request.insertion is None:
            validation_errors.append("Request.insertion should be set")
        else:
            for ins in request.insertion:
                if ins.insertion_id:
                    validation_errors.append("Insertion.insertionId should not be set")
                if not ins.content_id:
                    validation_errors.append("Insertion.contentId should be set")

        return validation_errors
