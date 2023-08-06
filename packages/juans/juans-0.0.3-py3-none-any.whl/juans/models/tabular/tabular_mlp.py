# Third party libraries
import torch
import torch.nn as nn

# User defined libraries
# 在构建不同模型时的几个要求
# 1. 所有函数输入、输出参数命名保持一致，注意单复数，变量命名要有合理的含义
# 2. 变量命名用小写字母+下划线、类命名用大驼峰
# 2. 模型代码保持简洁和可扩展性，减少不必要的包装
# 3. 做注释


class TabularMLP(nn.Module):
    def __init__(self, num_inputs=1, num_outputs=1):
        super().__init__()
        self.fc = torch.nn.Sequential(torch.nn.Linear(num_inputs, num_outputs))

    def forward(self, x):
        result = self.fc(x)
        return result
