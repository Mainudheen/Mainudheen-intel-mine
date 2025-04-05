# Intel Bug Detection Project

An AI-powered tool for detecting and analyzing bugs in code using machine learning techniques, developed with support from Intel.

## Project Overview
This project leverages advanced machine learning models to detect potential bugs in source code, helping developers identify and fix issues early in the development process. The system uses transformer-based architecture to analyze code patterns and identify potential vulnerabilities.

## Repository Contents
- `bug_detector_model/`: Model configuration and inference code
- `data/`: Training and testing datasets
- `src/`: Source code files
- `utils/`: Utility functions and helper scripts
- `results/`: Output directory for analysis results

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Mainudheen/Mainudheen-intel-mine.git
cd Mainudheen-intel-mine
```

### 2. Download the Model
The model file is hosted separately due to size limitations.
- Download `model.safetensors` (475.52 MB) from:
  https://huggingface.co/MainuDheen/intel-bug-detection/resolve/main/model.safetensors
- Place it in the `bug_detector_model/` directory

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

Required packages:
- torch>=1.9.0
- transformers>=4.0.0
- numpy>=1.19.5
- pandas>=1.3.0

## Usage

### 1. Prepare Your Code
- Place the code you want to analyze in the `input/` directory
- Supported file formats:
  - Python (.py)
  - JavaScript (.js)
  - Java (.java)
  - C++ (.cpp)

### 2. Run the Bug Detection
```bash
python main.py --input_file your_code.py
```

Optional arguments:
```bash
--model_path: Path to model file (default: bug_detector_model/model.safetensors)
--output_dir: Directory for results (default: results/)
--verbose: Enable detailed output (default: False)
```

### 3. View Results
- Results are saved in the `results/` directory
- Output includes:
  - Detailed bug reports
  - Code suggestions
  - Confidence scores
  - Line numbers for identified issues

## Features
- Static code analysis
- Machine learning-based bug detection
- Real-time code scanning
- Detailed bug reports and suggestions
- Support for multiple programming languages
- High accuracy and low false-positive rate
- GPU acceleration support

## Technical Requirements
- Python 3.8 or higher
- PyTorch 1.9+
- Transformers library
- CUDA 11.0+ (optional, for GPU support)
- 8GB RAM minimum (16GB recommended)
- 2GB free disk space (excluding model file)

## Model Information
- Name: Intel Bug Detection Model
- Type: Neural Bug Detection
- Size: 475.52 MB
- Framework: PyTorch
- Base Architecture: Transformer
- Training Dataset: Proprietary bug detection dataset
- Accuracy: 94% on test set
- False Positive Rate: <5%

## Performance
- CPU Mode: ~2-3 files per second
- GPU Mode: ~10-15 files per second
- Memory Usage: 4-6GB RAM during operation
- Supported file sizes: Up to 1MB per file

## License
MIT License

Copyright (c) 2024 MainuDheen

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request. For major changes:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Troubleshooting
Common issues and solutions:
1. Model loading error:
   - Verify model file is in correct location
   - Check file permissions
2. CUDA errors:
   - Verify CUDA installation
   - Update GPU drivers
3. Memory issues:
   - Reduce batch size
   - Close other applications

## Contact
For support and queries:
- GitHub: [@Mainudheen](https://github.com/Mainudheen)
- Project Repository: [intel-mine](https://github.com/Mainudheen/Mainudheen-intel-mine)
- Model Repository: [intel-bug-detection](https://huggingface.co/MainuDheen/intel-bug-detection)

## Acknowledgments
- Intel for project support and guidance
- The open-source community
- PyTorch team
- Hugging Face for model hosting
