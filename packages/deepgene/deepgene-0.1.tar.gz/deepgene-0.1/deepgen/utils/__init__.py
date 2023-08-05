import gin
from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import ModelCheckpoint

from pytorch_lightning.loggers import CometLogger
from .train_test import train_model, test_model
from .viz import viz_heatmap, create_heatmap, create_dist_plot

Trainer = gin.external_configurable(Trainer)
CometLogger = gin.external_configurable(CometLogger)
ModelCheckpoint = gin.external_configurable(ModelCheckpoint)

train_model = gin.external_configurable(train_model)
test_model = gin.external_configurable(test_model)
