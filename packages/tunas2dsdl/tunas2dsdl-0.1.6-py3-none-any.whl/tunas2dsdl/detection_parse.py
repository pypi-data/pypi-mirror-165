import json
import re
from .general.classdomain import ClassDomain, Label
from .general.struct import Field, Struct
from .general.samples import DataSample


class DetectionParse:
    INSTANCE_SEG_ANN_TYPE = "polygon"
    DETECTION_ANN_TYPE = "box2d"
    PARENT_PATTERN = "Parent"

    def __init__(self, data_info_file, ann_file, dataset_name=None):
        self._dataset_name = dataset_name
        self._data_info_file = data_info_file
        self._annotation_file = ann_file
        self._data_info = self._read_json(data_info_file)
        self._annotation_info = self._read_json(ann_file)
        self._meta_info = self._parse_meta_info()
        self._parent_class_domain, self._class_domain, self.raw_class_info = self._parse_class_domain()  # 父类的class domain和子类的class domain
        self._dsdl_version_info = {"$dsdl-version": "0.5.0"}
        self._struct_defs, self._samples = self._parse_ann_info()

    def _parse_meta_info(self):
        """
        提取数据集元信息
        :return: 元信息字典
        """
        meta_info = {k: v for k, v in self._data_info.items() if k not in ("tasks", "statistics")}
        meta_info["sub_dataset_name"] = self._annotation_info["sub_dataset_name"]
        if not self._dataset_name:
            self._dataset_name = meta_info["dataset_name"]
        return meta_info

    def _parse_class_domain(self):
        """
        提取class domain相关的信息
        :return: 父类class domain对象，子类class domain对象，class原始信息字典
        """
        class_domain = ClassDomain(self.clean(f"{self._dataset_name}ClassDom"))
        parent_class_domain = ClassDomain(self.clean(f"{self._dataset_name}{self.PARENT_PATTERN}ClassDom"))
        raw_class_info = {}
        for task in self._data_info["tasks"]:
            task_type, catalog = task["type"], task["catalog"]
            task_class_info = {}
            if task_type not in (self.INSTANCE_SEG_ANN_TYPE, self.DETECTION_ANN_TYPE):
                continue
            raw_class_info[task_type] = task_class_info
            for label_info in catalog:
                label_name = label_info["category_name"]
                task_class_info[label_info['category_id']] = label_name
                label_obj = Label(label_name)
                if label_obj in class_domain:
                    continue
                class_domain.add_label(label_obj)
                for supercategory_name in label_info.get("supercategories", []):
                    super_label = Label(supercategory_name)
                    if super_label not in parent_class_domain:
                        parent_class_domain.add_label(super_label)
                    label_obj.add_supercategory(super_label)  # 添加父类
        if parent_class_domain:
            class_domain.set_parent(parent_class_domain)
            return parent_class_domain, class_domain, raw_class_info
        else:
            return None, class_domain, raw_class_info

    def _parse_ann_info(self):
        samples = self._annotation_info["samples"]
        object_struct = Struct("LocalObjectEntry")
        sample_struct = Struct("ObjectDetectionSample")
        media_field = Field("media", field_type="media")
        sample_struct.add_field(media_field)  # 添加图像field
        annotation_field = Field("annotations", field_type="list", param=object_struct.as_others_param(sample_struct))
        sample_struct.add_field(annotation_field)  # 添加annotation field
        sample_container = DataSample(sample_struct, self._class_domain)

        for sample in samples:
            sample_item = {}  # 存储当前样本信息
            media_info = sample["media"]
            img_path = media_info.pop("path")
            sample_item["media"] = img_path  # 添加图像样本信息
            for k, v in media_info.items():  # 添加图像相关的attributes
                this_field = Field(k, field_value=v, is_attr=True)
                sample_struct.add_field(this_field)
                sample_item[k] = v
            all_gt_info = {}

            if "ground_truth" in sample:
                gt_info = sample["ground_truth"]
            else:
                gt_info = []
                sample_struct.set_optional("annotations")
            annotations = []
            for gt in gt_info:
                # 获取ann_id
                ann_id = gt.pop("ann_id")
                ann_id = gt.pop("ref_ann_id", ann_id)
                gt["ann_id"] = ann_id
                gt_item = {}
                gt_type = gt.pop("type")
                if gt_type == self.DETECTION_ANN_TYPE:
                    bbox_field = Field("bbox", field_type="bbox")
                    object_struct.add_field(bbox_field)
                    gt_item["bbox"] = gt.pop("bbox")
                elif gt_type == self.INSTANCE_SEG_ANN_TYPE:
                    ins_field = Field("points", field_type="points")
                    object_struct.add_field(ins_field)
                    gt_item["points"] = gt.pop("points")
                else:
                    continue
                # 创建LabelField并将值装进gt_item里面
                label_field = Field("category", field_type="category", param=f"${object_struct.ARG}")
                object_struct.add_field(label_field)
                category_id = gt.pop("categories")[0]["category_id"]
                category_name = self.raw_class_info[gt_type][category_id]  # 拿到category_name
                gt_item["category"] = self._class_domain.index(category_name)
                attributes = gt.pop("attributes")
                for attr_k, attr_v in attributes.items():
                    attr_field = Field(attr_k, field_value=attr_v, is_attr=True)
                    object_struct.add_field(attr_field, optional=True)
                    gt_item[attr_k] = attr_v
                for other_k, other_v in gt.items():
                    other_field = Field(other_k, field_value=other_v, is_attr=True)
                    object_struct.add_field(other_field)
                    gt_item[other_k] = other_v
                all_gt_info.setdefault(ann_id, {})
                all_gt_info[ann_id].update(gt_item)

            annotations.extend(list(all_gt_info.values()))
            if annotations:
                sample_item["annotations"] = annotations

            sample_container.add_item(sample_item)
        return (object_struct, sample_struct), sample_container

    @staticmethod
    def _read_json(file):
        with open(file, "r") as f:
            json_info = json.load(f)
        return json_info

    @staticmethod
    def clean(varStr):
        return re.sub('\W|^(?=\d)', '', varStr)

    @property
    def struct_defs(self):
        """
        dsdl的struct定义字典组成的列表
        """
        return self._struct_defs

    @property
    def samples(self):
        """
        dsdl的data字段下的内容，为一个字典，有sample-type域samples字段，samples包含了样本列表
        """
        return self._samples

    @property
    def sample_info(self):
        """
        tunas v0.3的annotation的json文件的原始内容
        """
        return self._annotation_info

    @property
    def class_domain_info(self):
        """
        dsdl的class_domain的定义字典
        """
        return self._parent_class_domain, self._class_domain

    @property
    def meta_info(self):
        """
        dsdl的元信息内容
        """
        return self._meta_info

    @property
    def data_info_file(self):
        """
        返回tunas v0.3 dataset_info.json的文件路径
        """
        return self._data_info_file

    @property
    def annotation_file(self):
        """
        返回tunas v0.3 的标注文件json文件的路径
        """
        return self._annotation_file

    @property
    def dsdl_version(self):
        """
        dsdl的版本信息字典
        """
        return self._dsdl_version_info
