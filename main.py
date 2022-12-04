from experiment_one import ExperimentOne
from experiment_two import ExperimentTwo
from experiment_three import ExperimentThree
from experiment_four import ExperimentFour
import pandas as pd  # pip3 install pandas


def main():
    print('-'*5 + "Experiment 1" '-'*5)
    res_dict = {}
    not_knownseq_rules = ["digits.seq_unk", "n_gram"]
    for rule in not_knownseq_rules:
        lang_model = ExperimentOne(rule=rule)
        res_dict.setdefault(rule, lang_model.other_seq_loop())
    known_Seq = ExperimentOne()
    res_dict.setdefault("known_seqs", known_Seq.overall_known_seq())
    exp1_df = pd.DataFrame(res_dict).T
    exp1_idx = [1 for i in range(exp1_df.shape[0])]
    #df.insert(0, )

    print('-'*5 + "Experiment 2" '-'*5)
    res_dict = {}
    speakers = ["boy", "girl", "woman", "man"]
    for speaker in speakers:
        spkr = ExperimentTwo(speaker)
        res = spkr.overall_known_seq()
        res_dict.setdefault(speaker, res)

    print('-'*5 + "Experiment 3" '-'*5)
    adults = ExperimentThree()
    res_dict.setdefault("adults", adults.adult_exps())
    exp2_df = pd.DataFrame(res_dict).T
    exp2_idx = [2 for i in range(4)]
    exp3_idx = [3]
    
    print('-'*5 + "Experiment 4" '-'*5)
    noise_levels = ExperimentFour()
    exp_4_dict = noise_levels.audio_lvl_exps()
    exp4_df = pd.DataFrame(exp_4_dict).T
    exp4_idx = ["exp_4" for i in range(exp4_df.shape[0])]
    exp4_idx = [4 for i in range(exp4_df.shape[0])]
    
    exp_idx = exp1_idx + exp2_idx + exp3_idx + exp4_idx
    total_df = pd.concat([exp1_df, exp2_df, exp4_df], ignore_index=False)
    new_idx = total_df.index
    total_df.reset_index(drop=True)
    total_df.insert(0, "experiment", exp_idx)
    total_df.insert(1, "setup", new_idx)
    total_df.to_csv("ASR_Experimental_Results.csv", index=False)

if __name__ == "__main__":
    main()
