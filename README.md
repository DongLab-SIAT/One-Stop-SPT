# **One-Stop SPT: An Integrated Python Toolkit for One-Stop Analysis of Live-Cell Single-Particle Tracking Data**

*A unified and cross-platform Python framework for SPT data processing, nuclear segmentation, trajectory tracking, and biophysical modeling.*  


---

## **1. Overview**

One-Stop SPT is an integrated and open-source Python toolkit designed for end-to-end analysis of live-cell single-particle tracking data.  
Motivated by the operational fragmentation of existing SPT software, One-Stop SPT consolidates essential analytical components—including image pre-processing,single-molecule localization, trajectory reconstruction, nuclear segmentation, kinetic modeling, confinement analysis, and motion-state classification—into a unified workflow.

One-Stop SPT enables robust quantification of transcription factor dynamics, supports cross-platform operation, and is suitable for large-scale SPT datasets commonly generated in modern single-molecule imaging experiments.


## **2. Key Features**

### **Complete SPT Workflow Integration**

- TIFF image stack loading and visualization  
- Per-frame normalization, γ-correction, and optional up-sampling  
- GLRT-based localization with iterative deflation and sub-pixel refinement  
- KNN-based trajectory linking with gap closing  
- Parallel processing for high-throughput datasets

### **Deep Learning–Based Nuclear Segmentation**

- Multi-attention U-Net (MaU-Net) designed for SPT images  
- Dual-stream encoder (Gray vs. Render + Scatter)  
- Cross-stream attention fusion for high-accuracy nuclear masks  
- Offline model training and GPU-accelerated inference

### **Biophysical Analysis**

- Spot-On kinetic modeling  
- Radius of Confinement (RoC) estimation via constrained MSD fitting  
- Motion-State Classification using spatial density labeling  
- Supports analysis of TF dynamics, chromatin interactions, condensate transitions

### **High Throughput & Reproducible**

- Memory-mapped TIFF loading for efficient large data handling  
- Vectorized and parallelized computation throughout  
- Unified GUI ensuring reproducibility and consistency  
- Script-level access for automated workflows

### **User-Friendly GUI**

- Integrated graphical interface for end-to-end analysis  
- Interactive tools for inspecting images, localizations, trajectories  
- Batch-processing support for multiple files and parameters

---

## **3. System Requirements**

| Category             | Requirement                                       |
| :------------------- | :------------------------------------------------ |
| **Operating System** | Windows 10 or higher; Linux                       |
| **Python Version**   | Python ≥ 3.10                                     |
| **CPU**              | Multi-core processor recommended                  |
| **Memory**           | ≥ 16 GB (for large TIFF stacks)                   |
| **GPU (optional)**   | NVIDIA CUDA-enabled GPU (recommended for MaU-Net) |


---

## **4. Installation**

### **1. Clone the repository**

```bash
git clone https://github.com/DongLab-SIAT/One-Stop-SPT.git
cd One-Stop-SPT
```

### **2. Create an isolated Python environment (recommended)**

One-Stop SPT can be installed in either a standard Python virtual environment or a
Conda environment. Conda is often preferred by users who manage multiple
scientific Python environments on the same machine.

**Option A: Python virtual environment**

```bash
python -m venv one-stop-spt
```

**Windows**

```bash
one-stop-spt\Scripts\activate
```

**Linux/macOS**

```bash
source one-stop-spt/bin/activate
```

**Option B: Conda environment**

```bash
conda create -n one-stop-spt python=3.10
conda activate one-stop-spt
```

### **3. Install Python dependencies**

```bash
pip install -r requirements.txt
```

### **4. Install core algorithm package**

```bash
cd SPTpy
pip install -e .
```

---

## **5. Usage**

One-Stop SPT is primarily used through its graphical interface.  
Launch the GUI according to your current working directory:

The public toolkit name is One-Stop SPT; the Python module name remains `SPTpy`
for compatibility with the current package structure.

**From the repository root directory**

```bash
python -m SPTpy.SPTpy
```

**From inside the `SPTpy` package directory**

```bash
python -m SPTpy
```

## **6. Demo: CREB Nuclear Segmentation and Motion-State Analysis**

A demonstration notebook (`CREB_One_Stop_SPT_end_to_end_demo.ipynb`) is provided to showcase a minimal analysis workflow using the CREB dataset in `test_data/`.

The demo performs:

1. **Nuclear segmentation** using a pretrained MaU-Net model.  
2. **Trajectory filtering** based on the nuclear mask.  
3. **RoC analysis** and CDF visualization.  
4. **Motion-state classification** of trajectories.
---

## **7. Project Structure**

```
One-Stop-SPT/
├── SPTpy/                           # Python package; module name retained for compatibility
│   ├── __init__.py
│   ├── automated_spt_processor.py
│   ├── MonteCarloParams_1_gap.mat
│   ├── msd_analyzer.py
│   ├── radius_calculator.py
│   ├── rc_rg_combined_auto.py
│   ├── SPTpy.py                     # Main GUI application
│   ├── spoton_core/                 # Spot-On backend 
│   ├── spoton_core.egg-info/
│   ├── track_processor.py
│   └── unet_attention_model.py      # MaU-Net segmentation model
│
├── test_data/                       # Example dataset for demo
│   ├── MaU-Net.pth                  # Pretrained segmentation model
│   ├── segmentation_mask.npy        # Saved output mask
│   ├── SMI-293T-CREB-1-JF549_2D_561nm_200mw_10ms_3_pos1_frame1_raw.png
│   ├── SMI-293T-CREB-1-JF549_2D_561nm_200mw_10ms_3_pos1_locs.txt
│   ├── SMI-293T-CREB-1-JF549_2D_561nm_200mw_10ms_3_pos1_locs_render_image.png
│   ├── SMI-293T-CREB-1-JF549_2D_561nm_200mw_10ms_3_pos1_locs_scatter_plot.png
│   └── SMI-293T-CREB-1-JF549_2D_561nm_200mw_10ms_3_pos1_filtered_table.txt
│
├── CREB_One_Stop_SPT_end_to_end_demo.ipynb           # demo pipeline
├── LICENSE
├── README.md
├── requirements.txt
└── .gitignore
```
---

## **8. Example Datasets**

### **Zenodo Archive**

The datasets used in the manuscript have been deposited on Zenodo:

**📦 Zenodo DOI:** https://doi.org/10.5281/zenodo.17783061

To comply with size limitations and data-sharing constraints, **raw TIFF image stacks are not included** in this archive.  
Instead, the Zenodo dataset contains the processed results and intermediate files required to fully reproduce our analyses.

The archive includes the following three components:

#### **1. CREB SPT Dataset**

- Single-molecule localization results  
- Trajectory files used for diffusion, RoC, and motion-state analysis  
- Rendered localization density maps  


#### **2. Cohesin-Loss Dataset**

- Localization and trajectory files for histones (H2B, H2A.Z)  
- Transcriptional regulators (OCT4, BRD4, MED1, MED6, TBP)  
- Processed data used in the manuscript to analyze diffusion behavior, confinement, and condensate transitions  

#### **3. MaU-Net Training and Validation Dataset**

- Training set used for MaU-Net (Gray / Render / Scatter inputs with corresponding nuclear masks)  
- Validation set used for model selection and performance evaluation  
- Pre-processed grayscale image frames and their associated Render / Scatter channels  
- Manually annotated nuclear masks (DAPI-based ground truth)  
- Best-performing MaU-Net model checkpoint selected based on validation loss


These datasets contain all information necessary to reproduce the analyses presented in the manuscript.

---

## **9. Citation**

If you use One-Stop SPT for your research, please cite:

```bibtex
@article{Liao2025OneStopSPT,
  title={One-Stop SPT: An Integrated Python Toolkit for One-Stop Analysis of Live-Cell Single-Particle Tracking Data},
  author={Liao, Shasha and Yang, Xin and Wang, Jinhong and Zhu, Hongni and Song, Yi and Liu, Yajie and Dong, Peng},
  journal={Bioinformatics},
  year={2026},
}
```

---

## **10. License**

Distributed under the **MIT License**.

---

## **11. Contact**

For questions, data requests, or collaboration:

**Peng Dong**  
Shenzhen Institutes of Advanced Technology, Chinese Academy of Sciences  
📧 p.dong@siat.ac.cn
