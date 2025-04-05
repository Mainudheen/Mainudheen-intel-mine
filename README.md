# 🔍 Intel Bug Detection Hub

[![Deployment Status](https://img.shields.io/badge/Model-Hugging_Face-success)](https://huggingface.co/MainuDheen/intel-bug-detection)
[![GitHub](https://img.shields.io/badge/Repository-GitHub-blue)](https://github.com/Mainudheen/Mainudheen-intel-mine)

> Advanced code analysis powered by AI - detect bugs, analyze vulnerabilities, get intelligent fixes

## 🚀 Quick Start

### Option 1: Use the Model Directly (Recommended)

The model is fully deployed and ready to use:
- **Model**: Available at [Hugging Face Hub](https://huggingface.co/MainuDheen/intel-bug-detection)
- **Size**: 475.52 MB
- **Performance**: 94% accuracy on test set

### Option 2: Run Locally

```bash
# Clone the repository
git clone https://github.com/Mainudheen/Mainudheen-intel-mine.git

# Navigate to project directory
cd Mainudheen-intel-mine

# Install dependencies
pip install -r requirements.txt

# Download model
# Place model.safetensors in bug_detector_model/

# Commands to run
python bug-detection.py
```

---

### ML Model Access

> ⚠️ **Important**: The model must be downloaded from Hugging Face for optimal performance.

To access the model:
1. Visit [intel-bug-detection](https://huggingface.co/MainuDheen/intel-bug-detection)
2. Download `model.safetensors`
3. Place in `bug_detector_model/` directory

## 🌟 Key Features

- **AI-Powered Bug Detection** - Get intelligent insights from code analysis
- **Multi-Language Support** - Python
- **Real-time Analysis** - Quick and efficient code scanning
- **Detailed Reports** - Comprehensive bug analysis and fix suggestions

---

## 🏗️ Architecture

The project uses a two-tier architecture:

1. **Frontend**: Web interface with templates and static assets
2. **ML Backend**: PyTorch with Transformer models



## 📋 Documentation

Required environment setup:

#### Python Environment
```python
# Required packages in requirements.txt
torch>=1.9.0
transformers>=4.0.0
numpy>=1.19.5
pandas>=1.3.0
```

## 🔄 Project Structure


```bash
intel-mine/
├── bug_detector_model/              # Model and inference code
│   ├── model.safetensors           # Main model file (475.52 MB)
│   └── config.json                 # Model configuration
│
├── errors/                         # Error handling
│   ├── __init__.py
│   └── error_handlers.py
│
├── static/                         # Static assets
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
│       └── architecture.png
│
├── templates/                      # HTML templates
│   ├── index.html
│   ├── results.html
│   └── error.html
│
├── webapp/                         # Web application
│   ├── __init__.py
│   ├── routes.py
│   └── utils.py
│
├── input/                         # Input code files
│   └── sample_test.py
│
├── results/                       # Analysis output
│   └── bug_reports/
│
├── .gitignore                     # Git ignore file
├── README.md                      # Project documentation
├── requirements.txt               # Project dependencies
└── bug-detection.py              # Main application script
```

