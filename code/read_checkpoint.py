import torch

checkpoint = torch.load('checkpoint.pth')

print(checkpoint.keys())

epoch = checkpoint['epoch']
print(f"Last completed epoch: {epoch}")