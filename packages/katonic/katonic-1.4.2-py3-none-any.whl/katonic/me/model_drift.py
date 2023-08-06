#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#
import io

from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import CatTargetDriftTab
from evidently.dashboard.tabs import ClassificationPerformanceTab
from evidently.dashboard.tabs import DataDriftTab
from evidently.dashboard.tabs import DataQualityTab
from evidently.dashboard.tabs import NumTargetDriftTab
from evidently.dashboard.tabs import RegressionPerformanceTab
from minio import Minio


class DashDashboard:
    def __init__(
        self,
        training_data,
        production_data,
        target_feature_type,
        is_current_target_available: bool = False,
        model=None,
    ):
        self.ref_data = training_data
        self.cur_data = production_data

        # Performance Dashboard
        if is_current_target_available and target_feature_type and model:

            self.ref_data["prediction"] = model.predict(
                self.ref_data.drop(["target"], axis=1)
            )
            self.cur_data["prediction"] = model.predict(
                self.cur_data.drop(["target"], axis=1)
            )

            if target_feature_type.lower() == "cat":
                self.dashboard = Dashboard(
                    tabs=[
                        DataDriftTab(verbose_level=1),
                        CatTargetDriftTab(verbose_level=1),
                        DataQualityTab(verbose_level=1),
                        ClassificationPerformanceTab(verbose_level=1),
                    ]
                )

            elif target_feature_type.lower() == "num":
                self.dashboard = Dashboard(
                    tabs=[
                        DataDriftTab(verbose_level=1),
                        CatTargetDriftTab(verbose_level=1),
                        DataQualityTab(verbose_level=1),
                        RegressionPerformanceTab(verbose_level=1),
                    ]
                )

        # Drift, Quality Dashboard
        elif target_feature_type == "cat" and not is_current_target_available:
            self.dashboard = Dashboard(
                tabs=[
                    DataDriftTab(verbose_level=1),
                    CatTargetDriftTab(verbose_level=1),
                    DataQualityTab(verbose_level=1),
                ]
            )
        elif target_feature_type == "num" and not is_current_target_available:
            self.dashboard = Dashboard(
                tabs=[
                    DataDriftTab(verbose_level=1),
                    NumTargetDriftTab(verbose_level=1),
                    DataQualityTab(verbose_level=1),
                ]
            )
        self.dashboard.calculate(
            self.ref_data,
            self.cur_data,
        )

    def save(self, FILE_PATH, ACCESS_KEY=None, SECRET_KEY=None, BUCKET_NAME=None):

        if ACCESS_KEY and SECRET_KEY and BUCKET_NAME:

            client = Minio(
                "minio-server.default.svc.cluster.local:9000",
                access_key=ACCESS_KEY,
                secret_key=SECRET_KEY,
                secure=False,
            )

            client.put_object(
                bucket_name=BUCKET_NAME,
                object_name=FILE_PATH,
                data=io.BytesIO(self.dashboard._json().encode("utf-8")),
                length=-1,
                content_type="application/json",
                part_size=10 * 1024 * 1024,
            )

        else:
            self.dashboard._save_to_json(FILE_PATH)
