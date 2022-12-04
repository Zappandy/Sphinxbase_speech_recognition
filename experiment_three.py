from helper_classes import CustomDecoder, ExperimentRunner
from experiment_one import ExperimentOne

class ExperimentThree(ExperimentOne):

    def __init__(self, num_exp="exp3"):
        man_path = "td_corpus_digits/SNR35dB/man/seq"
        woman_path = "td_corpus_digits/SNR35dB/woman/seq"
        self.output_path = "outputs/"
        self.num_exp = num_exp
        self.man_paths = [man_path + "1digit_200_files", man_path + "3digits_100_files", man_path + "5digits_100_files"]    
        self.woman_paths = [woman_path + "1digit_200_files", woman_path + "3digits_100_files", woman_path + "5digits_100_files"]    

    def adult_exps(self):
        
        overall_refs = []
        overall_hyps = []
        res_dict = {}
        seq = [1, 3, 5]
        for i, (man, woman) in enumerate(zip(self.man_paths, self.woman_paths)):
                man_decoder = CustomDecoder(man)
                woman_decoder = CustomDecoder(woman)
                man_decoder.decoder = "digits.seq" + str(seq[i])
                woman_decoder.decoder = "digits.seq" + str(seq[i])
                man_refs, man_hyps = zip(*man_decoder.hyps_generator())
                woman_refs, woman_hyps = zip(*woman_decoder.hyps_generator())
                refs = man_refs + woman_refs
                hyps = man_hyps + woman_hyps
                ref_path = self.output_path + f"seq{seq[i]}_adults_{self.num_exp}.ref"
                hyp_path = self.output_path + f"seq{seq[i]}_adults_{self.num_exp}.hyp"
                res_path = self.output_path + f"seq{seq[i]}_adults_{self.num_exp}.res"
                self.store_output(refs, ref_path)
                self.store_output(hyps, hyp_path)
                exp_seq = ExperimentRunner(ref_path, hyp_path, res_path)
                exp_seq.result_gen()
                res = exp_seq.confidence_interval()
                res_dict.setdefault(f"seq_{seq[i]}", res)
                overall_hyps.extend(hyps)
                overall_refs.extend(refs)


        overall_ref_path = self.output_path + f"overall_adults_{self.num_exp}.ref"
        overall_hyp_path = self.output_path + f"overall_adults_{self.num_exp}.hyp"
        overall_res_path = self.output_path + f"overall_adults_{self.num_exp}.res"

        self.store_output(overall_refs, overall_ref_path)
        self.store_output(overall_hyps, overall_hyp_path)
        overall_exp = ExperimentRunner(overall_ref_path, overall_hyp_path, overall_res_path)
        overall_exp.result_gen()
        overall_res = overall_exp.confidence_interval()
        res_dict.setdefault("overall", overall_res)
        return res_dict