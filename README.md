# Exphlot
This repository contains the code developed for Exphlot: EXplainable Privacy assessment for Human LOcation Trajectories.

The framework of Exphlot is composed by 2 main modules: the privacy risk computation and the privacy risk explanations. Both of them are generic modules, which can be instantieted in different ways. In this repository, you can find:
1. Train and test of the rocket model to predict the privacy risk of the people in a dataset of human trajectories.
2. Train and test of the Inception Time model. The objetive is to predict the privacy risk.
3. Train and test of the LSTM model. The objetive is to predict the privacy risk.
4. Local explanations extracted from SHAP with a dynamic masking strategy.
