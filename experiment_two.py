from helper_classes import CustomDecoder, ExperimentRunner
from experiment_one import ExperimentOne

class ExperimentTwo(ExperimentOne):

    def __init__(self, gender, num_exp="exp2"):
        base_path = "td_corpus_digits/SNR35dB/" + gender + "/seq"
        #base_path = "td_corpus_digits/SNR35dB/man/seq"
        self.output_path = "outputs/"
        self.gender = gender
        self.num_exp = num_exp
        self.seqs = [1, 3, 5]
        self.paths = [base_path + "1digit_200_files", base_path + "3digits_100_files", base_path + "5digits_100_files"]    


    def known_seq(self, n, path_idx):
        # seq_1     
        custom_decoder = CustomDecoder(self.paths[path_idx])
        custom_decoder.decoder = "digits.seq" + str(n)
        refs, hyps = zip(*custom_decoder.hyps_generator())

        ref_path = self.output_path + f"seq{n}_{self.gender}_{self.num_exp}.ref"
        hyp_path = self.output_path + f"seq{n}_{self.gender}_{self.num_exp}.hyp"
        res_path = self.output_path + f"seq{n}_{self.gender}_{self.num_exp}.res"
        return refs, hyps, [ref_path, hyp_path, res_path]


    def overall_known_seq(self):

        all_refs = []
        all_hyps = []
        res_dict = {}
        for i, seq in enumerate(self.seqs):
            refs, hyps, paths = self.known_seq(seq, i)
            ref_path, hyp_path, res_path = paths
            self.store_output(refs, ref_path)
            self.store_output(hyps, hyp_path)
            exp_seq = ExperimentRunner(ref_path, hyp_path, res_path)
            exp_seq.result_gen()
            res = exp_seq.confidence_interval()
            res_dict.setdefault(f"seq_{seq}", res)
            all_refs.extend(refs)
            all_hyps.extend(hyps)

        overall_ref = self.output_path + f"overall_known_{self.gender}_{self.num_exp}.ref"
        overall_hyp = self.output_path + f"overall_known_{self.gender}_{self.num_exp}.hyp"
        overall_res = self.output_path + f"overall_known_{self.gender}_{self.num_exp}.res"

        self.store_output(all_refs, overall_ref)
        self.store_output(all_hyps, overall_hyp)
        exp_all = ExperimentRunner(overall_ref, overall_hyp, overall_res)
        exp_all.result_gen()
        overall_res = exp_all.confidence_interval()
        res_dict.setdefault("overall", overall_res)
        return res_dict
