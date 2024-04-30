
# PyDockStats - Web Application

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/molmodcs/roc-auc-pc/blob/main/LICENSE)
![2024-04-30-20-16-09](https://github.com/matheuscamposmt/PyDockStats/assets/69912320/5114b692-dfec-4ad9-bf7a-e7cc96c179ba)

[PyDockStats](https://pydockstats.streamlit.app/) is an easy-to-use Python tool designed to analyze and visualize the performance of Virtual Screening programs in the context of drug discovery and development. It focuses on building [ROC](https://en.wikipedia.org/wiki/Receiver_operating_characteristic) (Receiver Operating Characteristic) and [Predictiveness Curve](https://jcheminf.biomedcentral.com/articles/10.1186/s13321-015-0100-8) curves to assess the predictive power of scoring functions in separating true positives from false positives.

### Features

- **ROC Curve Analysis**: PyDockStats creates a logistic regression model from the data to generate ROC curves. These curves illustrate the trade-offs between the True Positive Rate (TPR) and False Positive Rate (FPR) at various threshold settings. The Area Under the Curve (AUC) provides a quantitative measure of the scoring function's ability to distinguish true positives from false positives.
<p align="center">
  <img src="https://github.com/matheuscamposmt/PyDockStats/assets/69912320/599e6ee2-fedc-4d9b-9174-1168373374fc" width="800" class="center">
</p>


- **Predictiveness Curve (PC) Analysis**: In addition to ROC curves, PyDockStats constructs Predictiveness Curves to evaluate the performance of Virtual Screening programs. These curves quantify and compare the predictive power of scoring functions, aiding in the selection of an optimal score threshold for prospective virtual screening.
<p align="center">
  <img src="https://github.com/matheuscamposmt/PyDockStats/assets/69912320/20b2f2d1-0a13-4a63-b6a6-b3ce5a38b91f" width="800" class="center">
</p>

### How to Use

The web-app is available [here](https://pydockstats.streamlit.app/)

Using PyDockStats is straightforward and intuitive. Follow these steps to analyze the performance of Virtual Screening programs:

1. **Add Programs**: Start by clicking the ➕ Add Program button below. This action creates a new expander for each program you want to analyze. Each expander will be labeled with the name of the program.

2. **Input Data**: Within each program expander, paste the scores of the ligands and decoys into the data editor. You can add as many rows as needed and preview the data in a table format.

3. **Generate Curves**: After adding the scores, click on the ✨ Generate button to create ROC and PC curves for each program. PyDockStats will utilize a logistic regression model to analyze the relationship between the molecule score and activity, distinguishing True Positives from False Positives.

4. **Visualize Results**: The ROC and PC curves will be displayed on the same page for easy comparison. You can download the figures individually using the 📥 Download button located below each figure.

5. **Email Sharing**: If needed, you can send the figures to your email address using the option provided at the bottom of the page.

6. **Save Progress**: To save your progress, click on the 💾 Save Progress button on the sidebar. This action generates a checkpoint file (.pkl) that you can download. Later, you can upload the checkpoint file using the 📁 Upload button, allowing you to load your progress and continue your analysis seamlessly from where you left off.

### Applications

- **Virtual Screening Program Evaluation**: PyDockStats is invaluable for assessing the performance of Virtual Screening programs. By comparing ROC and Predictiveness Curves, researchers can evaluate the efficacy of different scoring functions and make informed decisions about prospective virtual screening.

- **Decision Support in Drug Discovery**: Researchers can use PyDockStats to determine cutoff values and prioritize compounds for experimental testing. This enhances the efficiency of drug discovery programs by focusing resources on the most promising candidates.
<p align="center">
  <img src="https://github.com/matheuscamposmt/PyDockStats/assets/69912320/49722e1f-83a5-4200-8d10-b3caffe04992" width="800" class="center">
</p>

### Support

For any questions, issues, or feature requests, please [open an issue](https://github.com/matheuscamposmt/PyDockStats/issues) on GitHub. We welcome contributions and feedback from the community to improve PyDockStats and make it even more valuable for drug discovery research.

## Authors
* **Matheus C. de Mattos** - (https://github.com/matheuscamposmtt)
* **Luciano T. Costa** - (http://www.molmodcs.uff.br/) or (https://github.com/molmodcs)
* **Marcus V. H. Faria**
* **Leonardo Federico**

See also the list of [contributors](https://github.com/molmodcs/roc-auc-pc/blob/3936564b42f2626d41962c3b16ef074d166d8582/contributors) who participated in this project.

## License

This project is licensed under the GNU License - see the [LICENSE.md](LICENSE.md) file for details

* PyDockStats version 1.0 (746241f) compiled by 'matheuscamposmattos@id.uff.br' on 2022-07-25

   PyDockStats is free software: you can redistribute it and/or modify it under
   the terms of the GNU Lesser General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   PyDockStats is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU Lesser General Public License for more details.

## Acknowledgments

This program is used for evaluating and classifying the results from virtual screening. If you want to know more deeply how it works, check the [paper](https://doi.org/10.1186/s13321-015-0100-8) which the program is based on.

   
## References
Empereur-mot, C., Guillemain, H., Latouche, A. et al. Predictiveness curves in virtual screening. J Cheminform 7, 52 (2015). https://doi.org/10.1186/s13321-015-0100-8
