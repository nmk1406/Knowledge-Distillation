Install torchdistill library
"""

!pip install torchdistill

"""Clone repository"""

!git clone https://github.com/nmk1406/Knowledge-Distillation.git

"""Hyperparameter tuning based on train:val = 45k:5k"""

!python Knowledge-Distillation/examples/image_classification.py --config Knowledge-Distillation/configs/kd/resnet20_from_densenet_bc_k12_depth100-final_run.yaml --log log/cifar10/kd/resnet20_from_densenet_bc_k12_depth100-hyperparameter_tuning.log

"""Final run with hyperparameters determinded by the above hyperparameter-tuning

"""

!python Knowledge-Distillation/examples/image_classification.py --config Knowledge-Distillation/configs/kd/resnet20_from_densenet_bc_k12_depth100-final_run.yaml --log log/cifar10/kd/resnet20_from_densenet_bc_k12_depth100-final_run.log