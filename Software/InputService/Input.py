from InputService.ReadFiles import ReadFiles
from datastructures.Assertion import Assertion
from datastructures.exceptions.InputException import InputException
import logging, copy

class Input:
    """
    Main class of InputService.
    Class that is called to read the input dataset.
    """

    cache = dict()
    
    def getInput(self, filePath:str):
        """
        Get the dataset located at 'filePath' divided into test and training data.
        If the dataset has been read before, it is cached in 'cache'.
        """
        if not filePath in Input.cache.keys():
            result = self._readInput(filePath)
            Input.cache[filePath] = result
        return copy.deepcopy(Input.cache[filePath])
            
    def _readInput(self, filePath:str):

        rf = ReadFiles()

        result = []
        # if (filePath.endswith(".csv")):
        #     df = rf.getCsv(filePath)
        #     result = self.parseTriples(df)
        #     logging.info("Read {} assertions".format(len(result)))
        #     return result,result
        # elif (filePath.endswith(".tsv")):
        #
        # elif(str(filePath).lower().find("favel") != -1):
        #     df_train, df_test = rf.getFavel(filePath)
        # elif(str(filePath).lower().find("factbench") != -1):
        #     df_train, df_test = rf.getFactbench(filePath)
        # elif(str(filePath).lower().find("bpdp") != -1):
        #     df_train, df_test = rf.getBPDP(filePath)
        # else:
        #     df_train = rf.getCsv(filePath+"/train.csv")
        #     df_test = rf.getCsv(filePath+"/test.csv")

        #####
        # df_train = rf.getTsv(filePath + "bpdp_train_full.tsv")
        # df_test = rf.getTsv(filePath + "bpdp_test_full.tsv")

        # df_train = rf.getTsv(filePath + "factbench_train_full.tsv")
        # df_test = rf.getTsv(filePath + "factbench_test_full.tsv")

        df_train = rf.getTsv(filePath + "favel_train_full.tsv")
        df_test = rf.getTsv(filePath + "favel_test_full.tsv")
        #####

        result_train = self.parseTriples(df_train)
        result_test = self.parseTriples(df_test)
        if len(result_train) == 0 or len(result_test) == 0:
            raise InputException("The specified dataset does not contain any assertions.")
        logging.info("Read {} training assertions, {} testing assertions".format(len(result_train),len(result_test)))
        return result_train, result_test
            
    def parseTriples(self, df):
        result = []
        for i, row in df.iterrows():
            a = Assertion(row['subject'], row['predicate'], row['object'])
            a._expectedScore = row['truth']
            a.score['adamic_adar'] = row['adamic_adar']
            a.score['degree_product'] = row['degree_product']
            a.score['jaccard'] = row['jaccard']
            a.score['katz'] = row['katz']
            a.score['kl'] = row['kl']
            a.score['kl_rel'] = row['kl_rel']
            a.score['ks'] = row['ks']
            a.score['pathent'] = row['pathent']
            a.score['predpath'] = row['predpath']
            a.score['simrank'] = row['simrank']
            a.score['pra'] = row['pra']
            a.score['esther'] = row['esther']
            a.score['copaal'] = row['copaal']
            result.append(a)
        return result
