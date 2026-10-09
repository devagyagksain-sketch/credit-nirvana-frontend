# PS-3 Location Prediction & Confidence Radius

This package provides a complete, executable Python pipeline for predicting a borrower's physical address location and delivering mathematically honest confidence bounds. 

## Scope Boundary
**Important:** This module **DOES NOT** implement NLP or address parsing. It assumes another team extracts structured components (e.g., locality, landmarks, street tokens) from the raw address text. 
The system provides `src/upstream_interface.py` to seamlessly accept the upstream NLP team's output.

## System Architecture

The pipeline processes addresses through the following logical flow:
**Clean → Trust → Prior → Fuse → Calibrate → Output → Update**

1. **Upstream Features**: Ingests mocked/parsed address constraints.
2. **Prior Model**: Uses the commercial geocoder's location (`geocoder_x/y`) and precision-derived variance to establish the baseline spatial belief.
3. **Visit Trust**: Analyzes raw GPS trails and field remarks to identify faked check-ins (via photo hash reuse, GPS displacement, and tortuosity heuristics).
4. **Bayesian Fusion**: Overlays the prior with the observed GPS visit coordinates.
5. **Confidence Region**: Extracts raw containment radii from the Bayesian probability grid.
6. **Conformal Calibration**: Computes a multiplier on a held-out calibration set to ensure the final output actually meets the advertised coverage target.

## Mathematical Formulation

### 1. Bayesian Fusion
The core engine updates a spatial belief (over an $(x, y)$ grid) using Bayes' Rule:
$$ P(L|E) \propto P(L) \prod_{i=1}^{N} P(V_i|L) $$
- **$L$**: The candidate location grid cell.
- **$P(L)$**: The Prior derived from the commercial geocoder and NLP constraints.
- **$V_i$**: The field visit evidence.

### 2. Visit Likelihood & Outlier Mixture
Every visit is modeled as a mixture of a normal check-in distribution and an outlier penalty (since some borrowers are met away from the house, or the visit is falsified):
$$ p(z_i|\mu) = \pi_i \mathcal{N}(z_i; \mu, \sigma_i^2 I) + (1-\pi_i) \text{Outlier}(z_i) $$
- **$z_i$**: Observed GPS point (`checkin_x`, `checkin_y`).
- **$\mu$**: The candidate location.
- **$\sigma_i$**: Visit uncertainty, strictly bound by the device's `gps_accuracy_m`.
- **$\pi_i$**: The output of the `VisitTrustModel` representing the probability the visit genuinely occurred at the door.

### 3. Confidence Region
Once the posterior grid is formed, we extract a radius $r_\alpha$ that contains the desired probability mass:
$$ P(\| \text{true\_pin} - \text{predicted\_pin} \| \le r_\alpha) = \alpha $$
For example, an 80% radius covers 0.8 of the posterior mass.

### 4. Conformal Calibration
Since analytical models make Gaussian assumptions that real data often violates, we apply **Split Conformal Calibration**.
We compute the non-conformity score on a held-out validation set:
$$ s_j = \frac{\| \text{true\_pin}_j - \text{predicted\_pin}_j \|}{\text{raw\_radius}_j} $$
We find the empirical quantile $q$ such that it covers $\alpha$ fraction of the scores. 
The final returned radius is:
$$ r_{\text{calibrated}} = q \times r_{\text{raw}} $$
This provides a rigorous empirical guarantee on our output bounds.

## Code Structure

- `src/upstream_interface.py`: Accepts structured features from the NLP team.
- `src/data_loader.py`: Ingests all PS-3 and shared CSVs.
- `src/feature_builder.py`: Extracts GPS trail physics and photo constraints.
- `src/visit_trust.py`: Calculates $\pi_i$ (Visit Trust).
- `src/prior_model.py`: Generates the initial spatial prior grid.
- `src/likelihood.py`: Computes the mixture likelihood for each visit.
- `src/bayesian_fusion.py`: Combines the Prior and Likelihoods into a Posterior.
- `src/confidence_region.py`: Extracts $r_\alpha$.
- `src/conformal.py`: Calibrates $r_\alpha$ using true distance errors.
- `src/inference.py`: Exposes `LocationPredictor` for production inference.
- `evaluate.py`: The main entry point to train calibrators and output accuracy metrics.

## Running the Pipeline

To run the full end-to-end evaluation:
```bash
python3 evaluate.py
```
*Note: Due to the very small ground-truth sample size (`N=100` surveyed addresses divided into 50 calibration / 50 test), calibration coverage may fluctuate around the target depending on spatial variance.*
