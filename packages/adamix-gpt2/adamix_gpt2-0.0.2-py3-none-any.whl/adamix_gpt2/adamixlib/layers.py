#  ------------------------------------------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  Licensed under the MIT License (MIT). See LICENSE in the repo root for license information.
#  ------------------------------------------------------------------------------------------
import torch
import torch.nn as nn
import torch.nn.functional as F

import math
from typing import Optional, List
from loralib.layers import *

class AdamixLayer():
    def __init__(
        self,
        share_down: bool,
        share_up: bool,
        num_experts: int
    ):
        self.share_down = share_down
        self.share_up = share_up
        self.num_experts = num_experts

class AdamixLoRALinear(nn.Linear, LoRALayer, AdamixLayer):
    # LoRA implemented in a dense layer
    def __init__(
        self, 
        in_features: int, 
        out_features: int, 
        r: int = 0, 
        lora_alpha: int = 1, 
        lora_dropout: float = 0.,
        fan_in_fan_out: bool = False, # Set this to True if the layer to replace stores weight like (fan_in, fan_out)
        merge_weights: bool = True,
        share_down: bool = False,
        share_up: bool = False,
        num_experts: int = 1,
        **kwargs
    ):
        nn.Linear.__init__(self, in_features, out_features, **kwargs)
        LoRALayer.__init__(self, r=r, lora_alpha=lora_alpha, lora_dropout=lora_dropout,
                           merge_weights=merge_weights)
        AdamixLayer.__init__(self, share_down=share_down, share_up=share_up, num_experts=num_experts)

        self.fan_in_fan_out = fan_in_fan_out
        # Actual trainable parameters
        if r > 0:
            if num_experts > 1 and not share_down:
                self.lora_A = torch.nn.ParameterList([nn.Parameter(self.weight.new_zeros((r, in_features))) for i in range(num_experts)])
            else:
                self.lora_A = nn.Parameter(self.weight.new_zeros((r, in_features)))
            
            if num_experts > 1 and not share_up:
                self.lora_B = torch.nn.ParameterList([nn.Parameter(self.weight.new_zeros((out_features, r))) for i in range(num_experts)])
            else:
                self.lora_B = nn.Parameter(self.weight.new_zeros((out_features, r)))
            
            self.scaling = self.lora_alpha / self.r
            # Freezing the pre-trained weight matrix
            self.weight.requires_grad = False
        self.reset_parameters()
        if fan_in_fan_out:
            self.weight.data = self.weight.data.T

    def reset_parameters(self):
        nn.Linear.reset_parameters(self)
        if hasattr(self, 'lora_A'):
            # initialize A the same way as the default for nn.Linear and B to zero
            if self.num_experts > 1 and (not self.share_down or not self.share_up):
                if not self.share_down and not self.share_up:
                    for i in range(self.num_experts):
                        nn.init.kaiming_uniform_(self.lora_A[i], a=math.sqrt(5))
                        nn.init.zeros_(self.lora_B[i])
                elif not self.share_down:
                    for i in range(self.num_experts):
                        nn.init.kaiming_uniform_(self.lora_A[i], a=math.sqrt(5))
                        nn.init.zeros_(self.lora_B)
                elif not self.share_up:
                    for i in range(self.num_experts):
                        nn.init.kaiming_uniform_(self.lora_A, a=math.sqrt(5))
                        nn.init.zeros_(self.lora_B[i])
            else:
                nn.init.kaiming_uniform_(self.lora_A, a=math.sqrt(5))
                nn.init.zeros_(self.lora_B)

    def train(self, mode: bool = True):
        def T(w):
            return w.T if self.fan_in_fan_out else w
        nn.Linear.train(self, mode)
        if self.merge_weights and self.merged:
            # Make sure that the weights are not merged
            if self.r > 0:
                if self.num_experts > 1 and (not self.share_down or not self.share_up):
                    if not self.share_down and not self.share_up:
                        new_weights_lora_A = sum([p.data for p in self.lora_A]) / self.num_experts
                        new_weights_lora_B = sum([p.data for p in self.lora_B]) / self.num_experts
                        self.weight.data -= T(new_weights_lora_B @ new_weights_lora_A) * self.scaling
                    elif not self.share_down:
                        new_weights_lora_A = sum([p.data for p in self.lora_A]) / self.num_experts
                        self.weight.data -= T(self.lora_B @ new_weights_lora_A) * self.scaling
                    elif not self.share_up:
                        new_weights_lora_B = sum([p.data for p in self.lora_B]) / self.num_experts
                        self.weight.data -= T(new_weights_lora_B @ self.lora_A) * self.scaling
                else:
                    self.weight.data -= T(self.lora_B @ self.lora_A) * self.scaling
            self.merged = False
    
    def eval(self):
        def T(w):
            return w.T if self.fan_in_fan_out else w
        nn.Linear.eval(self)
        if self.merge_weights and not self.merged:
            # Merge the weights and mark it
            if self.r > 0:
                if self.num_experts > 1 and (not self.share_down or not self.share_up):
                    if not self.share_down and not self.share_up:
                        new_weights_lora_A = sum([p.data for p in self.lora_A]) / self.num_experts
                        new_weights_lora_B = sum([p.data for p in self.lora_B]) / self.num_experts
                        self.weight.data += T(new_weights_lora_B @ new_weights_lora_A) * self.scaling
                    elif not self.share_down:
                        new_weights_lora_A = sum([p.data for p in self.lora_A]) / self.num_experts
                        self.weight.data += T(self.lora_B @ new_weights_lora_A) * self.scaling
                    elif not self.share_up:
                        new_weights_lora_B = sum([p.data for p in self.lora_B]) / self.num_experts
                        self.weight.data += T(new_weights_lora_B @ self.lora_A) * self.scaling
                else:
                    self.weight.data += T(self.lora_B @ self.lora_A) * self.scaling
            self.merged = True

    def forward(self, x: torch.Tensor):
        def T(w):
            return w.T if self.fan_in_fan_out else w
        if self.r > 0 and not self.merged:
            result = F.linear(x, T(self.weight), bias=self.bias)
            if self.r > 0:
                if self.num_experts > 1 and (not self.share_down or not self.share_up):
                    if not self.share_down and not self.share_up:
                        expert_idx_A, expert_idx_B = torch.randint(low=0, high=self.num_experts, size=(2,)).tolist()
                        result += (self.lora_dropout(x) @ self.lora_A[expert_idx_A].T @ self.lora_B[expert_idx_B].T) * self.scaling
                    elif not self.share_down:
                        expert_idx = torch.randint(low=0, high=self.num_experts, size=(1,)).item()
                        result += (self.lora_dropout(x) @ self.lora_A[expert_idx].T @ self.lora_B.T) * self.scaling
                    elif not self.share_up:
                        expert_idx = torch.randint(low=0, high=self.num_experts, size=(1,)).item()
                        result += (self.lora_dropout(x) @ self.lora_A.T @ self.lora_B[expert_idx].T) * self.scaling
                else:
                    result += (self.lora_dropout(x) @ self.lora_A.T @ self.lora_B.T) * self.scaling
            return result
        else:
            return F.linear(x, T(self.weight), bias=self.bias)

class AdamixLoRAMergedLinear(nn.Linear, LoRALayer, AdamixLayer):
    # LoRA implemented in a dense layer
    def __init__(
            self,
            in_features: int,
            out_features: int,
            r: int = 0,
            lora_alpha: int = 1,
            lora_dropout: float = 0.,
            enable_lora: List[bool] = [False],
            fan_in_fan_out: bool = False,
            merge_weights: bool = True,
            share_down: bool = False,
            share_up: bool = False,
            num_experts: int = 1,
            **kwargs
    ):
        nn.Linear.__init__(self, in_features, out_features, **kwargs)
        LoRALayer.__init__(self, r=r, lora_alpha=lora_alpha, lora_dropout=lora_dropout,
                           merge_weights=merge_weights)
        AdamixLayer.__init__(self, share_down=share_down, share_up=share_up, num_experts=num_experts)

        assert out_features % len(enable_lora) == 0, \
            'The length of enable_lora must divide out_features'
        self.enable_lora = enable_lora
        self.fan_in_fan_out = fan_in_fan_out
        # Actual trainable parameters
        if r > 0 and any(enable_lora):
            if num_experts > 1 and not share_down:
                self.lora_A = torch.nn.ParameterList([nn.Parameter(self.weight.new_zeros((r*sum(enable_lora), in_features))) for i in range(num_experts)])
            else:
                self.lora_A = nn.Parameter(self.weight.new_zeros((r * sum(enable_lora), in_features)))
            
            if num_experts > 1 and not share_up:
                self.lora_B = torch.nn.ParameterList([nn.Parameter(self.weight.new_zeros((out_features // len(enable_lora) * sum(enable_lora), r))) for i in range(num_experts)])
            else:
                self.lora_B = nn.Parameter(self.weight.new_zeros((out_features // len(enable_lora) * sum(enable_lora), r)))

            self.scaling = self.lora_alpha / self.r
            # Freezing the pre-trained weight matrix
            self.weight.requires_grad = False
            # Compute the indices
            self.lora_ind = self.weight.new_zeros(
                (out_features,), dtype=torch.bool
            ).view(len(enable_lora), -1)
            self.lora_ind[enable_lora, :] = True
            self.lora_ind = self.lora_ind.view(-1)
        self.reset_parameters()
        if fan_in_fan_out:
            self.weight.data = self.weight.data.T

    def reset_parameters(self):
        nn.Linear.reset_parameters(self)
        if hasattr(self, 'lora_A'):
            # initialize A the same way as the default for nn.Linear and B to zero
            if self.num_experts > 1 and (not self.share_down or not self.share_up):
                if not self.share_down and not self.share_up:
                    for i in range(self.num_experts):
                        nn.init.kaiming_uniform_(self.lora_A[i], a=math.sqrt(5))
                        nn.init.zeros_(self.lora_B[i])
                elif not self.share_down:
                    for i in range(self.num_experts):
                        nn.init.kaiming_uniform_(self.lora_A[i], a=math.sqrt(5))
                        nn.init.zeros_(self.lora_B)
                elif not self.share_up:
                    for i in range(self.num_experts):
                        nn.init.kaiming_uniform_(self.lora_A, a=math.sqrt(5))
                        nn.init.zeros_(self.lora_B[i])
                    
    def zero_pad(self, x):
        result = x.new_zeros((*x.shape[:-1], self.out_features))
        result = result.view(-1, self.out_features)
        result[:, self.lora_ind] = x.reshape(
            -1, self.out_features // len(self.enable_lora) * sum(self.enable_lora)
        )
        return result.view((*x.shape[:-1], self.out_features))

    def train(self, mode: bool = True):
        def T(w):
            return w.T if self.fan_in_fan_out else w
        nn.Linear.train(self, mode)
        if self.merge_weights and self.merged:
            # Make sure that the weights are not merged
            if self.r > 0 and any(self.enable_lora):
                if self.num_experts > 1 and (not self.share_down or not self.share_up):
                    if not self.share_down and not self.share_up:
                        new_weights_lora_A = sum([p.data for p in self.lora_A]) / self.num_experts
                        new_weights_lora_B = sum([p.data for p in self.lora_B]) / self.num_experts
                        delta_w = F.conv1d(
                            new_weights_lora_A.unsqueeze(0),
                            new_weights_lora_B.unsqueeze(-1),
                            groups=sum(self.enable_lora)
                        ).squeeze(0)
                    elif not self.share_down:
                        new_weights_lora_A = sum([p.data for p in self.lora_A]) / self.num_experts
                        delta_w = F.conv1d(
                            new_weights_lora_A.unsqueeze(0),
                            self.lora_B.data.unsqueeze(-1),
                            groups=sum(self.enable_lora)
                        ).squeeze(0)
                    elif not self.share_up:
                        new_weights_lora_B = sum([p.data for p in self.lora_B]) / self.num_experts
                        delta_w = F.conv1d(
                            self.lora_A.data.unsqueeze(0),
                            new_weights_lora_B.unsqueeze(-1),
                            groups=sum(self.enable_lora)
                        ).squeeze(0)
                else:
                    delta_w = F.conv1d(
                        self.lora_A.data.unsqueeze(0),
                        self.lora_B.data.unsqueeze(-1),
                        groups=sum(self.enable_lora)
                    ).squeeze(0)
                
                self.weight.data -= self.zero_pad(T(delta_w * self.scaling))
            self.merged = False

    def eval(self):
        def T(w):
            return w.T if self.fan_in_fan_out else w

        nn.Linear.eval(self)
        if self.merge_weights and not self.merged:
            # Merge the weights and mark it
            if self.r > 0 and any(self.enable_lora):
                if self.num_experts > 1 and (not self.share_down or not self.share_up):
                    if not self.share_down and not self.share_up:
                        new_weights_lora_A = sum([p.data for p in self.lora_A]) / self.num_experts
                        new_weights_lora_B = sum([p.data for p in self.lora_B]) / self.num_experts
                        delta_w = F.conv1d(
                            new_weights_lora_A.unsqueeze(0),
                            new_weights_lora_B.unsqueeze(-1),
                            groups=sum(self.enable_lora)
                        ).squeeze(0)
                    elif not self.share_down:
                        new_weights_lora_A = sum([p.data for p in self.lora_A]) / self.num_experts
                        delta_w = F.conv1d(
                            new_weights_lora_A.unsqueeze(0),
                            self.lora_B.data.unsqueeze(-1),
                            groups=sum(self.enable_lora)
                        ).squeeze(0)
                    elif not self.share_up:
                        new_weights_lora_B = sum([p.data for p in self.lora_B]) / self.num_experts
                        delta_w = F.conv1d(
                            self.lora_A.data.unsqueeze(0),
                            new_weights_lora_B.unsqueeze(-1),
                            groups=sum(self.enable_lora)
                        ).squeeze(0)
                else:
                    delta_w = F.conv1d(
                        self.lora_A.data.unsqueeze(0),
                        self.lora_B.data.unsqueeze(-1),
                        groups=sum(self.enable_lora)
                    ).squeeze(0)

                self.weight.data += self.zero_pad(T(delta_w * self.scaling))
            self.merged = True

    def forward(self, x: torch.Tensor):
        def T(w):
            return w.T if self.fan_in_fan_out else w
        if self.merged:
            return F.linear(x, T(self.weight), bias=self.bias)
        else:
            result = F.linear(x, T(self.weight), bias=self.bias)
            if self.r > 0:
                if self.num_experts > 1 and (not self.share_down or not self.share_up):
                    if not self.share_down and not self.share_up:
                        expert_idx_A, expert_idx_B = torch.randint(low=0, high=self.num_experts, size=(2,)).tolist()
                        after_A = F.linear(self.lora_dropout(x), self.lora_A[expert_idx_A])
                        after_B = F.conv1d(
                            after_A.transpose(-2, -1),
                            self.lora_B[expert_idx_B].unsqueeze(-1),
                            groups=sum(self.enable_lora)
                        ).transpose(-2, -1)
                    elif not self.share_down:
                        expert_idx = torch.randint(low=0, high=self.num_experts, size=(1,)).item()
                        after_A = F.linear(self.lora_dropout(x), self.lora_A[expert_idx])
                        after_B = F.conv1d(
                            after_A.transpose(-2, -1),
                            self.lora_B.unsqueeze(-1),
                            groups=sum(self.enable_lora)
                        ).transpose(-2, -1)
                    elif not self.share_up:
                        expert_idx = torch.randint(low=0, high=self.num_experts, size=(1,)).item()
                        after_A = F.linear(self.lora_dropout(x), self.lora_A)
                        after_B = F.conv1d(
                            after_A.transpose(-2, -1),
                            self.lora_B[expert_idx].unsqueeze(-1),
                            groups=sum(self.enable_lora)
                        ).transpose(-2, -1)
                else:
                    after_A = F.linear(self.lora_dropout(x), self.lora_A)
                    after_B = F.conv1d(
                        after_A.transpose(-2, -1),
                        self.lora_B.unsqueeze(-1),
                        groups=sum(self.enable_lora)
                    ).transpose(-2, -1)

                result += self.zero_pad(after_B) * self.scaling
            return result