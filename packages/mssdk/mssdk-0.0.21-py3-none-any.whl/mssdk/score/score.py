# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/8/25 18:33
Desc: 判分主类，主要提供判分及保存
"""
import os
import sys
from typing import Any

import requests
import yaml


class Score:
    def __init__(self, file_name):
        self.answer_title = None
        self.answer_result = {}
        self.answer_detail = {}
        self.name = self.get_user_name()
        self.file_name = file_name
        self.answer = self.get_answer(file_name)
        self.right_answer = {}
        self.wrong_answer = {}
        print(self.tips())

    def tips(self):
        tip_content = (
            f"感谢您学习 {self.answer_title} 课程，本次课程共需要回答 {len(self.answer)} 个问题，问题的序号分别为：{list(self.answer.keys())}"
            f"您需要使用 score.judge() 函数来提交问题。比如提交 `q_1` 问题的答案：score.judge('q_1', q_1)，其中 `'q_1'` 为序号，`q_1` 为答案变量。"
        )
        return tip_content

    @classmethod
    def get_user_name(cls):
        # 获取 Ubuntu 系统的用户名
        user_name = sys.path[0].split("/")[-1].split("-")[-1]
        return user_name

    def get_answer(self, file_name: str = "answer"):
        self.answer_title = file_name
        file_address = os.path.join(os.path.dirname(os.path.abspath(__file__)),  file_name)
        f = open(
            rf"{file_address}.yaml",
            "r",
        )
        data = yaml.load(f, Loader=yaml.FullLoader)
        question_list = list(data.keys())
        answer_dict = {}
        for i in range(0, len(data.keys())):
            answer_dict.update(
                {question_list[i]: eval(data[question_list[i]])}
            )
        return answer_dict

    def judge(self, q_name: str = None, q_value: Any = "hello") -> str:
        """
        判分逻辑
        :param q_name: 问题的序列号
        :type q_name: str
        :param q_value: 问题的答案
        :type q_value: Any
        :return: 回答正确与否
        :rtype: str
        """
        # 记录具体 q_name 问题的回答次数
        self.answer_detail[f"{q_name}_total_num"] = (
            self.answer_detail.get(f"{q_name}_total_num", 0) + 1
        )
        if str(q_name) in self.answer:
            answer_result = self.answer[str(q_name)]
            if answer_result == q_value:
                self.right_answer[f"{str(q_name)}_total_right_num"] = (
                    self.right_answer.get(f"{str(q_name)}_total_right_num", 0)
                    + 1
                )
                self.answer_detail[
                    f"{str(q_name)}_total_right_num"
                ] = self.right_answer[f"{str(q_name)}_total_right_num"]
                return "回答正确"
            else:
                self.wrong_answer[f"{str(q_name)}_total_wrong_num"] = (
                    self.wrong_answer.get(f"{str(q_name)}_total_wrong_num", 0)
                    + 1
                )
                self.answer_detail[
                    f"{str(q_name)}_total_wrong_num"
                ] = self.wrong_answer[f"{str(q_name)}_total_wrong_num"]
                return "回答错误"
        else:
            return "请输入正确的变量名称和变量"

    @property
    def result(self):
        return {"回答正确": self.right_answer, "回答错误": self.wrong_answer}

    def save(self):
        url = "http://140.210.214.231:8000/"
        right_num = len(
            [
                value
                for key, value in self.answer_detail.items()
                if key.endswith("total_right_num") and value != 0
            ]
        )
        all_num = len(
            [
                value
                for key, value in self.answer_detail.items()
                if key.endswith("total_num")
            ]
        )
        if len(self.answer) != all_num:
            print("请回答完所有问题后再提交答案")
            raise "请回答完所有问题后再提交答案"
        self.answer_result["right_rate"] = round(right_num / all_num, 2)
        self.answer_result["right_question"] = [
            "_".join(key.split("_")[:2])
            for key, value in self.answer_detail.items()
            if key.endswith("total_right_num") and value != 0
        ]
        self.answer_result["wrong_question"] = list(
            {
                "_".join(key.split("_")[:2])
                for key, value in self.answer_detail.items()
                if key.endswith("total_num")
            }
            - set(self.answer_result["right_question"])
        )
        payload = {
            "user_name": self.name,
            "answer_title": self.answer_title,
            "answer_detail": str(self.answer_detail),
            "answer_result": str(self.answer_result),
        }
        r = requests.post(url, json=payload)
        if r.status_code == 200:
            return {"msg": "success"}
        else:
            return {"msg": "fail"}


if __name__ == "__main__":
    q_1 = [1, 2, 3, 4]
    q_2 = {"fruit": "apple", "animal": "pig"}
    q_3 = '6'
    score = Score("answer")
    score.judge("q_1", q_1)
    score.judge("q_2", q_1)
    score.judge("q_3", q_1)
    score.result
    score.save()
