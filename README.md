# Project: Rage Against the Mice

##### Neuromatch Academy Project - pod-129-large-manatee
![pod-129-large-manatee](https://raw.githubusercontent.com/gumadeiras/neuromatch-academy/master/github_images/peixe_boi.jpg?token=ADK6ITMYKMZ7NE6Q3GKD7OS7EA4FC)

## Scientific context
 
 Brain-computer interfaces (BCIs) acquire brain signals, analyze them, and translate them into commands that are relayed to output devices that carry out desired actions. The day-to-day and moment-to-moment reliability of BCI performance must be improved so that it approaches the reliability of natural muscle-based function [Shih et al., 2012]. A standard approach to building BCIs consists of modeling brain activity in animal models performing isolated tasks. In this work, we propose to model neuronal activity as a way to infer motor behavior. Can we identify which - and to what extent - neuronal populations are required for the wheel turning behavior.


## Specific questions

- Can we model visual perception to motor coordination neuronal activity propagation and infer the wheel rotation (in degrees) from neuronal activity alone?

- Which populations are required for the behavior and to what extent (modeling with few neurons vs full population)

- Which brain wave (alpha, beta, gamma, delta or theta) is most related to intention activities in the brain

## Project breakdown
    
-   Isolate neuronal populations that encode visual perception of the moving target and motor actions, not reward.
    
-   Model spiking activity to infer wheel rotation direction (left or right).
    
-   Refine model to infer wheel rotation (in degrees).


## Proposed analyses: 

- Neuronal Population Coding
- Dimensionality Reduction (Single Trial Manifolds, dPCA)
- MLE/HMM
- Spectral Decomposition    

## Dataset: 

Steinmetz dataset. Electrophysiology from multiple regions of mouse brain during 2AFC (two-alternative forced choice) task.  Image source: Steinmetz et al. 2019
  ![Image from Steinmetz et al.](https://raw.githubusercontent.com/gumadeiras/neuromatch-academy/master/github_images/steinmetz.jpg?token=ADK6ITL34UPRJHYLT77UGAC7EA4LY)

## Techniques

-   Python code (GitHub, Google Colab or Jupyter Notebooks)
    
-   Neuronal population coding
    
-   Dimensionality reduction (Clustering, PCA, nonlinear, ...)
    
-   Optimal control?
    
-   Model (MLE, HMM, ...)
    

## Controls

-   Resampling neurons
    
-   Cross-Validation/Leave-one-out
    
-   How changing the clustering technique affects results
    
-   Comparative metrics with state-of-art techniques (or any technique in the literature)


## Predictions

Forebrain and midbrain regions integrate external stimuli and reward probability and are not necessary for motor output inference. Motor neurons alone are enough, and required, to infer forelimb movement to map wheel rotation (regardless of task outcome giving a reward or not).


## Members

Allan Paulo de Souza - allanpaulo2@hotmail.com

Gustavo Madeira Santana - gumadeiras@gmail.com

Heitor Rapela Medeiros - hrm@cin.ufpe.br

Mentor: Michael Okun - m.okun@le.ac.uk