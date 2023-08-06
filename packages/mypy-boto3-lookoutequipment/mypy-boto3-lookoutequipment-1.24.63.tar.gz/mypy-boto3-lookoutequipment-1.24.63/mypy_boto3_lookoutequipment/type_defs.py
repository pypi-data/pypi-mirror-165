"""
Type annotations for lookoutequipment service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/type_defs/)

Usage::

    ```python
    from mypy_boto3_lookoutequipment.type_defs import CategoricalValuesTypeDef

    data: CategoricalValuesTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    DatasetStatusType,
    DataUploadFrequencyType,
    InferenceExecutionStatusType,
    InferenceSchedulerStatusType,
    IngestionJobStatusType,
    LabelRatingType,
    LatestInferenceResultType,
    ModelStatusType,
    MonotonicityType,
    StatisticalIssueStatusType,
    TargetSamplingRateType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "CategoricalValuesTypeDef",
    "CountPercentTypeDef",
    "DatasetSchemaTypeDef",
    "TagTypeDef",
    "ResponseMetadataTypeDef",
    "CreateLabelRequestRequestTypeDef",
    "DataPreProcessingConfigurationTypeDef",
    "DuplicateTimestampsTypeDef",
    "InvalidSensorDataTypeDef",
    "MissingSensorDataTypeDef",
    "UnsupportedTimestampsTypeDef",
    "DatasetSummaryTypeDef",
    "DeleteDatasetRequestRequestTypeDef",
    "DeleteInferenceSchedulerRequestRequestTypeDef",
    "DeleteLabelGroupRequestRequestTypeDef",
    "DeleteLabelRequestRequestTypeDef",
    "DeleteModelRequestRequestTypeDef",
    "DescribeDataIngestionJobRequestRequestTypeDef",
    "DescribeDatasetRequestRequestTypeDef",
    "DescribeInferenceSchedulerRequestRequestTypeDef",
    "DescribeLabelGroupRequestRequestTypeDef",
    "DescribeLabelRequestRequestTypeDef",
    "DescribeModelRequestRequestTypeDef",
    "InferenceEventSummaryTypeDef",
    "S3ObjectTypeDef",
    "InferenceInputNameConfigurationTypeDef",
    "InferenceS3InputConfigurationTypeDef",
    "InferenceS3OutputConfigurationTypeDef",
    "InferenceSchedulerSummaryTypeDef",
    "IngestionS3InputConfigurationTypeDef",
    "MissingCompleteSensorDataTypeDef",
    "SensorsWithShortDateRangeTypeDef",
    "LabelGroupSummaryTypeDef",
    "LabelSummaryTypeDef",
    "LabelsS3InputConfigurationTypeDef",
    "LargeTimestampGapsTypeDef",
    "ListDataIngestionJobsRequestRequestTypeDef",
    "ListDatasetsRequestRequestTypeDef",
    "ListInferenceEventsRequestRequestTypeDef",
    "ListInferenceExecutionsRequestRequestTypeDef",
    "ListInferenceSchedulersRequestRequestTypeDef",
    "ListLabelGroupsRequestRequestTypeDef",
    "ListLabelsRequestRequestTypeDef",
    "ListModelsRequestRequestTypeDef",
    "ModelSummaryTypeDef",
    "ListSensorStatisticsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "MonotonicValuesTypeDef",
    "MultipleOperatingModesTypeDef",
    "StartInferenceSchedulerRequestRequestTypeDef",
    "StopInferenceSchedulerRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateLabelGroupRequestRequestTypeDef",
    "CreateDatasetRequestRequestTypeDef",
    "CreateLabelGroupRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateDatasetResponseTypeDef",
    "CreateInferenceSchedulerResponseTypeDef",
    "CreateLabelGroupResponseTypeDef",
    "CreateLabelResponseTypeDef",
    "CreateModelResponseTypeDef",
    "DescribeLabelGroupResponseTypeDef",
    "DescribeLabelResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "StartDataIngestionJobResponseTypeDef",
    "StartInferenceSchedulerResponseTypeDef",
    "StopInferenceSchedulerResponseTypeDef",
    "ListDatasetsResponseTypeDef",
    "ListInferenceEventsResponseTypeDef",
    "IngestedFilesSummaryTypeDef",
    "InferenceInputConfigurationTypeDef",
    "InferenceOutputConfigurationTypeDef",
    "ListInferenceSchedulersResponseTypeDef",
    "IngestionInputConfigurationTypeDef",
    "InsufficientSensorDataTypeDef",
    "ListLabelGroupsResponseTypeDef",
    "ListLabelsResponseTypeDef",
    "LabelsInputConfigurationTypeDef",
    "ListModelsResponseTypeDef",
    "SensorStatisticsSummaryTypeDef",
    "CreateInferenceSchedulerRequestRequestTypeDef",
    "DescribeInferenceSchedulerResponseTypeDef",
    "InferenceExecutionSummaryTypeDef",
    "UpdateInferenceSchedulerRequestRequestTypeDef",
    "DataIngestionJobSummaryTypeDef",
    "StartDataIngestionJobRequestRequestTypeDef",
    "DataQualitySummaryTypeDef",
    "CreateModelRequestRequestTypeDef",
    "DescribeModelResponseTypeDef",
    "ListSensorStatisticsResponseTypeDef",
    "ListInferenceExecutionsResponseTypeDef",
    "ListDataIngestionJobsResponseTypeDef",
    "DescribeDataIngestionJobResponseTypeDef",
    "DescribeDatasetResponseTypeDef",
)

_RequiredCategoricalValuesTypeDef = TypedDict(
    "_RequiredCategoricalValuesTypeDef",
    {
        "Status": StatisticalIssueStatusType,
    },
)
_OptionalCategoricalValuesTypeDef = TypedDict(
    "_OptionalCategoricalValuesTypeDef",
    {
        "NumberOfCategory": int,
    },
    total=False,
)


class CategoricalValuesTypeDef(
    _RequiredCategoricalValuesTypeDef, _OptionalCategoricalValuesTypeDef
):
    pass


CountPercentTypeDef = TypedDict(
    "CountPercentTypeDef",
    {
        "Count": int,
        "Percentage": float,
    },
)

DatasetSchemaTypeDef = TypedDict(
    "DatasetSchemaTypeDef",
    {
        "InlineDataSchema": str,
    },
    total=False,
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

_RequiredCreateLabelRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLabelRequestRequestTypeDef",
    {
        "LabelGroupName": str,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "Rating": LabelRatingType,
        "ClientToken": str,
    },
)
_OptionalCreateLabelRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLabelRequestRequestTypeDef",
    {
        "FaultCode": str,
        "Notes": str,
        "Equipment": str,
    },
    total=False,
)


class CreateLabelRequestRequestTypeDef(
    _RequiredCreateLabelRequestRequestTypeDef, _OptionalCreateLabelRequestRequestTypeDef
):
    pass


DataPreProcessingConfigurationTypeDef = TypedDict(
    "DataPreProcessingConfigurationTypeDef",
    {
        "TargetSamplingRate": TargetSamplingRateType,
    },
    total=False,
)

DuplicateTimestampsTypeDef = TypedDict(
    "DuplicateTimestampsTypeDef",
    {
        "TotalNumberOfDuplicateTimestamps": int,
    },
)

InvalidSensorDataTypeDef = TypedDict(
    "InvalidSensorDataTypeDef",
    {
        "AffectedSensorCount": int,
        "TotalNumberOfInvalidValues": int,
    },
)

MissingSensorDataTypeDef = TypedDict(
    "MissingSensorDataTypeDef",
    {
        "AffectedSensorCount": int,
        "TotalNumberOfMissingValues": int,
    },
)

UnsupportedTimestampsTypeDef = TypedDict(
    "UnsupportedTimestampsTypeDef",
    {
        "TotalNumberOfUnsupportedTimestamps": int,
    },
)

DatasetSummaryTypeDef = TypedDict(
    "DatasetSummaryTypeDef",
    {
        "DatasetName": str,
        "DatasetArn": str,
        "Status": DatasetStatusType,
        "CreatedAt": datetime,
    },
    total=False,
)

DeleteDatasetRequestRequestTypeDef = TypedDict(
    "DeleteDatasetRequestRequestTypeDef",
    {
        "DatasetName": str,
    },
)

DeleteInferenceSchedulerRequestRequestTypeDef = TypedDict(
    "DeleteInferenceSchedulerRequestRequestTypeDef",
    {
        "InferenceSchedulerName": str,
    },
)

DeleteLabelGroupRequestRequestTypeDef = TypedDict(
    "DeleteLabelGroupRequestRequestTypeDef",
    {
        "LabelGroupName": str,
    },
)

DeleteLabelRequestRequestTypeDef = TypedDict(
    "DeleteLabelRequestRequestTypeDef",
    {
        "LabelGroupName": str,
        "LabelId": str,
    },
)

DeleteModelRequestRequestTypeDef = TypedDict(
    "DeleteModelRequestRequestTypeDef",
    {
        "ModelName": str,
    },
)

DescribeDataIngestionJobRequestRequestTypeDef = TypedDict(
    "DescribeDataIngestionJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

DescribeDatasetRequestRequestTypeDef = TypedDict(
    "DescribeDatasetRequestRequestTypeDef",
    {
        "DatasetName": str,
    },
)

DescribeInferenceSchedulerRequestRequestTypeDef = TypedDict(
    "DescribeInferenceSchedulerRequestRequestTypeDef",
    {
        "InferenceSchedulerName": str,
    },
)

DescribeLabelGroupRequestRequestTypeDef = TypedDict(
    "DescribeLabelGroupRequestRequestTypeDef",
    {
        "LabelGroupName": str,
    },
)

DescribeLabelRequestRequestTypeDef = TypedDict(
    "DescribeLabelRequestRequestTypeDef",
    {
        "LabelGroupName": str,
        "LabelId": str,
    },
)

DescribeModelRequestRequestTypeDef = TypedDict(
    "DescribeModelRequestRequestTypeDef",
    {
        "ModelName": str,
    },
)

InferenceEventSummaryTypeDef = TypedDict(
    "InferenceEventSummaryTypeDef",
    {
        "InferenceSchedulerArn": str,
        "InferenceSchedulerName": str,
        "EventStartTime": datetime,
        "EventEndTime": datetime,
        "Diagnostics": str,
        "EventDurationInSeconds": int,
    },
    total=False,
)

S3ObjectTypeDef = TypedDict(
    "S3ObjectTypeDef",
    {
        "Bucket": str,
        "Key": str,
    },
)

InferenceInputNameConfigurationTypeDef = TypedDict(
    "InferenceInputNameConfigurationTypeDef",
    {
        "TimestampFormat": str,
        "ComponentTimestampDelimiter": str,
    },
    total=False,
)

_RequiredInferenceS3InputConfigurationTypeDef = TypedDict(
    "_RequiredInferenceS3InputConfigurationTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalInferenceS3InputConfigurationTypeDef = TypedDict(
    "_OptionalInferenceS3InputConfigurationTypeDef",
    {
        "Prefix": str,
    },
    total=False,
)


class InferenceS3InputConfigurationTypeDef(
    _RequiredInferenceS3InputConfigurationTypeDef, _OptionalInferenceS3InputConfigurationTypeDef
):
    pass


_RequiredInferenceS3OutputConfigurationTypeDef = TypedDict(
    "_RequiredInferenceS3OutputConfigurationTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalInferenceS3OutputConfigurationTypeDef = TypedDict(
    "_OptionalInferenceS3OutputConfigurationTypeDef",
    {
        "Prefix": str,
    },
    total=False,
)


class InferenceS3OutputConfigurationTypeDef(
    _RequiredInferenceS3OutputConfigurationTypeDef, _OptionalInferenceS3OutputConfigurationTypeDef
):
    pass


InferenceSchedulerSummaryTypeDef = TypedDict(
    "InferenceSchedulerSummaryTypeDef",
    {
        "ModelName": str,
        "ModelArn": str,
        "InferenceSchedulerName": str,
        "InferenceSchedulerArn": str,
        "Status": InferenceSchedulerStatusType,
        "DataDelayOffsetInMinutes": int,
        "DataUploadFrequency": DataUploadFrequencyType,
        "LatestInferenceResult": LatestInferenceResultType,
    },
    total=False,
)

_RequiredIngestionS3InputConfigurationTypeDef = TypedDict(
    "_RequiredIngestionS3InputConfigurationTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalIngestionS3InputConfigurationTypeDef = TypedDict(
    "_OptionalIngestionS3InputConfigurationTypeDef",
    {
        "Prefix": str,
        "KeyPattern": str,
    },
    total=False,
)


class IngestionS3InputConfigurationTypeDef(
    _RequiredIngestionS3InputConfigurationTypeDef, _OptionalIngestionS3InputConfigurationTypeDef
):
    pass


MissingCompleteSensorDataTypeDef = TypedDict(
    "MissingCompleteSensorDataTypeDef",
    {
        "AffectedSensorCount": int,
    },
)

SensorsWithShortDateRangeTypeDef = TypedDict(
    "SensorsWithShortDateRangeTypeDef",
    {
        "AffectedSensorCount": int,
    },
)

LabelGroupSummaryTypeDef = TypedDict(
    "LabelGroupSummaryTypeDef",
    {
        "LabelGroupName": str,
        "LabelGroupArn": str,
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
    },
    total=False,
)

LabelSummaryTypeDef = TypedDict(
    "LabelSummaryTypeDef",
    {
        "LabelGroupName": str,
        "LabelId": str,
        "LabelGroupArn": str,
        "StartTime": datetime,
        "EndTime": datetime,
        "Rating": LabelRatingType,
        "FaultCode": str,
        "Equipment": str,
        "CreatedAt": datetime,
    },
    total=False,
)

_RequiredLabelsS3InputConfigurationTypeDef = TypedDict(
    "_RequiredLabelsS3InputConfigurationTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalLabelsS3InputConfigurationTypeDef = TypedDict(
    "_OptionalLabelsS3InputConfigurationTypeDef",
    {
        "Prefix": str,
    },
    total=False,
)


class LabelsS3InputConfigurationTypeDef(
    _RequiredLabelsS3InputConfigurationTypeDef, _OptionalLabelsS3InputConfigurationTypeDef
):
    pass


_RequiredLargeTimestampGapsTypeDef = TypedDict(
    "_RequiredLargeTimestampGapsTypeDef",
    {
        "Status": StatisticalIssueStatusType,
    },
)
_OptionalLargeTimestampGapsTypeDef = TypedDict(
    "_OptionalLargeTimestampGapsTypeDef",
    {
        "NumberOfLargeTimestampGaps": int,
        "MaxTimestampGapInDays": int,
    },
    total=False,
)


class LargeTimestampGapsTypeDef(
    _RequiredLargeTimestampGapsTypeDef, _OptionalLargeTimestampGapsTypeDef
):
    pass


ListDataIngestionJobsRequestRequestTypeDef = TypedDict(
    "ListDataIngestionJobsRequestRequestTypeDef",
    {
        "DatasetName": str,
        "NextToken": str,
        "MaxResults": int,
        "Status": IngestionJobStatusType,
    },
    total=False,
)

ListDatasetsRequestRequestTypeDef = TypedDict(
    "ListDatasetsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "DatasetNameBeginsWith": str,
    },
    total=False,
)

_RequiredListInferenceEventsRequestRequestTypeDef = TypedDict(
    "_RequiredListInferenceEventsRequestRequestTypeDef",
    {
        "InferenceSchedulerName": str,
        "IntervalStartTime": Union[datetime, str],
        "IntervalEndTime": Union[datetime, str],
    },
)
_OptionalListInferenceEventsRequestRequestTypeDef = TypedDict(
    "_OptionalListInferenceEventsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListInferenceEventsRequestRequestTypeDef(
    _RequiredListInferenceEventsRequestRequestTypeDef,
    _OptionalListInferenceEventsRequestRequestTypeDef,
):
    pass


_RequiredListInferenceExecutionsRequestRequestTypeDef = TypedDict(
    "_RequiredListInferenceExecutionsRequestRequestTypeDef",
    {
        "InferenceSchedulerName": str,
    },
)
_OptionalListInferenceExecutionsRequestRequestTypeDef = TypedDict(
    "_OptionalListInferenceExecutionsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "DataStartTimeAfter": Union[datetime, str],
        "DataEndTimeBefore": Union[datetime, str],
        "Status": InferenceExecutionStatusType,
    },
    total=False,
)


class ListInferenceExecutionsRequestRequestTypeDef(
    _RequiredListInferenceExecutionsRequestRequestTypeDef,
    _OptionalListInferenceExecutionsRequestRequestTypeDef,
):
    pass


ListInferenceSchedulersRequestRequestTypeDef = TypedDict(
    "ListInferenceSchedulersRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "InferenceSchedulerNameBeginsWith": str,
        "ModelName": str,
    },
    total=False,
)

ListLabelGroupsRequestRequestTypeDef = TypedDict(
    "ListLabelGroupsRequestRequestTypeDef",
    {
        "LabelGroupNameBeginsWith": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredListLabelsRequestRequestTypeDef = TypedDict(
    "_RequiredListLabelsRequestRequestTypeDef",
    {
        "LabelGroupName": str,
    },
)
_OptionalListLabelsRequestRequestTypeDef = TypedDict(
    "_OptionalListLabelsRequestRequestTypeDef",
    {
        "IntervalStartTime": Union[datetime, str],
        "IntervalEndTime": Union[datetime, str],
        "FaultCode": str,
        "Equipment": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListLabelsRequestRequestTypeDef(
    _RequiredListLabelsRequestRequestTypeDef, _OptionalListLabelsRequestRequestTypeDef
):
    pass


ListModelsRequestRequestTypeDef = TypedDict(
    "ListModelsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Status": ModelStatusType,
        "ModelNameBeginsWith": str,
        "DatasetNameBeginsWith": str,
    },
    total=False,
)

ModelSummaryTypeDef = TypedDict(
    "ModelSummaryTypeDef",
    {
        "ModelName": str,
        "ModelArn": str,
        "DatasetName": str,
        "DatasetArn": str,
        "Status": ModelStatusType,
        "CreatedAt": datetime,
    },
    total=False,
)

_RequiredListSensorStatisticsRequestRequestTypeDef = TypedDict(
    "_RequiredListSensorStatisticsRequestRequestTypeDef",
    {
        "DatasetName": str,
    },
)
_OptionalListSensorStatisticsRequestRequestTypeDef = TypedDict(
    "_OptionalListSensorStatisticsRequestRequestTypeDef",
    {
        "IngestionJobId": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListSensorStatisticsRequestRequestTypeDef(
    _RequiredListSensorStatisticsRequestRequestTypeDef,
    _OptionalListSensorStatisticsRequestRequestTypeDef,
):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

_RequiredMonotonicValuesTypeDef = TypedDict(
    "_RequiredMonotonicValuesTypeDef",
    {
        "Status": StatisticalIssueStatusType,
    },
)
_OptionalMonotonicValuesTypeDef = TypedDict(
    "_OptionalMonotonicValuesTypeDef",
    {
        "Monotonicity": MonotonicityType,
    },
    total=False,
)


class MonotonicValuesTypeDef(_RequiredMonotonicValuesTypeDef, _OptionalMonotonicValuesTypeDef):
    pass


MultipleOperatingModesTypeDef = TypedDict(
    "MultipleOperatingModesTypeDef",
    {
        "Status": StatisticalIssueStatusType,
    },
)

StartInferenceSchedulerRequestRequestTypeDef = TypedDict(
    "StartInferenceSchedulerRequestRequestTypeDef",
    {
        "InferenceSchedulerName": str,
    },
)

StopInferenceSchedulerRequestRequestTypeDef = TypedDict(
    "StopInferenceSchedulerRequestRequestTypeDef",
    {
        "InferenceSchedulerName": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateLabelGroupRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateLabelGroupRequestRequestTypeDef",
    {
        "LabelGroupName": str,
    },
)
_OptionalUpdateLabelGroupRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateLabelGroupRequestRequestTypeDef",
    {
        "FaultCodes": Sequence[str],
    },
    total=False,
)


class UpdateLabelGroupRequestRequestTypeDef(
    _RequiredUpdateLabelGroupRequestRequestTypeDef, _OptionalUpdateLabelGroupRequestRequestTypeDef
):
    pass


_RequiredCreateDatasetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDatasetRequestRequestTypeDef",
    {
        "DatasetName": str,
        "ClientToken": str,
    },
)
_OptionalCreateDatasetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDatasetRequestRequestTypeDef",
    {
        "DatasetSchema": DatasetSchemaTypeDef,
        "ServerSideKmsKeyId": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDatasetRequestRequestTypeDef(
    _RequiredCreateDatasetRequestRequestTypeDef, _OptionalCreateDatasetRequestRequestTypeDef
):
    pass


_RequiredCreateLabelGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLabelGroupRequestRequestTypeDef",
    {
        "LabelGroupName": str,
        "ClientToken": str,
    },
)
_OptionalCreateLabelGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLabelGroupRequestRequestTypeDef",
    {
        "FaultCodes": Sequence[str],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateLabelGroupRequestRequestTypeDef(
    _RequiredCreateLabelGroupRequestRequestTypeDef, _OptionalCreateLabelGroupRequestRequestTypeDef
):
    pass


TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateDatasetResponseTypeDef = TypedDict(
    "CreateDatasetResponseTypeDef",
    {
        "DatasetName": str,
        "DatasetArn": str,
        "Status": DatasetStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateInferenceSchedulerResponseTypeDef = TypedDict(
    "CreateInferenceSchedulerResponseTypeDef",
    {
        "InferenceSchedulerArn": str,
        "InferenceSchedulerName": str,
        "Status": InferenceSchedulerStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLabelGroupResponseTypeDef = TypedDict(
    "CreateLabelGroupResponseTypeDef",
    {
        "LabelGroupName": str,
        "LabelGroupArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLabelResponseTypeDef = TypedDict(
    "CreateLabelResponseTypeDef",
    {
        "LabelId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateModelResponseTypeDef = TypedDict(
    "CreateModelResponseTypeDef",
    {
        "ModelArn": str,
        "Status": ModelStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeLabelGroupResponseTypeDef = TypedDict(
    "DescribeLabelGroupResponseTypeDef",
    {
        "LabelGroupName": str,
        "LabelGroupArn": str,
        "FaultCodes": List[str],
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeLabelResponseTypeDef = TypedDict(
    "DescribeLabelResponseTypeDef",
    {
        "LabelGroupName": str,
        "LabelGroupArn": str,
        "LabelId": str,
        "StartTime": datetime,
        "EndTime": datetime,
        "Rating": LabelRatingType,
        "FaultCode": str,
        "Notes": str,
        "Equipment": str,
        "CreatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartDataIngestionJobResponseTypeDef = TypedDict(
    "StartDataIngestionJobResponseTypeDef",
    {
        "JobId": str,
        "Status": IngestionJobStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartInferenceSchedulerResponseTypeDef = TypedDict(
    "StartInferenceSchedulerResponseTypeDef",
    {
        "ModelArn": str,
        "ModelName": str,
        "InferenceSchedulerName": str,
        "InferenceSchedulerArn": str,
        "Status": InferenceSchedulerStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopInferenceSchedulerResponseTypeDef = TypedDict(
    "StopInferenceSchedulerResponseTypeDef",
    {
        "ModelArn": str,
        "ModelName": str,
        "InferenceSchedulerName": str,
        "InferenceSchedulerArn": str,
        "Status": InferenceSchedulerStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDatasetsResponseTypeDef = TypedDict(
    "ListDatasetsResponseTypeDef",
    {
        "NextToken": str,
        "DatasetSummaries": List[DatasetSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListInferenceEventsResponseTypeDef = TypedDict(
    "ListInferenceEventsResponseTypeDef",
    {
        "NextToken": str,
        "InferenceEventSummaries": List[InferenceEventSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredIngestedFilesSummaryTypeDef = TypedDict(
    "_RequiredIngestedFilesSummaryTypeDef",
    {
        "TotalNumberOfFiles": int,
        "IngestedNumberOfFiles": int,
    },
)
_OptionalIngestedFilesSummaryTypeDef = TypedDict(
    "_OptionalIngestedFilesSummaryTypeDef",
    {
        "DiscardedFiles": List[S3ObjectTypeDef],
    },
    total=False,
)


class IngestedFilesSummaryTypeDef(
    _RequiredIngestedFilesSummaryTypeDef, _OptionalIngestedFilesSummaryTypeDef
):
    pass


InferenceInputConfigurationTypeDef = TypedDict(
    "InferenceInputConfigurationTypeDef",
    {
        "S3InputConfiguration": InferenceS3InputConfigurationTypeDef,
        "InputTimeZoneOffset": str,
        "InferenceInputNameConfiguration": InferenceInputNameConfigurationTypeDef,
    },
    total=False,
)

_RequiredInferenceOutputConfigurationTypeDef = TypedDict(
    "_RequiredInferenceOutputConfigurationTypeDef",
    {
        "S3OutputConfiguration": InferenceS3OutputConfigurationTypeDef,
    },
)
_OptionalInferenceOutputConfigurationTypeDef = TypedDict(
    "_OptionalInferenceOutputConfigurationTypeDef",
    {
        "KmsKeyId": str,
    },
    total=False,
)


class InferenceOutputConfigurationTypeDef(
    _RequiredInferenceOutputConfigurationTypeDef, _OptionalInferenceOutputConfigurationTypeDef
):
    pass


ListInferenceSchedulersResponseTypeDef = TypedDict(
    "ListInferenceSchedulersResponseTypeDef",
    {
        "NextToken": str,
        "InferenceSchedulerSummaries": List[InferenceSchedulerSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

IngestionInputConfigurationTypeDef = TypedDict(
    "IngestionInputConfigurationTypeDef",
    {
        "S3InputConfiguration": IngestionS3InputConfigurationTypeDef,
    },
)

InsufficientSensorDataTypeDef = TypedDict(
    "InsufficientSensorDataTypeDef",
    {
        "MissingCompleteSensorData": MissingCompleteSensorDataTypeDef,
        "SensorsWithShortDateRange": SensorsWithShortDateRangeTypeDef,
    },
)

ListLabelGroupsResponseTypeDef = TypedDict(
    "ListLabelGroupsResponseTypeDef",
    {
        "NextToken": str,
        "LabelGroupSummaries": List[LabelGroupSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListLabelsResponseTypeDef = TypedDict(
    "ListLabelsResponseTypeDef",
    {
        "NextToken": str,
        "LabelSummaries": List[LabelSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LabelsInputConfigurationTypeDef = TypedDict(
    "LabelsInputConfigurationTypeDef",
    {
        "S3InputConfiguration": LabelsS3InputConfigurationTypeDef,
        "LabelGroupName": str,
    },
    total=False,
)

ListModelsResponseTypeDef = TypedDict(
    "ListModelsResponseTypeDef",
    {
        "NextToken": str,
        "ModelSummaries": List[ModelSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SensorStatisticsSummaryTypeDef = TypedDict(
    "SensorStatisticsSummaryTypeDef",
    {
        "ComponentName": str,
        "SensorName": str,
        "DataExists": bool,
        "MissingValues": CountPercentTypeDef,
        "InvalidValues": CountPercentTypeDef,
        "InvalidDateEntries": CountPercentTypeDef,
        "DuplicateTimestamps": CountPercentTypeDef,
        "CategoricalValues": CategoricalValuesTypeDef,
        "MultipleOperatingModes": MultipleOperatingModesTypeDef,
        "LargeTimestampGaps": LargeTimestampGapsTypeDef,
        "MonotonicValues": MonotonicValuesTypeDef,
        "DataStartTime": datetime,
        "DataEndTime": datetime,
    },
    total=False,
)

_RequiredCreateInferenceSchedulerRequestRequestTypeDef = TypedDict(
    "_RequiredCreateInferenceSchedulerRequestRequestTypeDef",
    {
        "ModelName": str,
        "InferenceSchedulerName": str,
        "DataUploadFrequency": DataUploadFrequencyType,
        "DataInputConfiguration": InferenceInputConfigurationTypeDef,
        "DataOutputConfiguration": InferenceOutputConfigurationTypeDef,
        "RoleArn": str,
        "ClientToken": str,
    },
)
_OptionalCreateInferenceSchedulerRequestRequestTypeDef = TypedDict(
    "_OptionalCreateInferenceSchedulerRequestRequestTypeDef",
    {
        "DataDelayOffsetInMinutes": int,
        "ServerSideKmsKeyId": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateInferenceSchedulerRequestRequestTypeDef(
    _RequiredCreateInferenceSchedulerRequestRequestTypeDef,
    _OptionalCreateInferenceSchedulerRequestRequestTypeDef,
):
    pass


DescribeInferenceSchedulerResponseTypeDef = TypedDict(
    "DescribeInferenceSchedulerResponseTypeDef",
    {
        "ModelArn": str,
        "ModelName": str,
        "InferenceSchedulerName": str,
        "InferenceSchedulerArn": str,
        "Status": InferenceSchedulerStatusType,
        "DataDelayOffsetInMinutes": int,
        "DataUploadFrequency": DataUploadFrequencyType,
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
        "DataInputConfiguration": InferenceInputConfigurationTypeDef,
        "DataOutputConfiguration": InferenceOutputConfigurationTypeDef,
        "RoleArn": str,
        "ServerSideKmsKeyId": str,
        "LatestInferenceResult": LatestInferenceResultType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InferenceExecutionSummaryTypeDef = TypedDict(
    "InferenceExecutionSummaryTypeDef",
    {
        "ModelName": str,
        "ModelArn": str,
        "InferenceSchedulerName": str,
        "InferenceSchedulerArn": str,
        "ScheduledStartTime": datetime,
        "DataStartTime": datetime,
        "DataEndTime": datetime,
        "DataInputConfiguration": InferenceInputConfigurationTypeDef,
        "DataOutputConfiguration": InferenceOutputConfigurationTypeDef,
        "CustomerResultObject": S3ObjectTypeDef,
        "Status": InferenceExecutionStatusType,
        "FailedReason": str,
    },
    total=False,
)

_RequiredUpdateInferenceSchedulerRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateInferenceSchedulerRequestRequestTypeDef",
    {
        "InferenceSchedulerName": str,
    },
)
_OptionalUpdateInferenceSchedulerRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateInferenceSchedulerRequestRequestTypeDef",
    {
        "DataDelayOffsetInMinutes": int,
        "DataUploadFrequency": DataUploadFrequencyType,
        "DataInputConfiguration": InferenceInputConfigurationTypeDef,
        "DataOutputConfiguration": InferenceOutputConfigurationTypeDef,
        "RoleArn": str,
    },
    total=False,
)


class UpdateInferenceSchedulerRequestRequestTypeDef(
    _RequiredUpdateInferenceSchedulerRequestRequestTypeDef,
    _OptionalUpdateInferenceSchedulerRequestRequestTypeDef,
):
    pass


DataIngestionJobSummaryTypeDef = TypedDict(
    "DataIngestionJobSummaryTypeDef",
    {
        "JobId": str,
        "DatasetName": str,
        "DatasetArn": str,
        "IngestionInputConfiguration": IngestionInputConfigurationTypeDef,
        "Status": IngestionJobStatusType,
    },
    total=False,
)

StartDataIngestionJobRequestRequestTypeDef = TypedDict(
    "StartDataIngestionJobRequestRequestTypeDef",
    {
        "DatasetName": str,
        "IngestionInputConfiguration": IngestionInputConfigurationTypeDef,
        "RoleArn": str,
        "ClientToken": str,
    },
)

DataQualitySummaryTypeDef = TypedDict(
    "DataQualitySummaryTypeDef",
    {
        "InsufficientSensorData": InsufficientSensorDataTypeDef,
        "MissingSensorData": MissingSensorDataTypeDef,
        "InvalidSensorData": InvalidSensorDataTypeDef,
        "UnsupportedTimestamps": UnsupportedTimestampsTypeDef,
        "DuplicateTimestamps": DuplicateTimestampsTypeDef,
    },
)

_RequiredCreateModelRequestRequestTypeDef = TypedDict(
    "_RequiredCreateModelRequestRequestTypeDef",
    {
        "ModelName": str,
        "DatasetName": str,
        "ClientToken": str,
    },
)
_OptionalCreateModelRequestRequestTypeDef = TypedDict(
    "_OptionalCreateModelRequestRequestTypeDef",
    {
        "DatasetSchema": DatasetSchemaTypeDef,
        "LabelsInputConfiguration": LabelsInputConfigurationTypeDef,
        "TrainingDataStartTime": Union[datetime, str],
        "TrainingDataEndTime": Union[datetime, str],
        "EvaluationDataStartTime": Union[datetime, str],
        "EvaluationDataEndTime": Union[datetime, str],
        "RoleArn": str,
        "DataPreProcessingConfiguration": DataPreProcessingConfigurationTypeDef,
        "ServerSideKmsKeyId": str,
        "Tags": Sequence[TagTypeDef],
        "OffCondition": str,
    },
    total=False,
)


class CreateModelRequestRequestTypeDef(
    _RequiredCreateModelRequestRequestTypeDef, _OptionalCreateModelRequestRequestTypeDef
):
    pass


DescribeModelResponseTypeDef = TypedDict(
    "DescribeModelResponseTypeDef",
    {
        "ModelName": str,
        "ModelArn": str,
        "DatasetName": str,
        "DatasetArn": str,
        "Schema": str,
        "LabelsInputConfiguration": LabelsInputConfigurationTypeDef,
        "TrainingDataStartTime": datetime,
        "TrainingDataEndTime": datetime,
        "EvaluationDataStartTime": datetime,
        "EvaluationDataEndTime": datetime,
        "RoleArn": str,
        "DataPreProcessingConfiguration": DataPreProcessingConfigurationTypeDef,
        "Status": ModelStatusType,
        "TrainingExecutionStartTime": datetime,
        "TrainingExecutionEndTime": datetime,
        "FailedReason": str,
        "ModelMetrics": str,
        "LastUpdatedTime": datetime,
        "CreatedAt": datetime,
        "ServerSideKmsKeyId": str,
        "OffCondition": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSensorStatisticsResponseTypeDef = TypedDict(
    "ListSensorStatisticsResponseTypeDef",
    {
        "SensorStatisticsSummaries": List[SensorStatisticsSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListInferenceExecutionsResponseTypeDef = TypedDict(
    "ListInferenceExecutionsResponseTypeDef",
    {
        "NextToken": str,
        "InferenceExecutionSummaries": List[InferenceExecutionSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDataIngestionJobsResponseTypeDef = TypedDict(
    "ListDataIngestionJobsResponseTypeDef",
    {
        "NextToken": str,
        "DataIngestionJobSummaries": List[DataIngestionJobSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDataIngestionJobResponseTypeDef = TypedDict(
    "DescribeDataIngestionJobResponseTypeDef",
    {
        "JobId": str,
        "DatasetArn": str,
        "IngestionInputConfiguration": IngestionInputConfigurationTypeDef,
        "RoleArn": str,
        "CreatedAt": datetime,
        "Status": IngestionJobStatusType,
        "FailedReason": str,
        "DataQualitySummary": DataQualitySummaryTypeDef,
        "IngestedFilesSummary": IngestedFilesSummaryTypeDef,
        "StatusDetail": str,
        "IngestedDataSize": int,
        "DataStartTime": datetime,
        "DataEndTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDatasetResponseTypeDef = TypedDict(
    "DescribeDatasetResponseTypeDef",
    {
        "DatasetName": str,
        "DatasetArn": str,
        "CreatedAt": datetime,
        "LastUpdatedAt": datetime,
        "Status": DatasetStatusType,
        "Schema": str,
        "ServerSideKmsKeyId": str,
        "IngestionInputConfiguration": IngestionInputConfigurationTypeDef,
        "DataQualitySummary": DataQualitySummaryTypeDef,
        "IngestedFilesSummary": IngestedFilesSummaryTypeDef,
        "RoleArn": str,
        "DataStartTime": datetime,
        "DataEndTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
