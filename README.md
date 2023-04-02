# Exphlot
This repository contains the code developed for Exphlot: EXplainable Privacy assessment for Human LOcation Trajectories.

The framework of Exphlot is composed by 2 main modules: the privacy risk computation and the privacy risk explanations. Both of them are generic modules, which can be instantieted in different ways. In this repository, you can find:
1. The complete privacy risk assessment, based on Prudence, for the trajectories. This is an exahustive search, hence the computation may require a while.
2. Train and test of the rocket model to predict the privacy risk of the people in a dataset of human trajectories.
3. Train and test of the Inception Time model. The objetive is to predict the privacy risk.
4. Train and test of the LSTM model. The objetive is to predict the privacy risk.
5. Local explanations extracted from SHAP with a dynamic masking strategy.
