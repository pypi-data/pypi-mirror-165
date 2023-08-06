#  ------------------------------------------------------------------------------------------
#  Copyright (c). All rights reserved.
#  Licensed under the MIT License (MIT). See LICENSE in the repo root for license information.
#  ------------------------------------------------------------------------------------------
import torch
import torch.nn as nn

from typing import Dict

from loralib.layers import LoRALayer


def mark_only_lora_as_trainable(model: nn.Module, bias: str = 'none') -> None:
    for n, p in model.named_parameters():
        if 'lora_' not in n:
            p.requires_grad = False
    if bias == 'none':
        return
    elif bias == 'all':
        for n, p in model.named_parameters():
            if 'bias' in n:
                p.requires_grad = True
    elif bias == 'lora_only':
        for m in model.modules():
            if isinstance(m, LoRALayer) and \
                hasattr(m, 'bias') and \
                m.bias is not None:
                    m.bias.requires_grad = True
    else:
        raise NotImplementedError


def adamix_state_dict(model_state_dict: Dict, bias: str = 'none') -> Dict[str, torch.Tensor]:
    return {k: model_state_dict[k] for k in model_state_dict if 'lora_' in k or 'expert_score_weight' in k or 'deepspeed_experts' in k}