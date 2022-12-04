# How to run?

Create a *td_corpus_digit* in the main directory. Therein 4 folders should contain different noise levels and speaker per folder. Each speaker, regardless of sequence, must contain reference and raw audio files.

```bash
td_corpus_digits
├── SNR05dB
│   └── man
│       ├── seq1digit_200_files
│       ├── seq3digits_100_files
│       └── seq5digits_100_files
├── SNR15dB
│   └── man
│       ├── seq1digit_200_files
│       ├── seq3digits_100_files
│       └── seq5digits_100_files
├── SNR25dB
│   └── man
│       ├── seq1digit_200_files
│       ├── seq3digits_100_files
│       └── seq5digits_100_files
└── SNR35dB
    ├── boy
    │   ├── seq1digit_200_files
    │   ├── seq3digits_100_files
    │   └── seq5digits_100_files
    ├── girl
    │   ├── seq1digit_200_files
    │   ├── seq3digits_100_files
    │   └── seq5digits_100_files
    ├── man
    │   ├── seq1digit_200_files
    │   ├── seq3digits_100_files
    │   └── seq5digits_100_files
    └── woman
        ├── seq1digit_200_files
        ├── seq3digits_100_files
        └── seq5digits_100_files
```


Run this project by simply passing...
```python
python main.py -s no
```
If you want to save the output in a csv, change the argument from *no* to *yes*. The python script has been created with a helpful informative message in case of passing the wrong value to the -s option, so do not fret.

Output csv file is not stored in the outputs directory as the references, hypotheses, and results files are stored in said folder. The csv will always be stored in the main directory.

Please only run this script from the main directory as paths have been defined based on current working tree.

# Requirements

This project has only been tested in unix-based systems. Do not run from windows, unless you are on WSL. Please remember to install the following packages on your linux distribution to run the word error rates
```bash
sudo apt install swig
sudo apt install gcc
sudo apt install libpulse −dev
sudo apt install libasound2 −dev
```
This project uses an older version of pocketsphinx and pandas for storing the output data. Therefore, it is highly advisable to install the requirements file.


# Important files

Model, grammar, and lexicons can be found in the ps\_data directory. 
```bash
ps_data
├── example
├── jsgf
├── lex
├── lm
└── model
    └── en-us
```

