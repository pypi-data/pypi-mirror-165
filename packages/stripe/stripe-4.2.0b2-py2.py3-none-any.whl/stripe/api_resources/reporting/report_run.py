# File generated from our OpenAPI spec
from __future__ import absolute_import, division, print_function

from stripe.api_resources.abstract import CreateableAPIResource
from stripe.api_resources.abstract import ListableAPIResource


class ReportRun(CreateableAPIResource, ListableAPIResource):
    """
    The Report Run object represents an instance of a report type generated with
    specific run parameters. Once the object is created, Stripe begins processing the report.
    When the report has finished running, it will give you a reference to a file
    where you can retrieve your results. For an overview, see
    [API Access to Reports](https://stripe.com/docs/reporting/statements/api).

    Note that certain report types can only be run based on your live-mode data (not test-mode
    data), and will error when queried without a [live-mode API key](https://stripe.com/docs/keys#test-live-modes).
    """

    OBJECT_NAME = "reporting.report_run"
