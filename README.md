# **One-Stop SPT: An Integrated Python Toolkit for Comprehensive Live-Cell Single-Particle Tracking Analysis**

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
- Multiple-target tracing (MTT) with likelihood-based reconnection and gap handling
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

- Frame-by-frame TIFF processing for large image stacks
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
| **Operating System** | Windows 10 or higher; macOS; Linux                |
| **Python Version**   | Python ≥ 3.10; Python 3.11 recommended             |
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

Use a Python installation with Tkinter support. Python 3.11 is recommended for the installation steps below.

**macOS/Linux** (use the Python 3.11 executable available on your machine)

```bash
python3.11 -m venv .venv
```

**Windows** (with the Python launcher and Python 3.11 installed)

```powershell
py -3.11 -m venv .venv
```

**Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

For Windows Command Prompt, use `.venv\Scripts\activate.bat`.

**Linux/macOS**

```bash
source .venv/bin/activate
```

**Option B: Conda environment**

```bash
conda create -n one-stop-spt python=3.11 pip tk
conda activate one-stop-spt
```

### **3. Check GUI support and install dependencies**

After activating the environment, check that Python can open a Tk window:

```bash
python -m tkinter
```

Close the test window to continue. If this fails, install Tk support for the **same Python interpreter** or use the Conda environment above. Installing project requirements does not install Tkinter. A graphical desktop session is required to launch the GUI.

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

### **4. Install core algorithm package**

```bash
python -m pip install -e ./SPTpy
python -m pip check
```

First startup may take longer while libraries initialize and Matplotlib builds its font cache.

---

## **5. Usage**

One-Stop SPT is primarily used through its graphical interface.  
Launch the GUI according to your current working directory:

The public toolkit name is One-Stop SPT; the Python module name remains `SPTpy`
for compatibility with the current package structure.

**From the repository root directory**

```bash
python SPTpy/SPTpy.py
```

**From inside the `SPTpy` package directory**

```bash
python SPTpy.py
```

## **6. Demo: CREB Segmentation and Biophysical Analysis**

Open `CREB_One_Stop_SPT_end_to_end_demo.ipynb` from the repository root. Install the optional notebook kernel in the same environment as the application:

```bash
python -m pip install ipykernel
```

In VS Code, select that Python environment as the notebook kernel. Restart the kernel and run all cells after changing imported Python code.

The demo performs:

1. Validate and inspect matched raw-frame, localization, render, and scatter inputs.
2. Predict a nuclear mask using the pretrained MaU-Net checkpoint.
3. Filter precomputed trajectory points by the nuclear mask.
4. Compute Spot-On jump-length distributions, fit kinetic parameters, and plot the fit.
5. Group existing trajectories, compute MSD and RoC, and visualize the RoC CDF.
6. Classify motion from local density and trajectory endpoint states.
7. Export results and analysis settings to `test_data/demo_outputs/`.

The notebook calls the current `SPTpy.py` Spot-On and motion-classification methods and shares segmentation preprocessing with the GUI. Use matching input files and parameter settings to compare results. The CREB frame interval is **0.01 seconds (10 ms)**; Spot-On's GUI time field is in milliseconds, while the RoC GUI field is in seconds.

The example uses **precomputed trajectories**, not the complete raw TIFF stack. It does not rerun localization or MTT linking. Filtering existing trajectories after segmentation differs from filtering localizations before tracking in the GUI; demo results need not equal the full manuscript analysis.

### Required demo inputs

Place these files in `test_data/` before running the notebook:

- `MaU-Net.pth`
- `SMI-293T-CREB-1-JF549_2D_561nm_200mw_10ms_active_64_pos1.png`
- `SMI-293T-CREB-1-JF549_2D_561nm_200mw_10ms_active_64_pos1_locs.txt`
- `SMI-293T-CREB-1-JF549_2D_561nm_200mw_10ms_active_64.png`
- `SMI-293T-CREB-1-JF549_2D_561nm_200mw_10ms_active_64_scatter_plot.png`
- `SMI-293T-CREB-1-JF549_2D_561nm_200mw_10ms_active_64_pos1_table.txt`

Large datasets and model weights may need to be obtained separately; do not assume they are included in every checkout. The notebook reports missing inputs before starting analysis.

## **7. Example Datasets**

### **Figshare Archive**

The datasets used in the manuscript have been deposited on Figshare:

**📦 Figshare DOI:** https://doi.org/10.6084/m9.figshare.33842287

The archive includes **two raw microscopy TIFF stacks**, localization and trajectory data, and MaU-Net segmentation datasets and model weights for live-cell single-particle tracking analysis.

The two raw microscopy TIFF stacks are hosted on Figshare because they exceed GitHub’s per-file size limit: https://doi.org/10.6084/m9.figshare.33842287

---

## **8. Citation**

The manuscript is being prepared for resubmission. The following is a provisional reference to the unpublished manuscript; replace it with the verified publication citation when available. Do not assign a journal before publication details are confirmed.

```bibtex
@misc{LiaoOneStopSPT,
  title={One-Stop SPT: An Integrated Python Toolkit for Comprehensive Live-Cell Single-Particle Tracking Analysis},
  author={Liao, Shasha and Yang, Xin and Wang, Jinhong and Zhu, Hongni and Song, Yi and Liu, Yajie and Lei, Zhengyang and Dong, Peng},
  note={Unpublished manuscript}
}
```

---

## **9. License**

Distributed under the **MIT License**.

---

## **10. Contact**

For questions, data requests, or collaboration:

**Peng Dong**  
Shenzhen Institutes of Advanced Technology, Chinese Academy of Sciences  
📧 p.dong@siat.ac.cn
