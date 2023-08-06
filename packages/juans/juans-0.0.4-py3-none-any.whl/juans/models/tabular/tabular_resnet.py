import torch.nn as nn
import torch.nn.functional as F


class ResidualBlock(nn.Module):
    def __init__(self, channel):
        super().__init__()
        self.fc = nn.Linear(channel, channel)

    def forward(self, x):
        y = F.relu(self.fc(x))
        y = self.fc(y)

        return F.relu(x + y)


class TBResNet(nn.Module):
    def __init__(self, num_inputs=286, num_outputs=1, num_hiddens=512):
        super().__init__()
        num_hiddens_list = [round(num_hiddens / (2 ** i)) for i in range(4)]
        self.block = nn.Sequential(
            nn.Linear(num_inputs, num_hiddens_list[0]),
            nn.ReLU(),
            nn.BatchNorm1d(num_hiddens_list[0]),
            ResidualBlock(num_hiddens_list[0]),
            nn.Linear(num_hiddens_list[0], num_hiddens_list[1]),
            nn.ReLU(),
            nn.BatchNorm1d(num_hiddens_list[1]),
            ResidualBlock(num_hiddens_list[1]),
            nn.Linear(num_hiddens_list[1], num_hiddens_list[2]),
            nn.ReLU(),
            nn.BatchNorm1d(num_hiddens_list[2]),
            ResidualBlock(num_hiddens_list[2]),
            nn.Linear(num_hiddens_list[2], num_hiddens_list[3]),
            nn.ReLU(),
        )
        self.fc = nn.Linear(num_hiddens_list[3], num_outputs)

    def forward(self, x):
        x = self.block(x)
        x = self.fc(x)
        return x
