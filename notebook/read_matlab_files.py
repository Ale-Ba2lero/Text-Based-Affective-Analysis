import os
import numpy as np
import pandas as pd
import h5py
import data_loading_helpers as dh
import string

rootdir = '../dataset/Matlab files'
        

def getWordsValues():
    word_values = {}

    for file in os.listdir(rootdir):
        file_name = rootdir +'/'+ file
        f = h5py.File(file_name, 'r')

        sentence_data = f['sentenceData']
        rawData = sentence_data['rawData']
        wordData = sentence_data['word']

        for idx in range(len(rawData)):
            # get word level data
            word_data = dh.extract_word_for_analysis(f, f[wordData[idx][0]])
            for widx in range(len(word_data)):
                token = word_data[widx]['content']
                token = token.lower()
                token = token.strip(string.punctuation)
                token = token.split("'")[0]
                if not token.isnumeric():
                    if token not in word_values:
                        word_values[token] = {'GD':[], 'TRT':[], 'FFD':[], 'GPT':[], 'nFix':[], 'MPS':[]}
                        
                    if word_data[widx]['meanPupilSize'] is not None:
                        word_values[token]['MPS'].append(word_data[widx]['meanPupilSize'])

                    if word_data[widx]['TRT'] is not None:
                        word_values[token]['TRT'].append(word_data[widx]['TRT'])

                    if word_data[widx]['GD'] is not None:
                        word_values[token]['GD'].append(word_data[widx]['GD'])

                    if word_data[widx]['FFD'] is not None:
                        word_values[token]['FFD'].append(word_data[widx]['FFD'])
                        
                    #if word_data[widx]['SFD'] is not None:
                     #   word_values[token]['SFD'].append(word_data[widx]['SFD'])
                        
                    if word_data[widx]['GPT'] is not None:
                        word_values[token]['GPT'].append(word_data[widx]['GPT'])
                        
                    if word_data[widx]['nFixations'] is not None:
                        word_values[token]['nFix'].append(word_data[widx]['nFixations'])
    return word_values   

def getWordsMeanValues():
    word_values = getWordsValues()
    df = pd.DataFrame(columns=['Word', 'GD', 'TRT', 'FFD', 'GPT', 'nFix', 'MPS'])
    for word in word_values:
        mps = np.average(word_values[word]['MPS'])
        trt = np.average(word_values[word]['TRT'])
        gd = np.average(word_values[word]['GD'])
        ffd = np.average(word_values[word]['FFD'])
        gpt = np.average(word_values[word]['GPT'])
        nfix = np.average(word_values[word]['nFix'])
        #sfd = np.average(word_values[word]['SFD'])
        
        df.loc[len(df.index)] = [word, gd, trt, ffd, gpt, nfix, mps]
    return df

def getSentencesMeanValues():
    sentences_list = []
    firstDoc = True

    for file in os.listdir(rootdir):
        file_name = rootdir +'/'+ file
        f = h5py.File(file_name, 'r')

        #print(file_name)

        sentence_data = f['sentenceData']
        rawData = sentence_data['rawData']
        wordData = sentence_data['word']

        # indice per accesso diretto alla frase che ci serve
        idxSentences = 0 

        for idx in range(len(rawData)):
            # get word level data
            word_data = dh.extract_word_for_analysis(f, f[wordData[idx][0]])

            if firstDoc:
                word_values = {}

                # indice per accesso diretto a parola nella frase che ci serve
                idxWords = 0 

                for widx in range(len(word_data)):
                    token = word_data[widx]['content']
                    token = token.lower()
                    token = token.strip(string.punctuation)
                    token = token.split("'")[0]

                    if not token.isnumeric():
                        word_values[idxWords] = {'Word': [], 'MPS': [], 'TRT': [], 'GD': [], 'FFD': [], 'GPT':[], 'nFix':[]}
                        word_values[idxWords]['Word'].append(token)
                        if word_data[widx]['meanPupilSize'] is not None:
                            word_values[idxWords]['MPS'].append(word_data[widx]['meanPupilSize'])

                        if word_data[widx]['TRT'] is not None:
                            word_values[idxWords]['TRT'].append(word_data[widx]['TRT'])

                        if word_data[widx]['GD'] is not None:
                            word_values[idxWords]['GD'].append(word_data[widx]['GD'])

                        if word_data[widx]['FFD'] is not None:
                            word_values[idxWords]['FFD'].append(word_data[widx]['FFD'])
                            
                        if word_data[widx]['GPT'] is not None:
                            word_values[idxWords]['GPT'].append(word_data[widx]['GPT'])
                        
                        if word_data[widx]['nFixations'] is not None:
                            word_values[idxWords]['nFix'].append(word_data[widx]['nFixations'])

                        idxWords += 1

                sentences_list.append(word_values)
            else:
                idxWords = 0

                # se nella lista frase all'indice idxSentences presente prelevo valori parola per parola e li aggiungo
                if sentences_list[idxSentences] != {}: 
                    for widx in range(len(word_data)):

                        token = word_data[widx]['content']
                        token = token.lower()
                        token = token.strip(string.punctuation)
                        token = token.split("'")[0]
                        if not token.isnumeric():

                            if word_data[widx]['meanPupilSize'] is not None:
                                sentences_list[idxSentences][idxWords]['MPS'].append(word_data[widx]['meanPupilSize'])

                            if word_data[widx]['TRT'] is not None:
                                sentences_list[idxSentences][idxWords]['TRT'].append(word_data[widx]['TRT'])

                            if word_data[widx]['GD'] is not None:
                                sentences_list[idxSentences][idxWords]['GD'].append(word_data[widx]['GD'])

                            if word_data[widx]['FFD'] is not None:
                                sentences_list[idxSentences][idxWords]['FFD'].append(word_data[widx]['FFD'])
                            
                            if word_data[widx]['GPT'] is not None:
                                sentences_list[idxSentences][idxWords]['GPT'].append(word_data[widx]['GPT'])
                            
                            if word_data[widx]['nFixations'] is not None:
                                sentences_list[idxSentences][idxWords]['nFix'].append(word_data[widx]['nFixations'])

                            idxWords += 1

                # se nella lista frase all'indice idxSentences NON presente aggiungo frase alla lista in quella posizione
                else:
                    word_values = {}
                    for widx in range(len(word_data)):

                        token = word_data[widx]['content']
                        token = token.lower()
                        token = token.strip(string.punctuation)
                        token = token.split("'")[0]
                        if not token.isnumeric():

                            word_values[idxWords] = {'Word': [], 'MPS': [], 'TRT': [], 'GD': [], 'FFD': [], 'GPT':[], 'nFix':[]}
                            word_values[idxWords]['Word'].append(token)
                            if word_data[widx]['meanPupilSize'] is not None:
                                word_values[idxWords]['MPS'].append(word_data[widx]['meanPupilSize'])

                            if word_data[widx]['TRT'] is not None:
                                word_values[idxWords]['TRT'].append(word_data[widx]['TRT'])

                            if word_data[widx]['GD'] is not None:
                                word_values[idxWords]['GD'].append(word_data[widx]['GD'])

                            if word_data[widx]['FFD'] is not None:
                                word_values[idxWords]['FFD'].append(word_data[widx]['FFD'])
                            
                            if word_data[widx]['GPT'] is not None:
                                word_values[idxWords]['GPT'].append(word_data[widx]['GPT'])
                            
                            if word_data[widx]['nFixations'] is not None:
                                word_values[idxWords]['nFix'].append(word_data[widx]['nFixations'])

                            idxWords += 1

                    sentences_list[idxSentences] = word_values

            idxSentences += 1
        firstDoc = False



    for x in range(len(sentences_list)):
        for k in range(len(sentences_list[x])):
            sentences_list[x][k]['MPS'] = np.average(sentences_list[x][k]['MPS'])
            sentences_list[x][k]['TRT'] = np.average(sentences_list[x][k]['TRT'])
            sentences_list[x][k]['GD'] = np.average(sentences_list[x][k]['GD'])
            sentences_list[x][k]['FFD'] = np.average(sentences_list[x][k]['FFD'])
            sentences_list[x][k]['GPT'] = np.average(sentences_list[x][k]['GPT'])
            sentences_list[x][k]['nFix'] = np.average(sentences_list[x][k]['nFix'])

    return sentences_list

df = getWordsMeanValues()


'''
def printAll():
    for file in os.listdir(rootdir):
        if file.endswith("TSR.mat"):
            print(file)

            file_name = rootdir + file
            subject = file_name.split("ts")[1].split("_")[0]
            #print(subject)
            # exclude YMH due to incomplete data because of dyslexia
            if subject != 'YMH':

                f = h5py.File(file_name, 'r')

                sentence_data = f['sentenceData']
                rawData = sentence_data['rawData']
                contentData = sentence_data['content']
                omissionR = sentence_data['omissionRate']
                wordData = sentence_data['word']

                # number of sentences:
                # print(len(rawData))

                for idx in range(len(rawData)):
                    obj_reference_content = contentData[idx][0]
                    sent = dh.load_matlab_string(f[obj_reference_content])

                    # get omission rate
                    obj_reference_omr = omissionR[idx][0]
                    omr = np.array(f[obj_reference_omr])
                    #print('OMR ',omr)

                    # get word level data
                    word_data = dh.extract_word_level_data(f, f[wordData[idx][0]])

                    # number of tokens
                    # print(len(word_data))

                    for widx in range(len(word_data)):

                        print('CONTENT ', word_data[widx]['content'], ' INDEX ',word_data[widx]['word_idx'])
                        print('nFIX', word_data[widx]['nFix'])
                        print('Pupil Size', word_data[widx]['meanPupilSize'])
                        # get first fixation duration (FFD)
                        print('FFD', word_data[widx]['FFD'])
                        
                        print('TRT', word_data[widx]['TRT'])
                        print('GD', word_data[widx]['GD'])
                        print('GPT', word_data[widx]['GPT'])

                        print('SFD', word_data[widx]['SFD'])
                        print('')
'''