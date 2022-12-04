from helper_classes import CustomDecoder, ExperimentRunner

class ExperimentOne:

    def __init__(self, num_exp="exp1", rule="known"):
        base_path = "td_corpus_digits/SNR35dB/man/seq"
        self.output_path = "outputs/"
        self.rule = rule
        self.seqs = [1, 3, 5]
        self.paths = [base_path + "1digit_200_files", base_path + "3digits_100_files", base_path + "5digits_100_files"]    
        self.num_exp = num_exp  # exp1

    def known_seq(self, n, path_idx):
        # seq_1     
        custom_decoder = CustomDecoder(self.paths[path_idx])
        custom_decoder.decoder = "digits.seq" + str(n)
        refs, hyps = zip(*custom_decoder.hyps_generator())

        ref_path = self.output_path + f"seq{n}_{self.num_exp}.ref"
        hyp_path = self.output_path + f"seq{n}_{self.num_exp}.hyp"
        res_path = self.output_path + f"seq{n}_{self.num_exp}.res"
        return refs, hyps, [ref_path, hyp_path, res_path]



    def overall_known_seq(self):
        all_refs = []
        all_hyps = []
        results_dict = {}
        for i, seq in enumerate(self.seqs):
            refs, hyps, paths = self.known_seq(seq, i)
            ref_path, hyp_path, res_path = paths
            self.store_output(refs, ref_path)
            self.store_output(hyps, hyp_path)
            exp_seq = ExperimentRunner(ref_path, hyp_path, res_path)
            exp_seq.result_gen()
            res = exp_seq.confidence_interval()
            results_dict.setdefault(f"seq_{self.seqs[i]}", res)
            all_refs.extend(refs)
            all_hyps.extend(hyps)


        overall_ref = self.output_path + f"overall_known_{self.num_exp}.ref"
        overall_hyp = self.output_path + f"overall_known_{self.num_exp}.hyp"
        overall_res = self.output_path + f"overall_known_{self.num_exp}.res"
        self.store_output(all_refs, overall_ref)
        self.store_output(all_hyps, overall_hyp)
        exp_all = ExperimentRunner(overall_ref, overall_hyp, overall_res)
        exp_all.result_gen()
        overall_res = exp_all.confidence_interval()
        results_dict.setdefault("overall", overall_res)
        return results_dict

    def other_seq_loop(self):

        overall_refs = []
        overall_hyps = []
        results_dict = {}
        for i in range(len(self.paths)):
            custom_decoder = CustomDecoder(self.paths[i])
            custom_decoder.decoder = self.rule  # n_gram and seq_unk
            refs, hyps = zip(*custom_decoder.hyps_generator())
            ref_path = self.output_path + self.rule + f"_exp1_seq{self.seqs[i]}.ref" 
            hyp_path = self.output_path + self.rule + f"_exp1_seq{self.seqs[i]}.hyp" 
            res_path = self.output_path + self.rule + f"_exp1_seq{self.seqs[i]}.res" 
            self.store_output(refs, ref_path)
            self.store_output(hyps, hyp_path)
            exp_seq = ExperimentRunner(ref_path, hyp_path, res_path)
            exp_seq.result_gen()
            res = exp_seq.confidence_interval()
            results_dict.setdefault(f"seq_{self.seqs[i]}", res)
            overall_refs.extend(refs)
            overall_hyps.extend(hyps)
        

        overall_ref_path = self.output_path + self.rule + "exp1_overall.ref"
        overall_hyp_path = self.output_path + self.rule + "exp1_overall.hyp"
        overall_res_path = self.output_path + self.rule + "exp1_overall.res"
        self.store_output(overall_refs, overall_ref_path)
        self.store_output(overall_hyps, overall_hyp_path)
        overall = ExperimentRunner(overall_ref_path, overall_hyp_path, overall_res_path)
        overall.result_gen()
        overall_res = overall.confidence_interval()
        results_dict.setdefault("overall", overall_res)
        return results_dict


    def store_output(self, output, path):  # .ref or .hyp path = "outputs/data"
        # could be a shell line?        
        data = '\n'.join(output)

        with open(path, 'w') as f: 
            f.writelines(data)
        f.close()
    

