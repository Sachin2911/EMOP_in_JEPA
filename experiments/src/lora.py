#Contains the custom lora implementation
import torch
import torch.nn as nn

class LoRa(nn.Module): 
    """
    Instead of updating W directly, we learn a small additive update: W' = W + (B @ A) * (alpha / rank)
    Note B is initialized with zeros — so ΔW = BA = 0 at start (model unchanged)
    """
    def __init__(self, feat_in, feat_out, rank=16, alpha=32, device="cpu", dtype=torch.bfloat16):
        super().__init__() #Inherits from nn.Module
        self.lora_A = nn.Parameter(torch.zeros((rank, feat_out), device=device, dtype=dtype)) #Tells pytorch this is a learnable param not a normal tensor
        nn.init.normal_(self.lora_A, mean=0, std=1) #Makes every ele Gaussian
        
        #The second matrix
        self.lora_B = nn.Parameter(torch.zeros((feat_in, rank), device=device, dtype=dtype))
        
        self.scale = alpha/rank #Controls how much influence the adapter has, check the forward
        self.enabled = True #Whether the adapter is on or off
        
    def forward(self, original_weights):
        if self.enabled:
            return original_weights + (self.lora_B @ self.lora_A) * self.scale
        return original_weights