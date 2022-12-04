import subprocess
import math
import re
from my_functions import find_files, create_decoder_ngram, create_decoder_digit

class CustomDecoder:

    def __init__(self, path):
        self.folder_path = path
        self._decoder = None

    @property
    def decoder(self):
        return self._decoder

    @decoder.setter
    def decoder(self, rule):
        """
        lang_model is always a str that can be
        'n_gram', 'seq_unk', 'seq1', 'seq3', and 'seq5'
        """
        if rule == "n_gram":
            self._decoder = create_decoder_ngram()
        else:
            self._decoder = create_decoder_digit(rule)

    def start_decoder(self, file_path, verbose=True):
        assert self._decoder != None, "A decoder has not been defined"
        decoder = self._decoder
        self._decoder.start_utt()
        stream = open(file_path, 'rb')
        uttbuf = stream.read(-1)
        if uttbuf:
            decoder.process_raw(uttbuf, False, True)
        else:
            print("error reading speech data")
            exit()  # raise systemexit
        decoder.end_utt()
        
        if decoder.hyp() is None:
            best_hypothesis = ''
        else:
            best_hypothesis = decoder.hyp().hypstr
        if verbose:
            print(f"Best hypothesis {best_hypothesis}\nmodel_score {decoder.hyp().best_score}")
    
        return best_hypothesis


    def hyps_generator(self):

        raw_files = find_files(self.folder_path)
        ref_files = find_files(self.folder_path, pattern="*.ref")

        references = []
        hyp_list = []
        for ref, raw in zip(ref_files, raw_files):
            with open(ref, 'r') as f:
                nums = f.read()
                references.append(nums.strip())
            best_hyp = self.start_decoder(raw, False)
            hyp_list.append(best_hyp)

        #hyp_list = [self.start_decoder(raw, False) for raw in raw_files]
        return list(zip(references, hyp_list))


class ExperimentRunner:
    #TODO: Add a rep and a str to clean result output

    def __init__(self, ref_file, hyp_file, out_file, verbose=False):

        """
        command reference
        shell_line = "wer outputs/data.ref outputs/data.hyp > outputs/data.res"  # -i
        """
        self.command = "wer -i".split()
        self.command = self.command[:-1] if not verbose else self.command
        self.command.extend([ref_file, hyp_file])
        self.result = None
        self.out_file = out_file

    def result_gen(self, store=True):
        if store:
            with open(self.out_file, "w") as f:
                output = subprocess.run(self.command, stdout=f)  # capturing not poss or text when stdout?

            with open(self.out_file, "r") as f:
                self.result = f.readlines()
            self.result = [line.strip() for line in self.result]
        else:
            output = subprocess.run(self.command, capture_output=True, text=True)
            self.result = output.stdout.split("\n")
            #print("err\n", result.stderr)

    def confidence_interval(self, constant=1.96):
        probsRegex = re.compile(r"(\d+\.\d+)(%)")
        numsRegex = re.compile(r"(\d+)(\)$)")
        errorRegex = re.compile(r"^(\w+)")
        confidence_intervals = {}
        for line in self.result:
            probs_mo = probsRegex.search(line)
            nums_mo = numsRegex.search(line)
            if not probs_mo or not nums_mo:
                #print("No valid line -- skipping")  # sanity check! use logging instead
                continue
            else:
                error_mo = errorRegex.search(line)
                probs = float(probs_mo.group(1)) / 100
                num_words = int(nums_mo.group(1))
                ci = round(math.sqrt(probs/num_words) * constant, 3)
                confidence_intervals.setdefault(error_mo.group(1), {"CI": ci, "Percentage of errors": round(probs, 3), # "".join(probs_mo.groups())
                                                                    'N': num_words, 'P': round(probs, 3)})
        #return confidence_intervals["WER"]
        with open(self.out_file, 'a') as f:
            confidence = str(confidence_intervals["WER"]["Percentage of errors"]) + '±' + str(confidence_intervals["WER"]["CI"])   
            f.write(confidence)
        return confidence
        #return confidence_intervals["WER"]["Percentage of errors"], confidence_intervals["WER"]["CI"]