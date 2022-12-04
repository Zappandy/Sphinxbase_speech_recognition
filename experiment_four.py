from helper_classes import CustomDecoder, ExperimentRunner
from experiment_one import ExperimentOne

class ExperimentFour(ExperimentOne):

    def __init__(self, num_exp="exp4"):
        base_path = "td_corpus_digits/"
        self.audio_paths = [base_path + f"SNR{i}5dB/man/seq" for i in range(4)]
        self.output_path = "outputs/"
        self.num_exp = num_exp
        self.end_paths = ["1digit_200_files", "3digits_100_files", "5digits_100_files"]    

    def audio_lvl_exps(self):
        
        seq = [1, 3, 5]
        total_dict = {}
        for n, audio in enumerate(self.audio_paths):
            overall_refs = []
            overall_hyps = []
            snr_path = "SNR" + str(n) + "5dB"

            res_dict = {}
            for i, path in enumerate(self.end_paths):
                noise_level_decoder = CustomDecoder(audio + path)
                noise_level_decoder.decoder = "digits.seq" + str(seq[i])
                refs, hyps = zip(*noise_level_decoder.hyps_generator())
                ref_path = self.output_path + f"seq{seq[i]}_{snr_path}_{self.num_exp}.ref"
                hyp_path = self.output_path + f"seq{seq[i]}_{snr_path}_{self.num_exp}.hyp"
                res_path = self.output_path + f"seq{seq[i]}_{snr_path}_{self.num_exp}.res"
                self.store_output(refs, ref_path)
                self.store_output(hyps, hyp_path)
                exp_seq = ExperimentRunner(ref_path, hyp_path, res_path)
                exp_seq.result_gen()
                res = exp_seq.confidence_interval()
                res_dict.setdefault(f"seq_{seq[i]}", res)
                overall_refs.extend(refs)
                overall_hyps.extend(hyps)

            overall_ref_path = self.output_path + f"overall_{snr_path}_{self.num_exp}.ref"
            overall_hyp_path = self.output_path + f"overall_{snr_path}_{self.num_exp}.hyp"
            overall_res_path = self.output_path + f"overall_{snr_path}_{self.num_exp}.res"
            self.store_output(overall_refs, overall_ref_path)
            self.store_output(overall_hyps, overall_hyp_path)
            overall_exp = ExperimentRunner(overall_ref_path, overall_hyp_path, overall_res_path)
            overall_exp.result_gen()
            overall_res = overall_exp.confidence_interval()
            res_dict.setdefault("overall", overall_res)
            total_dict.setdefault(snr_path, res_dict)
        return total_dict