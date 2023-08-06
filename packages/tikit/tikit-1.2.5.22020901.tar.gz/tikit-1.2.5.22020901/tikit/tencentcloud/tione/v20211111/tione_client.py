# -*- coding: utf8 -*-
# Copyright (c) 2017-2021 THL A29 Limited, a Tencent company. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from tikit.tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tikit.tencentcloud.common.abstract_client import AbstractClient
from tikit.tencentcloud.tione.v20211111 import models


class TioneClient(AbstractClient):
    _apiVersion = '2021-11-11'
    _endpoint = 'tione.tencentcloudapi.com'
    _service = 'tione'


    def CreateBatchTask(self, request):
        """创建跑批任务

        :param request: Request instance for CreateBatchTask.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.CreateBatchTaskRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.CreateBatchTaskResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateBatchTask", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateBatchTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)

    def DeleteBatchTask(self, request):
        """删除跑批任务

        :param request: Request instance for DeleteBatchTask.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.DeleteBatchTaskRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DeleteBatchTaskResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteBatchTask", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteBatchTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeBatchTask(self, request):
        """查询跑批任务

        :param request: Request instance for DescribeBatchTask.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeBatchTaskRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeBatchTaskResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeBatchTask", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeBatchTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeModelAccelerateVersions(self, request):
        """模型加速之后的模型版本列表

        :param request: Request instance for DescribeModelAccelerateVersions.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeModelAccelerateVersionsRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeModelAccelerateVersionsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeModelAccelerateVersions", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeModelAccelerateVersionsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)

    def DescribeBatchTasks(self, request):
        """批量预测任务列表信息

        :param request: Request instance for DescribeBatchTasks.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeBatchTasksRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeBatchTasksResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeBatchTasks", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeBatchTasksResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)

    def StopBatchTask(self, request):
        """停止跑批任务

        :param request: Request instance for StopBatchTask.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.StopBatchTaskRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.StopBatchTaskResponse`

        """
        try:
            params = request._serialize()
            body = self.call("StopBatchTask", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.StopBatchTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateDataset(self, request):
        """创建数据集

        :param request: Request instance for CreateDataset.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.CreateDatasetRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.CreateDatasetResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateDataset", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateDatasetResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateTrainingModel(self, request):
        """导入模型

        :param request: Request instance for CreateTrainingModel.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.CreateTrainingModelRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.CreateTrainingModelResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateTrainingModel", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateTrainingModelResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateTrainingTask(self, request):
        """创建模型训练任务

        :param request: Request instance for CreateTrainingTask.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.CreateTrainingTaskRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.CreateTrainingTaskResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateTrainingTask", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateTrainingTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteDataset(self, request):
        """删除数据集

        :param request: Request instance for DeleteDataset.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.DeleteDatasetRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DeleteDatasetResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteDataset", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteDatasetResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteTrainingModel(self, request):
        """删除模型

        :param request: Request instance for DeleteTrainingModel.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.DeleteTrainingModelRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DeleteTrainingModelResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteTrainingModel", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteTrainingModelResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteTrainingModelVersion(self, request):
        """删除模型版本

        :param request: Request instance for DeleteTrainingModelVersion.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.DeleteTrainingModelVersionRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DeleteTrainingModelVersionResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteTrainingModelVersion", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteTrainingModelVersionResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteTrainingTask(self, request):
        """删除训练任务

        :param request: Request instance for DeleteTrainingTask.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.DeleteTrainingTaskRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DeleteTrainingTaskResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteTrainingTask", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteTrainingTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeBillingResourceGroups(self, request):
        """查询资源组详情

        :param request: Request instance for DescribeBillingResourceGroups.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeBillingResourceGroupsRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeBillingResourceGroupsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeBillingResourceGroups", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeBillingResourceGroupsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeBillingSpecs(self, request):
        """本接口(DescribeBillingSpecs)用于查询计费项列表

        :param request: Request instance for DescribeBillingSpecs.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeBillingSpecsRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeBillingSpecsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeBillingSpecs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeBillingSpecsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeBillingSpecsPrice(self, request):
        """本接口(DescribeBillingSpecsPrice)用于查询计费项价格。

        :param request: Request instance for DescribeBillingSpecsPrice.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeBillingSpecsPriceRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeBillingSpecsPriceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeBillingSpecsPrice", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeBillingSpecsPriceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDatasetDetailStructured(self, request):
        """查询结构化数据集详情

        :param request: Request instance for DescribeDatasetDetailStructured.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeDatasetDetailStructuredRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeDatasetDetailStructuredResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDatasetDetailStructured", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDatasetDetailStructuredResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDatasetDetailUnstructured(self, request):
        """查询非结构化数据集详情

        :param request: Request instance for DescribeDatasetDetailUnstructured.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeDatasetDetailUnstructuredRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeDatasetDetailUnstructuredResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDatasetDetailUnstructured", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDatasetDetailUnstructuredResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDatasets(self, request):
        """查询数据集列表

        :param request: Request instance for DescribeDatasets.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeDatasetsRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeDatasetsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDatasets", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDatasetsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeInferTemplates(self, request):
        """查询推理镜像模板

        :param request: Request instance for DescribeInferTemplates.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeInferTemplatesRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeInferTemplatesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInferTemplates", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInferTemplatesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeLatestTrainingMetrics(self, request):
        """查询最近上报的训练自定义指标

        :param request: Request instance for DescribeLatestTrainingMetrics.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeLatestTrainingMetricsRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeLatestTrainingMetricsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeLatestTrainingMetrics", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeLatestTrainingMetricsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeLogs(self, request):
        """获取训练、推理、Notebook服务的日志

        :param request: Request instance for DescribeLogs.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeLogsRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeLogsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeLogs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeLogsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeTrainingFrameworks(self, request):
        """训练框架列表

        :param request: Request instance for DescribeTrainingFrameworks.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTrainingFrameworksRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTrainingFrameworksResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeTrainingFrameworks", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTrainingFrameworksResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeTrainingMetrics(self, request):
        """查询训练自定义指标

        :param request: Request instance for DescribeTrainingMetrics.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTrainingMetricsRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTrainingMetricsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeTrainingMetrics", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTrainingMetricsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeTrainingModelVersion(self, request):
        """查询模型版本

        :param request: Request instance for DescribeTrainingModelVersion.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTrainingModelVersionRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTrainingModelVersionResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeTrainingModelVersion", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTrainingModelVersionResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeTrainingModelVersions(self, request):
        """模型版本列表

        :param request: Request instance for DescribeTrainingModelVersions.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTrainingModelVersionsRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTrainingModelVersionsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeTrainingModelVersions", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTrainingModelVersionsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeTrainingModels(self, request):
        """模型列表

        :param request: Request instance for DescribeTrainingModels.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTrainingModelsRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTrainingModelsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeTrainingModels", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTrainingModelsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeTrainingTask(self, request):
        """训练任务详情

        :param request: Request instance for DescribeTrainingTask.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTrainingTaskRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTrainingTaskResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeTrainingTask", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTrainingTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeTrainingTaskPods(self, request):
        """训练任务pod列表

        :param request: Request instance for DescribeTrainingTaskPods.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTrainingTaskPodsRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTrainingTaskPodsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeTrainingTaskPods", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTrainingTaskPodsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeTrainingTasks(self, request):
        """训练任务列表

        :param request: Request instance for DescribeTrainingTasks.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTrainingTasksRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTrainingTasksResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeTrainingTasks", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTrainingTasksResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def PushTrainingMetrics(self, request):
        """上报训练自定义指标

        :param request: Request instance for PushTrainingMetrics.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.PushTrainingMetricsRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.PushTrainingMetricsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("PushTrainingMetrics", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.PushTrainingMetricsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def StopTrainingTask(self, request):
        """停止模型训练任务

        :param request: Request instance for StopTrainingTask.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.StopTrainingTaskRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.StopTrainingTaskResponse`

        """
        try:
            params = request._serialize()
            body = self.call("StopTrainingTask", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.StopTrainingTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)

    def CreateModelService(self, request):
        """用于创建、发布一个新的模型服务

        :param request: Request instance for CreateModelService.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.CreateModelServiceRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.CreateModelServiceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateModelService", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateModelServiceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)

    def ModifyModelService(self, request):
        """用于更新模型服务

        :param request: Request instance for ModifyModelService.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.ModifyModelServiceRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.ModifyModelServiceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyModelService", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyModelServiceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)
    
    def DescribeModelService(self, request):
        """查询单个服务

        :param request: Request instance for DescribeModelService.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeModelService", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeModelServiceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeModelServiceCallInfo(self, request):
        """展示服务的调用信息

        :param request: Request instance for DescribeModelServiceCallInfo.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceCallInfoRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceCallInfoResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeModelServiceCallInfo", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeModelServiceCallInfoResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeModelServiceGroup(self, request):
        """查询单个服务组

        :param request: Request instance for DescribeModelServiceGroup.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceGroupRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceGroupResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeModelServiceGroup", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeModelServiceGroupResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeModelServiceGroups(self, request):
        """列举在线推理服务组

        :param request: Request instance for DescribeModelServiceGroups.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceGroupsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceGroupsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeModelServiceGroups", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeModelServiceGroupsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeModelServices(self, request):
        """查询多个服务

        :param request: Request instance for DescribeModelServices.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelServicesRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelServicesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeModelServices", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeModelServicesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteModelService(self, request):
        """根据服务id删除模型服务

        :param request: Request instance for DeleteModelService.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteModelServiceRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteModelServiceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteModelService", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteModelServiceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteModelServiceGroup(self, request):
        """根据服务组id删除服务组下所有模型服务

        :param request: Request instance for DeleteModelServiceGroup.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteModelServiceGroupRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteModelServiceGroupResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteModelServiceGroup", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteModelServiceGroupResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyServiceGroupWeights(self, request):
        """更新推理服务组流量分配

        :param request: Request instance for ModifyServiceGroupWeights.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyServiceGroupWeightsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyServiceGroupWeightsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyServiceGroupWeights", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyServiceGroupWeightsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)
