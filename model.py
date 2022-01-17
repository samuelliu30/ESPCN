import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self, upscale_factor):
        super(Net, self).__init__()

        # Modified the network to support 3 channels
        # added more channels into the intermediate layers
        # add more depth to the network 
        self.conv1 = nn.Conv2d(3, 128, (5, 5), (1, 1), (2, 2))
        self.conv2 = nn.Conv2d(128, 64, (3, 3), (1, 1), (1, 1))
        self.conv3 = nn.Conv2d(64, 32, (3, 3), (1, 1), (1, 1))
        # self.conv3 = nn.Conv2d(32, 1 * (upscale_factor ** 2), (3, 3), (1, 1), (1, 1))
        self.conv4 = nn.Conv2d(32, 3 * (upscale_factor ** 2), (3, 3), (1, 1), (1, 1))

        
        #Remove the pixel shuffle layer for now to run on RadeonML
        self.pixel_shuffle = nn.PixelShuffle(upscale_factor)

    def forward(self, x):
        x = F.tanh(self.conv1(x))
        x = F.tanh(self.conv2(x))
        x = F.tanh(self.conv3(x))
        x = F.sigmoid(self.pixel_shuffle(self.conv4(x)))

        #Remove the pixel shuffle layer for now to run on RadeonML
        #x = F.sigmoid(self.conv4(x))
        return x


if __name__ == "__main__":
    model = Net(upscale_factor=3)
    print(model)
